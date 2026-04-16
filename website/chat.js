(function () {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const log = document.getElementById("chat-log");
  const statusEl = document.getElementById("chat-status");
  const agentChoiceEl = document.getElementById("chat-agent-choice");
  const SESSION_KEY = "presidential_adk_session_id";
  const USER_KEY = "presidential_adk_user_id";
  const HISTORY_KEY = "presidential_chat_history_v2";

  const exportTxtBtn = document.getElementById("chat-export-txt");
  const exportJsonBtn = document.getElementById("chat-export-json");
  const exportCsvBtn = document.getElementById("chat-export-csv");
  const clearBtn = document.getElementById("chat-clear");

  if (!form || !input || !log || !statusEl) {
    return;
  }

  /** In-memory transcript; persisted for class demos (localStorage). */
  let messageHistory = [];

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

  function agentsApiUrl() {
    const c = chatApiUrl();
    if (c.startsWith("http://") || c.startsWith("https://")) {
      return c.replace(/\/?api\/chat\/?$/, "/api/agents");
    }
    return "/api/agents";
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

  async function loadAgentOptions() {
    if (!agentChoiceEl) return;
    try {
      const url = agentsApiUrl();
      dbg("[ADK] GET", url);
      const r = await fetch(url, { method: "GET", mode: "cors" });
      if (!r.ok) return;
      const ct = (r.headers.get("content-type") || "").toLowerCase();
      if (!ct.includes("application/json")) return;
      const list = await r.json();
      if (!Array.isArray(list) || list.length === 0) return;
      const current = agentChoiceEl.value;
      agentChoiceEl.innerHTML = "";
      list.forEach(function (a) {
        if (!a || !a.id) return;
        const opt = document.createElement("option");
        opt.value = a.id;
        opt.textContent = a.label || a.id;
        if (a.description) opt.title = a.description;
        agentChoiceEl.appendChild(opt);
      });
      if (
        current &&
        Array.from(agentChoiceEl.options).some(function (o) {
          return o.value === current;
        })
      ) {
        agentChoiceEl.value = current;
      }
    } catch (e) {
      dbg("[ADK] agents list error", e);
    }
  }

  function uid() {
    if (!sessionStorage.getItem(USER_KEY)) {
      sessionStorage.setItem(USER_KEY, "web-" + Math.random().toString(36).slice(2, 12));
    }
    return sessionStorage.getItem(USER_KEY);
  }

  function getRoutingLabel(routingId) {
    if (!agentChoiceEl || !routingId) return routingId || "auto";
    const opt = Array.from(agentChoiceEl.options).find(function (o) {
      return o.value === routingId;
    });
    return opt ? opt.textContent.trim() : routingId;
  }

  function nowIso() {
    return new Date().toISOString();
  }

  function slugFromParts(routingId) {
    const safe = String(routingId || "exchange").replace(/[^\w.-]+/g, "_");
    const t = Date.now();
    return safe + "-" + t;
  }

  function triggerDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.rel = "noopener";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function downloadTextFile(text, filename, mime) {
    const blob = new Blob([text], { type: mime || "text/plain;charset=utf-8" });
    triggerDownload(blob, filename);
  }

  /** Prefer official markers; models often vary brackets/spacing — try several before giving up. */
  function extractDelimitedChart(raw) {
    var s = String(raw || "");
    var patterns = [
      /<<<CHART>>>\s*([\s\S]*?)\s*<<<END_CHART>>>/i,
      /<<CHART>>\s*([\s\S]*?)\s*<<END_CHART>>/i,
      /<\s*CHART\s*>\s*([\s\S]*?)\s*<\s*END\s*CHART\s*>/i,
    ];
    for (var pi = 0; pi < patterns.length; pi++) {
      var m = s.match(patterns[pi]);
      if (m && m.index != null) {
        return { inner: m[1], index: m.index, length: m[0].length };
      }
    }
    return null;
  }

  function sanitizeChartJsonBlob(inner) {
    var s = String(inner || "").trim().replace(/^\uFEFF/, "");
    s = s.replace(/^```(?:json)?\s*/i, "");
    s = s.replace(/\s*```\s*$/i, "");
    s = s.trim();
    s = s.replace(/```(?:json)?/gi, "");
    s = s.replace(/```/g, "");
    s = s.replace(/[\u201C\u201D]/g, '"').replace(/[\u2018\u2019]/g, "'");
    return s.trim();
  }

  /** Models often break JSON by putting real newlines inside "..." strings — illegal in JSON. Collapse to spaces. */
  function repairModelJsonNewlines(s) {
    return String(s || "")
      .replace(/\r\n/g, "\n")
      .replace(/\r/g, "\n")
      .replace(/\n/g, " ")
      .replace(/ {2,}/g, " ")
      .trim();
  }

  /** Trailing commas before } or ] — common in model JSON; JSON.parse rejects them. */
  function repairJsonTrailingCommas(s) {
    return String(s || "").replace(/,(\s*[}\]])/g, "$1");
  }

  function tryParseChartSpecFromString(inner) {
    var cleaned = sanitizeChartJsonBlob(inner);
    if (!cleaned) return null;
    var candidates = [cleaned];
    var repaired = repairModelJsonNewlines(cleaned);
    if (repaired !== cleaned) {
      candidates.push(repaired);
    }
    var deTrail = repairJsonTrailingCommas(cleaned);
    if (deTrail !== cleaned) {
      candidates.push(deTrail);
      var both = repairModelJsonNewlines(deTrail);
      if (both !== deTrail) candidates.push(both);
    }
    for (var ci = 0; ci < candidates.length; ci++) {
      var c = candidates[ci];
      try {
        return JSON.parse(c);
      } catch (e) {
        var si = c.indexOf("{");
        var ei = c.lastIndexOf("}");
        if (si >= 0 && ei > si) {
          try {
            return JSON.parse(c.slice(si, ei + 1));
          } catch (e2) {
            /* continue */
          }
        }
      }
    }
    return null;
  }

  function coerceChartNumber(v) {
    if (typeof v === "number" && !isNaN(v)) return v;
    if (typeof v === "string") {
      var n = parseFloat(v.replace(/,/g, "").trim());
      return isNaN(n) ? 0 : n;
    }
    return 0;
  }

  /**
   * Many models emit Chart.js-style `{ labels, datasets: [{ label, data }] }` or use `categories` instead of `labels`.
   * Normalize into our `{ labels, series: [{ label, data }] }` shape before validation.
   */
  function shapeChartSpecFromModel(obj) {
    if (!obj || typeof obj !== "object") return null;
    var labels = Array.isArray(obj.labels) ? obj.labels : Array.isArray(obj.categories) ? obj.categories : null;
    var series = Array.isArray(obj.series) ? obj.series : null;
    if ((!series || !series.length) && Array.isArray(obj.datasets)) {
      series = obj.datasets.map(function (d, idx) {
        return {
          label: d && d.label != null ? String(d.label) : "Series " + (idx + 1),
          data: d && Array.isArray(d.data) ? d.data : [],
        };
      });
    }
    if ((!series || !series.length) && Array.isArray(labels) && Array.isArray(obj.data)) {
      series = [{ label: "Values", data: obj.data }];
    }
    if (!Array.isArray(labels) || labels.length === 0 || !Array.isArray(series) || series.length === 0) {
      return null;
    }
    return {
      title: obj.title,
      type: obj.type,
      labels: labels,
      series: series,
    };
  }

  /** Map common model phrasing ("bar chart", "line graph") to bar | line | pie. */
  function normalizeChartTypeString(raw) {
    var s = String(raw || "bar")
      .toLowerCase()
      .trim()
      .replace(/[\u201C\u201D\u2018\u2019]/g, '"')
      .replace(/\s+/g, "");
    if (s === "pie" || s === "piechart") return "pie";
    if (s === "line" || s === "linechart" || s === "linegraph") return "line";
    if (s === "bar" || s === "barchart" || s === "column" || s === "columnchart") return "bar";
    return null;
  }

  /** Returns a canonical spec for Chart.js or null if invalid. */
  function validateAndNormalizeChartSpec(spec) {
    if (!spec || typeof spec !== "object") return null;
    var coerced = shapeChartSpecFromModel(spec);
    if (coerced) spec = coerced;
    var t = normalizeChartTypeString(spec.type || "bar");
    if (!t) return null;
    if (!Array.isArray(spec.labels) || spec.labels.length === 0) return null;
    var labels = spec.labels.map(function (x) {
      return String(x);
    });
    if (!Array.isArray(spec.series) || spec.series.length === 0) return null;
    var series = spec.series.map(function (ser, i) {
      var lab = ser && ser.label != null ? String(ser.label) : "Series " + (i + 1);
      var data = ser && Array.isArray(ser.data) ? ser.data : [];
      data = data.map(coerceChartNumber);
      return { label: lab, data: data };
    });
    if (t === "pie") {
      if (series.length !== 1) return null;
      if (series[0].data.length !== labels.length) return null;
    } else {
      for (var j = 0; j < series.length; j++) {
        if (series[j].data.length !== labels.length) return null;
      }
    }
    return {
      title: spec.title != null ? String(spec.title) : "",
      type: t,
      labels: labels,
      series: series,
    };
  }

  /** Walk `raw` from `openIndex` (must be '{') and return index of matching '}' or -1. Respects JSON string escaping. */
  function findMatchingJsonBraceEnd(raw, openIndex) {
    if (openIndex < 0 || openIndex >= raw.length || raw[openIndex] !== "{") return -1;
    var depth = 0;
    var inStr = false;
    var esc = false;
    for (var i = openIndex; i < raw.length; i++) {
      var c = raw[i];
      if (esc) {
        esc = false;
        continue;
      }
      if (inStr) {
        if (c === "\\") esc = true;
        else if (c === '"') inStr = false;
        continue;
      }
      if (c === '"') {
        inStr = true;
        continue;
      }
      if (c === "{") depth++;
      else if (c === "}") {
        depth--;
        if (depth === 0) return i;
      }
    }
    return -1;
  }

  /**
   * Models sometimes emit a chart as a plain JSON object without <<<CHART>>> or fenced blocks. Scan for JSON objects
   * and accept the **best** chart spec (longest matching JSON) so a small `{ "x":1 }` does not win over the real chart.
   */
  function tryExtractLooseEmbeddedChart(raw) {
    var s = String(raw || "");
    var best = null;
    var bestLen = -1;
    var bestStart = 0;
    var bestEnd = 0;
    for (var i = 0; i < s.length; i++) {
      if (s[i] !== "{") continue;
      var end = findMatchingJsonBraceEnd(s, i);
      if (end < 0) continue;
      var slice = s.slice(i, end + 1);
      var parsed = tryParseChartSpecFromString(slice);
      var norm = validateAndNormalizeChartSpec(parsed);
      if (norm && slice.length > bestLen) {
        bestLen = slice.length;
        best = norm;
        bestStart = i;
        bestEnd = end + 1;
      }
    }
    if (!best) return null;
    var displayText = (s.slice(0, bestStart) + s.slice(bestEnd)).trim();
    return { spec: best, displayText: displayText };
  }

  /** Fallback: ```json ... ``` with chart shape (models often ignore <<<CHART>>> markers). */
  function tryExtractFencedChartBlock(raw) {
    var re = /```(?:json)?\s*([\s\S]*?)\s*```/gi;
    var match;
    while ((match = re.exec(raw)) !== null) {
      var parsed = tryParseChartSpecFromString(match[1]);
      var norm = validateAndNormalizeChartSpec(parsed);
      if (norm) {
        var dt = (raw.slice(0, match.index) + raw.slice(match.index + match[0].length)).trim();
        return { spec: norm, displayText: dt };
      }
    }
    return null;
  }

  function parseAssistantChart(raw) {
    if (raw == null || typeof raw !== "string") {
      return { displayText: "", spec: null };
    }
    var body = String(raw);
    var trimOnce = body.trim();
    if (/^```(?:json)?\s*\{/i.test(trimOnce) && trimOnce.lastIndexOf("```") > 3) {
      var unfenced = trimOnce
        .replace(/^```(?:json)?\s*/i, "")
        .replace(/\s*```\s*$/i, "")
        .trim();
      if (unfenced !== trimOnce && unfenced.indexOf("{") >= 0) {
        body = unfenced;
      }
    }
    var dm = extractDelimitedChart(body);
    if (dm) {
      var parsed = tryParseChartSpecFromString(dm.inner);
      var norm = validateAndNormalizeChartSpec(parsed);
      var stripped = (body.slice(0, dm.index) + body.slice(dm.index + dm.length)).trim();
      if (norm) {
        return { displayText: stripped, spec: norm };
      }
      dbg("[chart] markers present but JSON/spec invalid");
      return { displayText: stripped, spec: null };
    }
    var fb = tryExtractFencedChartBlock(body);
    if (fb && fb.spec) {
      return { displayText: fb.displayText, spec: fb.spec };
    }
    var loose = tryExtractLooseEmbeddedChart(body);
    if (loose && loose.spec) {
      return { displayText: loose.displayText, spec: loose.spec };
    }
    return { displayText: body, spec: null };
  }

  function stripChartFromAssistant(raw) {
    return parseAssistantChart(raw).displayText;
  }

  function scheduleAfterDoubleFrame(fn) {
    if (typeof requestAnimationFrame !== "undefined") {
      requestAnimationFrame(function () {
        requestAnimationFrame(fn);
      });
    } else {
      window.setTimeout(fn, 0);
    }
  }

  function renderAssistantChartMount(wrapEl, spec) {
    var ChartCtor = typeof Chart !== "undefined" ? Chart : null;
    if (!ChartCtor) {
      var p = document.createElement("p");
      p.className = "chat-msg-chart-fallback";
      p.textContent = "Chart could not load (Chart.js unavailable).";
      wrapEl.appendChild(p);
      return null;
    }
    var canvas = document.createElement("canvas");
    canvas.className = "chat-msg-chart-canvas";
    canvas.setAttribute("role", "img");
    canvas.setAttribute("aria-label", spec.title ? String(spec.title) : "Data chart");
    wrapEl.appendChild(canvas);
    wrapEl.style.width = "100%";
    wrapEl.style.minWidth = "280px";
    wrapEl.style.boxSizing = "border-box";
    var colors = ["#1a2744", "#c9a227", "#5a7a9a", "#2d5a3c", "#6b4f2a", "#2c3e50"];
    var t = String(spec.type || "bar").toLowerCase();
    var titleText = spec.title ? String(spec.title) : "";

    function afterChartMount(chartInst) {
      if (!chartInst || typeof chartInst.resize !== "function") return;
      scheduleAfterDoubleFrame(function () {
        try {
          chartInst.resize();
        } catch (re) {
          dbg("[chart] resize failed", re);
        }
      });
    }

    try {
      if (t === "pie") {
        var nums = spec.series[0].data;
        var pieChart = new ChartCtor(canvas, {
          type: "pie",
          data: {
            labels: spec.labels,
            datasets: [
              {
                data: nums,
                backgroundColor: spec.labels.map(function (_, i) {
                  return colors[i % colors.length];
                }),
                borderColor: "#ffffff",
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 1.35,
            animation: false,
            plugins: {
              title: { display: !!titleText, text: titleText, font: { size: 14 } },
              legend: { position: "bottom" },
            },
          },
        });
        afterChartMount(pieChart);
        return canvas;
      }

      var datasets = spec.series.map(function (s, i) {
        var base = colors[i % colors.length];
        if (t === "line") {
          return {
            label: s.label || "Series " + (i + 1),
            data: s.data,
            borderColor: base,
            backgroundColor: base + "33",
            borderWidth: 2,
            tension: 0.2,
            fill: false,
          };
        }
        return {
          label: s.label || "Series " + (i + 1),
          data: s.data,
          backgroundColor: base + "cc",
          borderColor: base,
          borderWidth: 1,
        };
      });

      var xyChart = new ChartCtor(canvas, {
        type: t === "line" ? "line" : "bar",
        data: { labels: spec.labels, datasets: datasets },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          aspectRatio: 1.6,
          animation: false,
          plugins: {
            title: { display: !!titleText, text: titleText, font: { size: 14 } },
            legend: { position: "bottom" },
          },
          scales:
            t === "line" || t === "bar"
              ? {
                  x: { ticks: { maxRotation: 45, minRotation: 0 } },
                  y: { beginAtZero: true },
                }
              : {},
        },
      });
      afterChartMount(xyChart);
      return canvas;
    } catch (chartErr) {
      dbg("[chart] Chart.js render failed", chartErr);
      var errP = document.createElement("p");
      errP.className = "chat-msg-chart-fallback";
      errP.textContent = "Chart could not be drawn. Check that data is numeric and try again.";
      wrapEl.appendChild(errP);
      if (canvas.parentNode) canvas.parentNode.removeChild(canvas);
      return null;
    }
  }

  /**
   * One .txt document per successful reply (user gesture chain from Send).
   */
  function autoDownloadOfficeDocument(userMessage, reply, assistantTitle, routingLabel, respondingAgentId) {
    var replyBody = stripChartFromAssistant(reply || "");
    var pieces = [];
    pieces.push("Presidential Office — reply document");
    pieces.push("Generated: " + nowIso());
    pieces.push("Responded by: " + (assistantTitle || "Office Assistant"));
    pieces.push("Advisor mode (UI): " + (routingLabel || ""));
    pieces.push("");
    pieces.push("--- Your message ---");
    pieces.push(userMessage || "");
    pieces.push("");
    pieces.push("--- Response ---");
    pieces.push(replyBody.trim());
    var fn = "office-document-" + slugFromParts(respondingAgentId || "reply") + ".txt";
    downloadTextFile(pieces.join("\n"), fn, "text/plain;charset=utf-8");
  }

  function downloadAssistantPdf(text, routingId, chartCanvas) {
    const jspdf = window.jspdf;
    if (!jspdf || !jspdf.jsPDF) {
      downloadTextFile(
        text,
        "office-reply-" + slugFromParts(routingId) + ".txt",
        "text/plain;charset=utf-8"
      );
      setStatus("PDF library unavailable — saved as .txt instead.");
      return;
    }
    const { jsPDF } = jspdf;

    function runPdf() {
      const doc = new jsPDF({ unit: "mm", format: "a4" });
      const margin = 15;
      const pageHeight = doc.internal.pageSize.getHeight();
      const pageWidth = doc.internal.pageSize.getWidth();
      const maxWidth = pageWidth - 2 * margin;
      const lineHeight = 6;
      let y = margin;
      const body = (text || "").trim();

      if (body) {
        const lines = doc.splitTextToSize(body, maxWidth);
        lines.forEach(function (line) {
          if (y > pageHeight - margin - lineHeight) {
            doc.addPage();
            y = margin;
          }
          doc.text(line, margin, y);
          y += lineHeight;
        });
      } else if (chartCanvas && chartCanvas.width > 0) {
        doc.text("(Chart only — no separate text.)", margin, y);
        y += lineHeight + 2;
      }

      if (chartCanvas && chartCanvas.width > 0 && chartCanvas.height > 0) {
        var imgData = null;
        try {
          imgData = chartCanvas.toDataURL("image/png");
        } catch (e) {
          dbg("[pdf] toDataURL failed", e);
        }
        if (imgData) {
          y += 2;
          if (y > pageHeight - margin - 40) {
            doc.addPage();
            y = margin;
          }
          var imgW = maxWidth;
          var imgH = (chartCanvas.height / chartCanvas.width) * imgW;
          var maxH = 95;
          if (imgH > maxH) {
            var s = maxH / imgH;
            imgH = maxH;
            imgW = imgW * s;
          }
          if (y + imgH > pageHeight - margin) {
            doc.addPage();
            y = margin;
          }
          try {
            doc.addImage(imgData, "PNG", margin, y, imgW, imgH);
            y += imgH + 4;
          } catch (e) {
            dbg("[pdf] addImage failed", e);
            doc.text("(Chart image could not be embedded in this PDF.)", margin, y);
          }
        }
      }

      doc.save("office-reply-" + slugFromParts(routingId) + ".pdf");
    }

    if (chartCanvas) {
      scheduleAfterDoubleFrame(function () {
        window.setTimeout(runPdf, 220);
      });
    } else {
      runPdf();
    }
  }

  function pushHistoryEntry(entry) {
    messageHistory.push(entry);
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(messageHistory));
    } catch (e) {
      dbg("[chat] localStorage save failed", e);
    }
  }

  function loadHistory() {
    try {
      const raw = localStorage.getItem(HISTORY_KEY);
      if (!raw) return;
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        messageHistory = parsed;
      }
    } catch (e) {
      dbg("[chat] history parse error", e);
    }
  }

  function assistantTitleFromEntry(m) {
    if (m && m.assistantTitle) return m.assistantTitle;
    if (m && m.routingLabel) return m.routingLabel;
    return "Office Assistant";
  }

  function slugAgentIdFromEntry(m) {
    if (m && m.respondingAgentId) return m.respondingAgentId;
    if (m && m.routingId) return m.routingId;
    return "assistant";
  }

  function buildUserRow(text) {
    const row = document.createElement("div");
    row.className = "chat-msg chat-msg-user";
    const label = document.createElement("span");
    label.className = "chat-msg-label";
    label.textContent = "You";
    const body = document.createElement("p");
    body.className = "chat-msg-body";
    body.textContent = text;
    row.appendChild(label);
    row.appendChild(body);
    return row;
  }

  function buildAssistantRow(text, assistantTitle, slugAgentId) {
    const title =
      assistantTitle && String(assistantTitle).trim()
        ? String(assistantTitle).trim()
        : "Office Assistant";
    const slug = slugAgentId && String(slugAgentId).trim() ? String(slugAgentId).trim() : "assistant";
    const parsed = parseAssistantChart(text);
    const forFiles = stripChartFromAssistant(text);
    const row = document.createElement("div");
    row.className = "chat-msg chat-msg-assistant";
    const label = document.createElement("span");
    label.className = "chat-msg-label";
    label.textContent = title;
    const body = document.createElement("p");
    body.className = "chat-msg-body";
    const displayTxt = (parsed.displayText || "").trim();
    if (displayTxt) {
      body.textContent = displayTxt;
    } else if (parsed.spec) {
      body.textContent = "(See chart.)";
    } else {
      body.textContent = "(No text.)";
    }
    const actions = document.createElement("div");
    actions.className = "chat-msg-actions";
    const base = "office-reply-" + slugFromParts(slug);
    let chartCanvasEl = null;

    function addDownloadButton(caption, handler) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "chat-download-btn";
      b.textContent = caption;
      b.addEventListener("click", handler);
      actions.appendChild(b);
    }

    addDownloadButton("Download .txt", function () {
      downloadTextFile(forFiles, base + ".txt", "text/plain;charset=utf-8");
    });
    addDownloadButton("Download .md", function () {
      const header = "# " + title + "\n\n---\n\n";
      downloadTextFile(header + forFiles, base + ".md", "text/markdown;charset=utf-8");
    });
    addDownloadButton("Download .pdf", function () {
      downloadAssistantPdf(forFiles, slug, chartCanvasEl);
    });
    addDownloadButton("Download .csv", function () {
      downloadTextFile(forFiles, base + ".csv", "text/csv;charset=utf-8");
    });

    row.appendChild(label);
    row.appendChild(body);
    if (parsed.spec) {
      const wrap = document.createElement("div");
      wrap.className = "chat-msg-chart";
      chartCanvasEl = renderAssistantChartMount(wrap, parsed.spec);
      row.appendChild(wrap);
    }
    row.appendChild(actions);
    return row;
  }

  function appendUserMessage(text, routingId, routingLabel) {
    const ts = nowIso();
    pushHistoryEntry({
      role: "user",
      text: text,
      routingId: routingId,
      routingLabel: routingLabel,
      ts: ts,
    });
    log.appendChild(buildUserRow(text));
    log.scrollTop = log.scrollHeight;
  }

  function appendAssistantMessage(text, opts) {
    const routingId = opts && opts.routingId ? opts.routingId : "auto";
    const routingLabel = opts && opts.routingLabel ? opts.routingLabel : "";
    const respondingAgentId = opts && opts.respondingAgentId != null ? opts.respondingAgentId : null;
    const assistantTitle =
      opts && opts.assistantTitle && String(opts.assistantTitle).trim()
        ? String(opts.assistantTitle).trim()
        : "Office Assistant";
    const ts = nowIso();
    pushHistoryEntry({
      role: "assistant",
      text: text,
      routingId: routingId,
      routingLabel: routingLabel,
      respondingAgentId: respondingAgentId,
      assistantTitle: assistantTitle,
      ts: ts,
    });
    log.appendChild(
      buildAssistantRow(text, assistantTitle, respondingAgentId || routingId)
    );
    log.scrollTop = log.scrollHeight;
  }

  function renderLogFromHistory() {
    log.innerHTML = "";
    messageHistory.forEach(function (m) {
      if (!m || !m.role) return;
      if (m.role === "user") {
        log.appendChild(buildUserRow(m.text));
      } else if (m.role === "assistant") {
        log.appendChild(
          buildAssistantRow(m.text, assistantTitleFromEntry(m), slugAgentIdFromEntry(m))
        );
      }
    });
    log.scrollTop = log.scrollHeight;
  }

  function csvEscapeCell(s) {
    const t = String(s == null ? "" : s);
    if (/[",\n\r]/.test(t)) {
      return '"' + t.replace(/"/g, '""') + '"';
    }
    return t;
  }

  function exportTranscriptTxt() {
    const lines = [];
    lines.push("Presidential Office — chat transcript");
    lines.push("Exported: " + nowIso());
    lines.push("");
    let turn = 0;
    for (let i = 0; i < messageHistory.length; i++) {
      const m = messageHistory[i];
      if (!m) continue;
      if (m.role === "user") {
        turn += 1;
        lines.push("--- Turn " + turn + " ---");
        lines.push(
          "Requested advisor mode (UI): " + (m.routingLabel || m.routingId || "")
        );
        lines.push("You: " + m.text);
        lines.push("");
      } else if (m.role === "assistant") {
        lines.push(
          assistantTitleFromEntry(m) + ": " + stripChartFromAssistant(m.text || "")
        );
        lines.push("");
      }
    }
    downloadTextFile(lines.join("\n"), "office-transcript-" + Date.now() + ".txt", "text/plain;charset=utf-8");
  }

  function exportTranscriptJson() {
    const payload = {
      exported_at: nowIso(),
      messages: messageHistory,
    };
    downloadTextFile(
      JSON.stringify(payload, null, 2),
      "office-transcript-" + Date.now() + ".json",
      "application/json;charset=utf-8"
    );
  }

  function exportTranscriptCsv() {
    const rows = [];
    rows.push([
      "turn",
      "timestamp_iso",
      "requested_routing_id",
      "requested_routing_label",
      "responding_agent_id",
      "assistant_title",
      "user_text",
      "assistant_text",
    ]);
    let turn = 0;
    for (let i = 0; i < messageHistory.length; i++) {
      const u = messageHistory[i];
      const a = messageHistory[i + 1];
      if (!u || u.role !== "user") continue;
      if (!a || a.role !== "assistant") {
        turn += 1;
        rows.push([
          String(turn),
          u.ts || "",
          u.routingId || "",
          u.routingLabel || "",
          "",
          "",
          u.text || "",
          "",
        ]);
        continue;
      }
      turn += 1;
      rows.push([
        String(turn),
        u.ts || "",
        u.routingId || "",
        u.routingLabel || "",
        a.respondingAgentId != null ? a.respondingAgentId : "",
        a.assistantTitle || assistantTitleFromEntry(a),
        u.text || "",
        stripChartFromAssistant(a.text || ""),
      ]);
      i += 1;
    }
    const body = rows
      .map(function (r) {
        return r.map(csvEscapeCell).join(",");
      })
      .join("\r\n");
    downloadTextFile(body, "office-transcript-" + Date.now() + ".csv", "text/csv;charset=utf-8");
  }

  function clearHistory() {
    if (
      messageHistory.length &&
      typeof window !== "undefined" &&
      window.confirm &&
      !window.confirm("Clear all chat history in this browser?")
    ) {
      return;
    }
    messageHistory = [];
    try {
      localStorage.removeItem(HISTORY_KEY);
    } catch (e) {}
    log.innerHTML = "";
  }

  function setStatus(msg) {
    statusEl.textContent = msg || "";
  }

  function setupPriorityAgentCards() {
    const cards = document.querySelectorAll("[data-priority-agent]");
    if (!agentChoiceEl || !cards.length) return;
    cards.forEach(function (card) {
      const agent = card.getAttribute("data-priority-agent");
      if (!agent) return;
      function activate() {
        const ok = Array.from(agentChoiceEl.options).some(function (o) {
          return o.value === agent;
        });
        if (!ok) {
          dbg("[chat] priority card: unknown agent id", agent);
          return;
        }
        agentChoiceEl.value = agent;
        const assistant = document.getElementById("assistant");
        if (assistant) {
          assistant.scrollIntoView({ behavior: "smooth", block: "start" });
        }
        if (input) {
          input.focus({ preventScroll: true });
        }
      }
      card.addEventListener("click", activate);
      card.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          activate();
        }
      });
    });
  }

  loadAgentOptions().then(function () {
    loadHistory();
    if (messageHistory.length) {
      renderLogFromHistory();
    }
  });
  setupPriorityAgentCards();

  if (exportTxtBtn) exportTxtBtn.addEventListener("click", exportTranscriptTxt);
  if (exportJsonBtn) exportJsonBtn.addEventListener("click", exportTranscriptJson);
  if (exportCsvBtn) exportCsvBtn.addEventListener("click", exportTranscriptCsv);
  if (clearBtn) clearBtn.addEventListener("click", clearHistory);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = (input.value || "").trim();
    if (!text) return;

    const routingId = agentChoiceEl && agentChoiceEl.value ? agentChoiceEl.value : "auto";
    const routingLabel = getRoutingLabel(routingId);

    appendUserMessage(text, routingId, routingLabel);
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
          agent_choice: routingId,
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
      appendAssistantMessage(data.reply || "", {
        routingId: routingId,
        routingLabel: routingLabel,
        respondingAgentId: data.responding_agent != null ? data.responding_agent : null,
        assistantTitle: data.assistant_title || "Office Assistant",
      });
      autoDownloadOfficeDocument(
        text,
        data.reply || "",
        data.assistant_title || "Office Assistant",
        routingLabel,
        data.responding_agent != null ? data.responding_agent : null
      );
    } catch (err) {
      const hint =
        "Start the API: uvicorn web_server:app --reload --host 127.0.0.1 --port 8000. " +
        "Then open the site at http://127.0.0.1:8000 (same server serves the page and /api/chat). " +
        "If you use Live Server on another port, set <meta name=\"chat-api-base\" content=\"http://127.0.0.1:8000\"> in index.html.";
      appendAssistantMessage(hint + " — " + String(err.message || err), {
        routingId: routingId,
        routingLabel: routingLabel,
        respondingAgentId: "root_agent",
        assistantTitle: "Office Assistant",
      });
    } finally {
      setStatus("");
      form.querySelector("button[type=submit]").disabled = false;
    }
  });
})();
