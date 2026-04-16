"""
Serve the static site and ADK chat API (root_agent + specialist sub-agents).

Run from project root: uvicorn web_server:app --reload --host 127.0.0.1 --port 8000

Set ADK_LOG_LEVEL=DEBUG for verbose logs. Health: GET /api/health. Agent list: GET /api/agents
"""

from __future__ import annotations

import logging
import os
import re
import sys
from collections import defaultdict
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

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
from my_agent.chat_options import CHAT_AGENT_OPTIONS, assistant_display_title

APP_NAME = "presidential_web"

AgentChoice = Literal[
    "auto",
    "root_agent",
    "agriculture_agent",
    "farm_bill_agent",
    "usda_programs_agent",
    "food_security_agent",
    "commodity_policy_agent",
    "criminal_justice_agent",
    "policing_reform_agent",
    "courts_sentencing_agent",
    "economic_agent",
    "education_agent",
    "environment_agent",
    "foreign_relations_agent",
    "healthcare_agent",
    "housing_agent",
    "immigration_agent",
    "infrastructure_agent",
    "military_agent",
    "national_security_agent",
    "technology_agent",
    "transportation_agent",
    "veterans_agent",
]

runner: Runner | None = None
session_service: InMemorySessionService | None = None


def merge_stream_chunks(chunks: list[str]) -> str:
    """Rebuild one assistant reply from ADK chunks for a single author.

    Gemini/ADK may stream **cumulative** snapshots (each event repeats the prefix and grows) or **delta** tokens
    (each event is only new tokens). Taking ``max(len)`` on chunks drops most of a delta stream (no chart JSON).
    Taking only one arbitrary chunk can miss content. This uses a small heuristic.
    """
    xs = [c for c in (chunks or []) if c and str(c).strip()]
    if not xs:
        return ""
    if len(xs) == 1:
        return xs[0]
    first = xs[0].strip()
    last_raw = xs[-1]
    last = last_raw.strip()
    longest = max(xs, key=lambda s: len(s))
    # Cumulative streaming: the final event is usually the full text and the longest string.
    if last_raw == longest:
        return last_raw
    head = first[: min(500, len(first))]
    if head and head in last:
        return last_raw
    if last.startswith(first[: min(200, len(first))]):
        return last_raw
    # Delta-style token chunks: concatenate in order
    return "".join(xs)


def extract_model_text_from_parts(parts) -> str:
    """Visible model text only (skip thought / tool parts when attributes exist)."""
    if not parts:
        return ""
    out: list[str] = []
    for p in parts:
        if getattr(p, "thought", None):
            continue
        if getattr(p, "function_call", None) or getattr(p, "function_response", None):
            continue
        t = getattr(p, "text", None)
        if t:
            out.append(str(t))
    return "\n".join(out)


# Users ask for charts in plain language; they never type <<<CHART>>>. When we see chart-ish wording, nudge the model.
CHART_INTENT_RE = re.compile(
    r"(?i)\b("
    r"charts?|graphs?|plots?|histogram|diagrams?|visuali[sz]e|visualisation|visualization|"
    r"data\s+visuali[sz]ation|data\s+viz\b|"
    r"bar\s*charts?|line\s*charts?|line\s*graphs?|pie\s*charts?|pie\s*graphs?|"
    r"show\s+(?:me\s+)?(?:a\s+)?(?:the\s+)?(?:numbers|data)\b|"
    r"(?:as\s+)?(?:a\s+)?(?:bar|line|pie)\b|"
    r"end\s+strength|manpower\b|headcount\b|by\s+service|active\s+duty\s+vs\.?\s*reserve|demographics\b|"
    r"past\s+\d+\s+years?|over\s+the\s+past\s+\d+|last\s+\d+\s+years?"
    r")\b"
)


# Extra nudge when the user asks for a trend / multi-year line (plain English).
LINE_CHART_TIME_RE = re.compile(
    r"(?is)\b("
    r"line\s*(?:graph|chart)|trend|over\s+the\s+past\s+\d+|past\s+\d+\s+years?|"
    r"last\s+\d+\s+years?|five\s+years?|5\s+years?"
    r")\b"
)


def apply_chart_intent_hint(text_for_model: str, original_user_message: str) -> str:
    """Append an assistant-only reminder when the user asked for a chart without special syntax."""
    if not (original_user_message and CHART_INTENT_RE.search(original_user_message)):
        return text_for_model
    tail = (
        "\n\n[Assistant reminder: The user asked for a chart using plain language only — they do not type "
        "<<<CHART>>> or any codes. Still include one valid chart JSON for the website per your chart instructions "
        "(<<<CHART>>>…<<<END_CHART>>> or an accepted fallback). Never ask them to use special tags.]\n"
    )
    out = text_for_model.rstrip() + tail
    if LINE_CHART_TIME_RE.search(original_user_message):
        out += (
            "\n[Time series: If they asked for a **line** graph or “past N years”, use JSON "
            '"type":"line", one label per year (or FY), one series, data length = labels length. '
            "Search for real figures; if the topic is vague, pick **one** explicit metric in the chart title.]\n"
        )
    return out


def apply_military_viz_hint(text_for_model: str, agent_choice: AgentChoice) -> str:
    """The military advisor often compares public workforce numbers — nudge valid <<<CHART>>> JSON for the website."""
    if agent_choice != "military_agent":
        return text_for_model
    tail = (
        "\n\n[Military advisor — site graphics: If your reply includes **comparable public numbers** (e.g. end strength "
        "by service, active vs reserve, demographic shares, trends across years), you **must** add **one** valid "
        "<<<CHART>>>…<<<END_CHART>>> JSON object per Office chart rules so the page can render a chart. If they asked for a "
        "**line graph** or **past N years**, use `\"type\":\"line\"` with one data point per year — same as other advisors. "
        "Prose with several figures but no chart block is a failed response when a chart is possible.] \n"
    )
    return text_for_model.rstrip() + tail


def apply_routing_hint(message: str, agent_choice: AgentChoice) -> str:
    """Prefix user text so root_agent honors UI routing (see my_agent.prompt.ROOT_AGENT_INSTR).

    Farm Bill, USDA program, food security, and commodity policy picks are nested under agriculture_agent; policing reform
    and courts/sentencing picks are nested under criminal_justice_agent — rewrite to Sub-delegate lines the coordinators
    understand.
    """
    if not agent_choice or agent_choice == "auto":
        return message
    if agent_choice == "farm_bill_agent":
        return (
            "[User routing preference: agriculture_agent]\n\n"
            "[Sub-delegate: farm_bill_agent]\n\n"
            + message
        )
    if agent_choice == "usda_programs_agent":
        return (
            "[User routing preference: agriculture_agent]\n\n"
            "[Sub-delegate: usda_programs_agent]\n\n"
            + message
        )
    if agent_choice == "food_security_agent":
        return (
            "[User routing preference: agriculture_agent]\n\n"
            "[Sub-delegate: food_security_agent]\n\n"
            + message
        )
    if agent_choice == "commodity_policy_agent":
        return (
            "[User routing preference: agriculture_agent]\n\n"
            "[Sub-delegate: commodity_policy_agent]\n\n"
            + message
        )
    if agent_choice == "policing_reform_agent":
        return (
            "[User routing preference: criminal_justice_agent]\n\n"
            "[Sub-delegate: policing_reform_agent]\n\n"
            + message
        )
    if agent_choice == "courts_sentencing_agent":
        return (
            "[User routing preference: criminal_justice_agent]\n\n"
            "[Sub-delegate: courts_sentencing_agent]\n\n"
            + message
        )
    return f"[User routing preference: {agent_choice}]\n\n" + message


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
    agent_choice: AgentChoice = "auto"


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    responding_agent: str | None = Field(
        default=None,
        description="ADK event.author for the last streamed model text (e.g. economic_agent).",
    )
    assistant_title: str = Field(
        default="Office Assistant",
        description="User-facing name for the responding assistant.",
    )


class HealthResponse(BaseModel):
    ok: bool
    app_name: str
    agent_name: str
    agent_model: str
    runner_ready: bool
    google_api_key_configured: bool
    sub_agent_names: list[str]


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Use this in the browser or `curl` to verify the server and ADK agent loaded."""
    key_ok = bool(os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))
    ready = runner is not None and session_service is not None
    sub_names = [getattr(a, "name", "") for a in getattr(root_agent, "sub_agents", []) or []]
    return HealthResponse(
        ok=ready and key_ok,
        app_name=APP_NAME,
        agent_name=str(getattr(root_agent, "name", "unknown")),
        agent_model=str(getattr(root_agent, "model", "unknown")),
        runner_ready=ready,
        google_api_key_configured=key_ok,
        sub_agent_names=[n for n in sub_names if n],
    )


@app.get("/api/agents")
async def list_chat_agents() -> list[dict[str, str]]:
    """Labels and ids for the assistant UI (aligned with ChatRequest.agent_choice)."""
    return CHAT_AGENT_OPTIONS


@app.post("/api/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    if runner is None or session_service is None:
        log.error("chat called but runner not initialized")
        raise HTTPException(status_code=503, detail="Agent runner not ready.")

    user_id = body.user_id.strip() or "website"
    session_id = body.session_id
    preview = body.message[:120] + ("…" if len(body.message) > 120 else "")
    log.info(
        "chat user_id=%s session_id=%s agent_choice=%s message_preview=%r",
        user_id,
        session_id,
        body.agent_choice,
        preview,
    )

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

        text_for_model = apply_routing_hint(body.message, body.agent_choice)
        text_for_model = apply_chart_intent_hint(text_for_model, body.message)
        text_for_model = apply_military_viz_hint(text_for_model, body.agent_choice)
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=text_for_model)],
        )

        # Per-author streamed text. Keep every chunk; at the end pick the **longest** non-empty merge for the chosen
        # author — handles incremental deltas, duplicates, and avoids a short trailing root_agent chunk replacing the full
        # specialist reply (with <<<CHART>>> JSON).
        chunks_by_author: defaultdict[str, list[str]] = defaultdict(list)
        last_merged_any: str = ""
        # ADK often ends with root_agent after a sub-agent; prefer specialist for attribution and reply body.
        last_agent_with_visible_text: str | None = None
        last_non_root_agent: str | None = None
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
                    merged = extract_model_text_from_parts(event.content.parts)
                    if merged:
                        last_merged_any = merged
                        auth = getattr(event, "author", None)
                        if auth is None:
                            continue
                        aid = str(auth).strip()
                        low = aid.lower()
                        if low == "user":
                            continue
                        chunks_by_author[aid].append(merged)
                        last_agent_with_visible_text = aid
                        if low != "root_agent":
                            last_non_root_agent = aid

        def _merged_for(agent_id: str | None) -> str:
            if not agent_id:
                return ""
            return merge_stream_chunks(chunks_by_author.get(agent_id) or [])

        responding_agent = last_non_root_agent or last_agent_with_visible_text
        assistant_title = assistant_display_title(responding_agent)
        if last_non_root_agent:
            pick = _merged_for(last_non_root_agent)
            last_text = pick.strip() and pick or last_merged_any
        elif last_agent_with_visible_text:
            pick = _merged_for(last_agent_with_visible_text)
            last_text = pick.strip() and pick or last_merged_any
        else:
            last_text = last_merged_any
        log.info(
            "chat done session_id=%s events=%s reply_len=%s responding_agent=%s",
            session_id,
            event_count,
            len(last_text),
            responding_agent,
        )
        return ChatResponse(
            reply=last_text or "(No text reply.)",
            session_id=session_id,
            responding_agent=responding_agent,
            assistant_title=assistant_title,
        )
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
