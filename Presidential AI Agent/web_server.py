"""
Serve the static site and POST /api/chat using only my_agent.root_agent (no sub-agents).

Run from project root: uvicorn web_server:app --reload --host 127.0.0.1 --port 8000

Set ADK_LOG_LEVEL=DEBUG for verbose logs. Health: GET /api/health
"""

from __future__ import annotations

import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from google.genai import types
from pydantic import BaseModel, Field

_PROJECT_ROOT = Path(__file__).resolve().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

load_dotenv(_PROJECT_ROOT / "my_agent" / ".env")
load_dotenv(_PROJECT_ROOT / ".env")

logging.basicConfig(
    level=os.environ.get("ADK_LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("presidential_web")

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.utils.context_utils import Aclosing

from my_agent.agent import root_agent

APP_NAME = "presidential_web"

runner: Runner | None = None
session_service: InMemorySessionService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global runner, session_service
    has_key = bool(os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))
    log.info(
        "Loading ADK agent name=%s model=%s GOOGLE_API_KEY_set=%s",
        getattr(root_agent, "name", "?"),
        getattr(root_agent, "model", "?"),
        has_key,
    )
    if not has_key:
        log.warning(
            "No GOOGLE_API_KEY or GEMINI_API_KEY in environment — agent calls will fail until set."
        )
    session_service = InMemorySessionService()
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
        auto_create_session=False,
    )
    log.info("Runner ready app_name=%s", APP_NAME)
    yield
    if runner is not None:
        await runner.close()
    runner = None
    session_service = None
    log.info("Runner closed")


app = FastAPI(title="Presidential site + ADK", lifespan=lifespan)
# allow_credentials=True cannot be combined with allow_origins=["*"] (browser CORS rules).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000)
    session_id: str | None = None
    user_id: str = "website"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


class HealthResponse(BaseModel):
    ok: bool
    app_name: str
    agent_name: str
    agent_model: str
    runner_ready: bool
    google_api_key_configured: bool


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Use this in the browser or `curl` to verify the server and ADK agent loaded."""
    key_ok = bool(os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))
    ready = runner is not None and session_service is not None
    return HealthResponse(
        ok=ready and key_ok,
        app_name=APP_NAME,
        agent_name=str(getattr(root_agent, "name", "unknown")),
        agent_model=str(getattr(root_agent, "model", "unknown")),
        runner_ready=ready,
        google_api_key_configured=key_ok,
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    if runner is None or session_service is None:
        log.error("chat called but runner not initialized")
        raise HTTPException(status_code=503, detail="Agent runner not ready.")

    user_id = body.user_id.strip() or "website"
    session_id = body.session_id
    preview = body.message[:120] + ("…" if len(body.message) > 120 else "")
    log.info("chat user_id=%s session_id=%s message_preview=%r", user_id, session_id, preview)

    try:
        sess = None
        if session_id:
            sess = await session_service.get_session(
                app_name=APP_NAME, user_id=user_id, session_id=session_id
            )
        if sess is None:
            created = await session_service.create_session(
                app_name=APP_NAME, user_id=user_id
            )
            session_id = created.id
            log.debug("created session id=%s", session_id)

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=body.message)],
        )

        last_text = ""
        event_count = 0
        async with Aclosing(
            runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content,
            )
        ) as agen:
            async for event in agen:
                event_count += 1
                if event.content and event.content.parts:
                    merged = "\n".join(
                        p.text
                        for p in event.content.parts
                        if p.text and not getattr(p, "thought", None)
                    )
                    if merged:
                        last_text = merged

        log.info(
            "chat done session_id=%s events=%s reply_len=%s",
            session_id,
            event_count,
            len(last_text),
        )
        return ChatResponse(reply=last_text or "(No text reply.)", session_id=session_id)
    except HTTPException:
        raise
    except Exception as e:
        log.exception("chat failed: %s", e)
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {e!s}"[:800],
        ) from e


app.mount(
    "/",
    StaticFiles(directory=str(_PROJECT_ROOT / "website"), html=True),
    name="site",
)
