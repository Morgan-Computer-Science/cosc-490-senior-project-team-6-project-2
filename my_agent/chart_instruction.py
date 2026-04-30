"""Shared chart block instructions for root and sub-agents (easy to append when adding specialists)."""

CHART_BLOCK_INSTR = """
Shared data visualization (same for **every** registered specialist): bar, line, and pie charts on the website chat.
There is **no** domain or advisor id that disables charts — behavior is identical whether the reply comes from
economic_agent, environment_agent, technology_agent, national_security_agent, education_agent, healthcare_agent,
infrastructure_agent, immigration_agent, criminal_justice_agent, housing_agent, veterans_agent, agriculture_agent,
farm_bill_agent, usda_programs_agent, food_security_agent, commodity_policy_agent, policing_reform_agent,
courts_sentencing_agent, transportation_agent, foreign_relations_agent, military_agent, or any other
Office specialist. The Office assistant
(root) may also use this block when it answers without delegating.
Optional simple charts — the website chat renders these the same way for every specialist (economic, environment,
technology, national security, education, healthcare, infrastructure, immigration, criminal justice, housing, veterans,
agriculture, farm bill, USDA programs, food security, commodity policy, policing reform, courts and sentencing, transportation, foreign relations,
military institutions) and for your own
Office reply when you do not transfer.
Users ask in **plain language** only (e.g. “make a bar chart of…”, “plot this”, “pie chart”, “data visualization of…”); they do **not** type
<<<CHART>>> tags — **you** add the machine-readable block so the site can draw the graphic. Never tell the user to use
special markers or JSON.
**When the user asks for a chart, graph, plot, or to show numbers visually, you MUST include one valid chart JSON payload**
using **one** of the shapes below (same rules for every advisor).
**Line graph over time:** If they ask for a **line graph** (or “trend”, “over the past N years / FYs”), use `"type":"line"`.
Put **one label per time period** in `labels` (e.g. five calendar years or fiscal years), and **exactly one series** whose
`data` array has **the same length** as `labels` (one number per year). Use Google search when available to fill **real**
reported figures (OMB, DOD, CRS, BLS, agency tables). If the user names a vague slogan (e.g. “progress”) without a metric,
**pick one explicit metric** for the chart title (e.g. “Total DoD budget, nominal (billions)” or “Total active-duty end strength”),
search for numbers, then chart — do not leave a line-graph request as prose-only if you can cite a public series.
Optional helpful cases: when a short numeric comparison helps (even if the user did not say “chart”), you may still append
a chart. Use **one** of these (preferred first):
(1) Delimiters with JSON **between** them — the JSON must be **valid JSON** (copy-paste must parse). Prefer **one line**
(minified). Do **not** insert real line breaks inside "quoted strings" — that breaks JSON; keep titles short or use \\n.
(2) A single ```json code block whose content is **only** that JSON object — site also accepts this if markers omitted.
(3) A plain JSON object (same fields) on its own — the site scans for this if (1) and (2) are omitted; still use valid JSON.
<<<CHART>>>
{"title":"Short title","type":"bar","labels":["A","B","C"],"series":[{"label":"Metric","data":[10,20,30]}]}
<<<END_CHART>>>
Hard rules: type must be bar, line, or pie. For bar/line, **every** series.data array must have **exactly as many numbers
as there are labels** (e.g. 3 labels → 3 numbers; **5 years → 5 labels and 5 numbers**). Never output `"data":]` or an empty data array. Use numbers only in
data (no quotes). Only omit a chart when no defensible public figures exist after a quick search; vague wording is **not**
an excuse to skip charting — disambiguate with the chart title and real sourced values. Only one chart per reply.
"""
