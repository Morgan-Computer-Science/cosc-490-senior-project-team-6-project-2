"""UI/API options for chat routing (must stay aligned with web_server routing prefixes)."""

# Display names for ADK Event.author (agent `name=`). Add entries when you register new sub_agents.
RESPONDING_AGENT_TITLES: dict[str, str] = {
    "root_agent": "Office Assistant",
    "agriculture_agent": "Agriculture Assistant",
    "farm_bill_agent": "Agriculture — Farm Bill",
    "usda_programs_agent": "Agriculture — USDA programs",
    "food_security_agent": "Agriculture — Food security",
    "commodity_policy_agent": "Agriculture — Commodity policy",
    "criminal_justice_agent": "Criminal Justice Assistant",
    "policing_reform_agent": "Justice — Policing reform",
    "courts_sentencing_agent": "Justice — Courts & sentencing",
    "economic_agent": "Economic Assistant",
    "education_agent": "Education Assistant",
    "k12_agent": "Education — K-12",
    "higher_education_agent": "Education — Higher education",
    "student_aid_agent": "Education — Student aid",
    "workforce_pathways_agent": "Education — Workforce pathways",
    "environment_agent": "Environmental Sustainability Assistant",
    "climate_clean_energy_agent": "Environment — Climate and clean energy",
    "conservation_agent": "Environment — Conservation",
    "epa_policy_agent": "Environment — EPA policy",
    "public_lands_agent": "Environment — Public lands",
    "foreign_relations_agent": "Foreign Relations Assistant",
    "diplomacy_agent": "Foreign Relations — Diplomacy",
    "treaties_agent": "Foreign Relations — Treaties",
    "alliances_agent": "Foreign Relations — Alliances",
    "regional_strategy_agent": "Foreign Relations — Regional strategy",
    "healthcare_agent": "Healthcare Assistant",
    "access_affordability_agent": "Healthcare — Access and affordability",
    "medicare_medicaid_agent": "Healthcare — Medicare/Medicaid",
    "public_health_agent": "Healthcare — Public health",
    "insurance_markets_agent": "Healthcare — Insurance markets",
    "housing_agent": "Housing & Affordability Assistant",
    "housing_supply_agent": "Housing — Supply",
    "housing_affordability_agent": "Housing — Affordability",
    "fair_housing_agent": "Housing — Fair housing",
    "rental_markets_agent": "Housing — Rental markets",
    "homelessness_agent": "Housing — Homelessness",
    "immigration_agent": "Immigration Assistant",
    "border_policy_agent": "Immigration — Border policy",
    "legal_immigration_agent": "Immigration — Legal immigration",
    "immigration_pathways_agent": "Immigration — Pathways",
    "humanitarian_processing_agent": "Immigration — Humanitarian processing",
    "infrastructure_agent": "Infrastructure Assistant",
    "water_systems_agent": "Infrastructure — Water systems",
    "grid_resilience_agent": "Infrastructure — Grid resilience",
    "public_works_agent": "Infrastructure — Public works",
    "broadband_agent": "Infrastructure — Broadband",
    "military_agent": "Military Institutions Assistant",
    "national_security_agent": "National Security Assistant",
    "defense_strategy_agent": "National Security — Defense strategy",
    "deterrence_agent": "National Security — Deterrence",
    "homeland_security_agent": "National Security — Homeland security",
    "military_affairs_agent": "National Security — Military affairs",
    "technology_agent": "Technological Advancement Assistant",
    "ai_innovation_agent": "Technology — AI and innovation",
    "cybersecurity_agent": "Technology — Cybersecurity",
    "rd_agent": "Technology — R&D",
    "semiconductors_agent": "Technology — Semiconductors",
    "digital_competitiveness_agent": "Technology — Digital competitiveness",
    "transportation_agent": "Transportation Assistant",
    "highways_agent": "Transportation — Highways",
    "transit_agent": "Transportation — Transit",
    "rail_agent": "Transportation — Rail",
    "aviation_agent": "Transportation — Aviation",
    "maritime_mobility_agent": "Transportation — Maritime mobility",
    "dot_programs_agent": "Transportation — DOT programs",
    "veterans_agent": "Veterans & Military Families Assistant",
    "va_benefits_agent": "Veterans — VA benefits",
    "veteran_education_agent": "Veterans — Education",
    "veteran_employment_agent": "Veterans — Employment",
    "veteran_housing_supports_agent": "Veterans — Housing supports",
    "military_families_agent": "Veterans — Military families",
}


def assistant_display_title(author_agent_id: str | None) -> str:
    """Map ADK `event.author` to a user-visible assistant name. Extend RESPONDING_AGENT_TITLES for new agents."""
    if not author_agent_id:
        return RESPONDING_AGENT_TITLES["root_agent"]
    aid = str(author_agent_id).strip()
    if aid.lower() == "user":
        return RESPONDING_AGENT_TITLES["root_agent"]
    for key, title in RESPONDING_AGENT_TITLES.items():
        if key.lower() == aid.lower():
            return title
    return aid.replace("_", " ").title()


CHAT_AGENT_OPTIONS: list[dict[str, str]] = [
    {
        "id": "auto",
        "label": "Auto (Office decides)",
        "description": (
            "The Office routes the question; specialists are used when the topic clearly fits their role."
        ),
    },
    {
        "id": "root_agent",
        "label": "General assistant only",
        "description": (
            "General answers on presidential leadership and policy without delegating to domain advisors."
        ),
    },
    {
        "id": "agriculture_agent",
        "label": "Agriculture & rural economies",
        "description": (
            "Coordinator: routes Farm Bill, USDA programs, food security, and commodity policy. Pick a delegate when you want one specialist."
        ),
    },
    {
        "id": "farm_bill_agent",
        "label": "Agriculture — Farm Bill",
        "description": (
            "Sections and deadlines, amendments, current vs prior bill language, presidential briefs, budget/food/rural impacts."
        ),
    },
    {
        "id": "usda_programs_agent",
        "label": "Agriculture — USDA programs",
        "description": (
            "Program data, expansion/reform, subsidy usage and outcomes, agency checklists, executive memos on performance."
        ),
    },
    {
        "id": "food_security_agent",
        "label": "Agriculture — Food security",
        "description": (
            "Hunger and SNAP/school-meal indicators, hotspot-style assessment, emergency assistance, crisis memos, escalation when hardship worsens."
        ),
    },
    {
        "id": "commodity_policy_agent",
        "label": "Agriculture — Commodity policy",
        "description": (
            "Prices and supply shocks; tariffs/drought/subsidy scenarios; stabilization options; crop/livestock briefings; note economic/foreign-relations coordination when needed."
        ),
    },
    {
        "id": "criminal_justice_agent",
        "label": "Criminal justice",
        "description": (
            "Coordinator: routes policing reform vs courts/sentencing. Pick a delegate for a focused specialist — not case advice."
        ),
    },
    {
        "id": "policing_reform_agent",
        "label": "Justice — Policing reform",
        "description": (
            "Policing bills and department reforms, best practices, executive guidance, use-of-force/accountability metrics, civil rights risks."
        ),
    },
    {
        "id": "courts_sentencing_agent",
        "label": "Justice — Courts & sentencing",
        "description": (
            "Backlogs and disparities, sentencing reform, justice-impact summaries, state/federal comparisons, urgent judicial bottlenecks."
        ),
    },
    {
        "id": "economic_agent",
        "label": "Economic advisor",
        "description": "Macroeconomy, jobs, inflation, trade, fiscal policy, budgets, and related economic topics.",
    },
    {
        "id": "education_agent",
        "label": "Education",
        "description": (
            "Coordinator: routes K-12, higher education, student aid, and workforce pathways. Pick a delegate for focused analysis."
        ),
    },
    {
        "id": "k12_agent",
        "label": "Education — K-12",
        "description": (
            "School performance, attendance, literacy, district funding gaps, and student wellbeing equity risks."
        ),
    },
    {
        "id": "higher_education_agent",
        "label": "Education — Higher education",
        "description": (
            "College affordability, enrollment/completion, institutional reforms, and research competitiveness."
        ),
    },
    {
        "id": "student_aid_agent",
        "label": "Education — Student aid",
        "description": (
            "Pell and loans, repayment and debt burden, aid reform options, and implementation/fraud risk signals."
        ),
    },
    {
        "id": "workforce_pathways_agent",
        "label": "Education — Workforce pathways",
        "description": (
            "Apprenticeships, certifications, pipeline and training gaps, and education-to-employment policy planning."
        ),
    },
    {
        "id": "environment_agent",
        "label": "Environmental sustainability",
        "description": (
            "Coordinator: routes climate and clean energy, conservation, EPA policy, and public lands. "
            "Pick a delegate for focused analysis."
        ),
    },
    {
        "id": "climate_clean_energy_agent",
        "label": "Environment — Climate and clean energy",
        "description": (
            "Emissions and climate-goal tracking, clean-energy deployment, reduction pathways, and investment options."
        ),
    },
    {
        "id": "conservation_agent",
        "label": "Environment — Conservation",
        "description": (
            "Biodiversity, forests, wetlands, habitat protection, preservation actions, and conservation funding usage."
        ),
    },
    {
        "id": "epa_policy_agent",
        "label": "Environment — EPA policy",
        "description": (
            "Regulations and enforcement, compliance trends, pollution summaries, and legal/implementation risk flags."
        ),
    },
    {
        "id": "public_lands_agent",
        "label": "Environment — Public lands",
        "description": (
            "Federal land-use and extraction proposals, recreation access, policy briefs, and land-use conflict alerts."
        ),
    },
    {
        "id": "foreign_relations_agent",
        "label": "Foreign relations",
        "description": (
            "Coordinator: routes diplomacy, treaties, alliances, and regional strategy. Pick a delegate for focused analysis."
        ),
    },
    {
        "id": "diplomacy_agent",
        "label": "Foreign Relations — Diplomacy",
        "description": "Country/region diplomatic developments, briefing notes, and negotiation priorities.",
    },
    {
        "id": "treaties_agent",
        "label": "Foreign Relations — Treaties",
        "description": "Treaty negotiation/compliance tracking, language comparisons, and legal/geopolitical risks.",
    },
    {
        "id": "alliances_agent",
        "label": "Foreign Relations — Alliances",
        "description": "Alliance commitments, burden-sharing, coordination steps, and strain/opportunity analysis.",
    },
    {
        "id": "regional_strategy_agent",
        "label": "Foreign Relations — Regional strategy",
        "description": "Region-level risk profiles, tailored strategy options, and crisis monitoring.",
    },
    {
        "id": "healthcare_agent",
        "label": "Healthcare",
        "description": (
            "Coordinator: routes access/affordability, Medicare/Medicaid, public health, and insurance markets."
        ),
    },
    {
        "id": "access_affordability_agent",
        "label": "Healthcare — Access and affordability",
        "description": "Uninsured/provider shortage/cost tracking, coverage options, and underserved population risks.",
    },
    {
        "id": "medicare_medicaid_agent",
        "label": "Healthcare — Medicare/Medicaid",
        "description": "Reimbursement, enrollment, reform proposals, and implementation impact monitoring.",
    },
    {
        "id": "public_health_agent",
        "label": "Healthcare — Public health",
        "description": "Outbreak and preparedness monitoring, emergency alerts, and rapid response actions.",
    },
    {
        "id": "insurance_markets_agent",
        "label": "Healthcare — Insurance markets",
        "description": "Premiums/competition stability analysis, market reforms, and consumer impact modeling.",
    },
    {
        "id": "housing_agent",
        "label": "Housing & cost of living",
        "description": (
            "Coordinator: routes housing supply, affordability, fair housing, rental markets, and homelessness."
        ),
    },
    {
        "id": "housing_supply_agent",
        "label": "Housing — Supply",
        "description": "Permits, construction, zoning barriers, shortages, and supply expansion strategies.",
    },
    {
        "id": "housing_affordability_agent",
        "label": "Housing — Affordability",
        "description": "Rent burden, home prices, mortgage stress, interventions, and market-instability alerts.",
    },
    {
        "id": "fair_housing_agent",
        "label": "Housing — Fair housing",
        "description": "Discrimination/enforcement trends, civil-rights options, and equitable-access monitoring.",
    },
    {
        "id": "rental_markets_agent",
        "label": "Housing — Rental markets",
        "description": "Eviction risk, vacancy, rent growth, renter-protection options, and pressure-zone signals.",
    },
    {
        "id": "homelessness_agent",
        "label": "Housing — Homelessness",
        "description": "Shelter/unsheltered trends, service gaps, emergency interventions, and humanitarian alerts.",
    },
    {
        "id": "immigration_agent",
        "label": "Immigration",
        "description": (
            "Coordinator: routes border policy, legal immigration, pathways/status adjustment, and humanitarian processing."
        ),
    },
    {
        "id": "border_policy_agent",
        "label": "Immigration — Border policy",
        "description": "Border activity and processing-delay monitoring, resource strain analysis, and surge alerts.",
    },
    {
        "id": "legal_immigration_agent",
        "label": "Immigration — Legal immigration",
        "description": "Visa backlogs, employment and family pathways, modernization options, and workforce effects.",
    },
    {
        "id": "immigration_pathways_agent",
        "label": "Immigration — Pathways",
        "description": "Legalization/status-adjustment policy options, outcomes modeling, and legal-constraint flags.",
    },
    {
        "id": "humanitarian_processing_agent",
        "label": "Immigration — Humanitarian processing",
        "description": "Asylum/refugee/parole flow monitoring, capacity expansion options, and bottleneck alerts.",
    },
    {
        "id": "infrastructure_agent",
        "label": "Infrastructure",
        "description": "Coordinator: routes water systems, grid resilience, public works, and broadband.",
    },
    {
        "id": "water_systems_agent",
        "label": "Infrastructure — Water systems",
        "description": "Water safety/pipes/drought/wastewater monitoring, resilience planning, and contamination alerts.",
    },
    {
        "id": "grid_resilience_agent",
        "label": "Infrastructure — Grid resilience",
        "description": "Outages and vulnerabilities, grid-hardening options, resilience briefs, and threat alerts.",
    },
    {
        "id": "public_works_agent",
        "label": "Infrastructure — Public works",
        "description": "Project timeline/cost/delay tracking, prioritization, dashboards, and execution-risk flags.",
    },
    {
        "id": "broadband_agent",
        "label": "Infrastructure — Broadband",
        "description": "Access/affordability/deployment tracking, investment options, and underserved-community alerts.",
    },
    {
        "id": "military_agent",
        "label": "Military (structure & demographics)",
        "description": "Chain of command and service roles (unclassified), rank overview, public force size and demographics.",
    },
    {
        "id": "national_security_agent",
        "label": "National security",
        "description": "Coordinator: routes defense strategy, deterrence, homeland security, and military affairs.",
    },
    {
        "id": "defense_strategy_agent",
        "label": "National Security — Defense strategy",
        "description": "Posture/readiness/priority tracking, strategic defense briefs, options, and capability gaps.",
    },
    {
        "id": "deterrence_agent",
        "label": "National Security — Deterrence",
        "description": "Adversary action assessment, posture/signaling options, escalation-risk modeling, and tension alerts.",
    },
    {
        "id": "homeland_security_agent",
        "label": "National Security — Homeland security",
        "description": "Domestic threat and preparedness monitoring, protection actions, and critical-incident alerts.",
    },
    {
        "id": "military_affairs_agent",
        "label": "National Security — Military affairs",
        "description": "Personnel/procurement/readiness tracking, force management summaries, and risk flags.",
    },
    {
        "id": "technology_agent",
        "label": "Technological advancements",
        "description": "Coordinator: routes AI/innovation, cybersecurity, R&D, semiconductors, and digital competitiveness.",
    },
    {
        "id": "ai_innovation_agent",
        "label": "Technology — AI and innovation",
        "description": "Frontier AI capability/governance tracking, strategy priorities, and strategic-risk flags.",
    },
    {
        "id": "cybersecurity_agent",
        "label": "Technology — Cybersecurity",
        "description": "Threat/incident/vulnerability monitoring, defensive actions, and urgent cyber alerts.",
    },
    {
        "id": "rd_agent",
        "label": "Technology — R&D",
        "description": "Research-investment tracking, bottleneck identification, and innovation-priority memos.",
    },
    {
        "id": "semiconductors_agent",
        "label": "Technology — Semiconductors",
        "description": "Chip supply-chain/capacity/dependency monitoring and disruption-risk analysis.",
    },
    {
        "id": "digital_competitiveness_agent",
        "label": "Technology — Digital competitiveness",
        "description": "Digital-infrastructure/adoption/competition tracking and capability-gap analysis.",
    },
    {
        "id": "transportation_agent",
        "label": "Transportation",
        "description": "Coordinator: routes highways, transit, rail, aviation, maritime mobility, and DOT programs.",
    },
    {
        "id": "highways_agent",
        "label": "Transportation — Highways",
        "description": "Condition/congestion/project monitoring, repair priorities, and safety-risk flags.",
    },
    {
        "id": "transit_agent",
        "label": "Transportation — Transit",
        "description": "Ridership/safety/reliability/funding-gap tracking and service-breakdown alerts.",
    },
    {
        "id": "rail_agent",
        "label": "Transportation — Rail",
        "description": "Freight/passenger rail performance, modernization plans, and bottleneck/safety risks.",
    },
    {
        "id": "aviation_agent",
        "label": "Transportation — Aviation",
        "description": "Air traffic/congestion/safety monitoring and major disruption alerts.",
    },
    {
        "id": "maritime_mobility_agent",
        "label": "Transportation — Maritime mobility",
        "description": "Port/shipping flow monitoring, modernization options, and commerce-disruption alerts.",
    },
    {
        "id": "dot_programs_agent",
        "label": "Transportation — DOT programs",
        "description": "DOT funding/performance tracking, implementation audits, and reform options.",
    },
    {
        "id": "veterans_agent",
        "label": "Veterans & military families",
        "description": "Coordinator: routes VA benefits, veteran education/employment/housing supports, and military families.",
    },
    {
        "id": "va_benefits_agent",
        "label": "Veterans — VA benefits",
        "description": "Claims/appeals backlog monitoring, modernization options, and benefits performance memos.",
    },
    {
        "id": "veteran_education_agent",
        "label": "Veterans — Education",
        "description": "GI Bill usage/access tracking and veteran education support-policy options.",
    },
    {
        "id": "veteran_employment_agent",
        "label": "Veterans — Employment",
        "description": "Unemployment/placement/skills-transition tracking and workforce initiative planning.",
    },
    {
        "id": "veteran_housing_supports_agent",
        "label": "Veterans — Housing supports",
        "description": "Homelessness/placement/support-program tracking and targeted intervention options.",
    },
    {
        "id": "military_families_agent",
        "label": "Veterans — Military families",
        "description": "Childcare/spouse employment/relocation stress monitoring and family support gaps.",
    },
]
