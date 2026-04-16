(function () {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const log = document.getElementById("chat-log");
  const statusEl = document.getElementById("chat-status");
  const SESSION_KEY = "presidential_adk_session_id";
  const USER_KEY = "presidential_adk_user_id";

  if (!form || !input || !log || !statusEl) {
    return;
  }

  const bannerEl = document.getElementById("chat-api-banner");
  const debugMeta = document.querySelector('meta[name="adk-debug"]')?.getAttribute("content");
  const debug =
    debugMeta === "true" ||
    debugMeta === "1" ||
    new URLSearchParams(window.location.search).get("debug") === "1";

  function dbg() {
    if (debug && typeof console !== "undefined" && console.debug) {
      console.debug.apply(console, arguments);
    }
  }

  /** Where the FastAPI app runs (same process as the ADK agent). */
  const STATIC_DEV_PORTS = new Set(["5500", "5501", "5173", "3000", "4173", "4200"]);

  function chatApiUrl() {
    const raw = document.querySelector('meta[name="chat-api-base"]')?.getAttribute("content");
    const base = (raw || "").trim();
    if (base) {
      return base.replace(/\/$/, "") + "/api/chat";
    }
    if (window.location.protocol === "file:") {
      return "http://127.0.0.1:8000/api/chat";
    }
    const host = window.location.hostname;
    const port = window.location.port || "";
    const local = host === "localhost" || host === "127.0.0.1";
    if (local && port && STATIC_DEV_PORTS.has(port)) {
      return "http://" + host + ":8000/api/chat";
    }
    return "/api/chat";
  }

  function healthApiUrl() {
    const c = chatApiUrl();
    if (c.startsWith("http://") || c.startsWith("https://")) {
      return c.replace(/\/?api\/chat\/?$/, "/api/health");
    }
    return "/api/health";
  }

  async function checkApiOnce() {
    if (!bannerEl) return;
    try {
      const url = healthApiUrl();
      dbg("[ADK] GET", url);
      const r = await fetch(url, { method: "GET", mode: "cors" });
      const ct = (r.headers.get("content-type") || "").toLowerCase();
      let payload = {};
      if (ct.includes("application/json")) {
        payload = await r.json().catch(() => ({}));
      }
      dbg("[ADK] health", r.status, payload);
      if (!r.ok) {
        bannerEl.hidden = false;
        bannerEl.classList.remove("chat-api-banner--warn");
        bannerEl.classList.add("chat-api-banner--error");
        bannerEl.textContent =
          "Assistant API returned HTTP " +
          r.status +
          ". Start the server: uvicorn web_server:app --host 127.0.0.1 --port 8000";
        return;
      }
      if (payload.runner_ready === false) {
        bannerEl.hidden = false;
        bannerEl.classList.remove("chat-api-banner--warn");
        bannerEl.classList.add("chat-api-banner--error");
        bannerEl.textContent = "Agent runner is not ready (check server logs).";
        return;
      }
      if (payload.google_api_key_configured === false) {
        bannerEl.hidden = false;
        bannerEl.classList.remove("chat-api-banner--error");
        bannerEl.classList.add("chat-api-banner--warn");
        bannerEl.textContent =
          "GOOGLE_API_KEY / GEMINI_API_KEY not loaded — set my_agent/.env and restart uvicorn.";
        return;
      }
      bannerEl.hidden = true;
      bannerEl.textContent = "";
      bannerEl.classList.remove("chat-api-banner--error", "chat-api-banner--warn");
    } catch (e) {
      dbg("[ADK] health error", e);
      bannerEl.hidden = false;
      bannerEl.classList.remove("chat-api-banner--warn");
      bannerEl.classList.add("chat-api-banner--error");
      bannerEl.textContent =
        "Cannot reach the assistant API at " +
        healthApiUrl() +
        ". Run uvicorn from the project folder and open this site via http://127.0.0.1:8000 (or set chat-api-base).";
    }
  }

  checkApiOnce();

  function uid() {
    if (!sessionStorage.getItem(USER_KEY)) {
      sessionStorage.setItem(
        USER_KEY,
        "web-" + Math.random().toString(36).slice(2, 12)
      );
    }
    return sessionStorage.getItem(USER_KEY);
  }

  function appendLine(role, text) {
    const row = document.createElement("div");
    row.className = "chat-msg " + (role === "user" ? "chat-msg-user" : "chat-msg-assistant");
    const label = document.createElement("span");
    label.className = "chat-msg-label";
    label.textContent = role === "user" ? "You" : "Assistant";
    const body = document.createElement("p");
    body.className = "chat-msg-body";
    body.textContent = text;
    row.appendChild(label);
    row.appendChild(body);
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
  }

  function setStatus(msg) {
    statusEl.textContent = msg || "";
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = (input.value || "").trim();
    if (!text) return;

    appendLine("user", text);
    input.value = "";
    setStatus("Thinking…");
    form.querySelector("button[type=submit]").disabled = true;

    try {
      const sid = sessionStorage.getItem(SESSION_KEY);
      const endpoint = chatApiUrl();
      dbg("[ADK] POST", endpoint, { session_id: sid || null });
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          session_id: sid || null,
          user_id: uid(),
        }),
        mode: "cors",
      });
      dbg("[ADK] response status", res.status);
      const ct = (res.headers.get("content-type") || "").toLowerCase();
      let data = {};
      if (ct.includes("application/json")) {
        data = await res.json().catch(() => ({}));
      } else {
        const raw = await res.text();
        if (!res.ok) {
          throw new Error(raw.slice(0, 300) || res.statusText || "Request failed");
        }
      }
      if (!res.ok) {
        const detail = data.detail || res.statusText || "Request failed";
        throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
      }
      if (data.session_id) {
        sessionStorage.setItem(SESSION_KEY, data.session_id);
      }
      appendLine("assistant", data.reply || "");
    } catch (err) {
      const hint =
        "Start the API: uvicorn web_server:app --reload --host 127.0.0.1 --port 8000. " +
        "Then open the site at http://127.0.0.1:8000 (same server serves the page and /api/chat). " +
        "If you use Live Server on another port, set <meta name=\"chat-api-base\" content=\"http://127.0.0.1:8000\"> in index.html.";
      appendLine("assistant", hint + " — " + String(err.message || err));
    } finally {
      setStatus("");
      form.querySelector("button[type=submit]").disabled = false;
    }
  });
})();
