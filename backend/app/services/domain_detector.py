import logging
from typing import List, Dict, Any
from app.schemas.scenario import Scenario, DetectedDomain
from app.services.llm_service import llm_service

logger = logging.getLogger("ai_parallel_universe.domain_detector")

SUPPORTED_DOMAINS = {
    "automotive": {
        "display_name": "Automotive & Technology",
        "description": "Technology adoption, automotive industry, technological disruption, manufacturing, innovation, infrastructure, technology transition.",
    },
    "energy": {
        "display_name": "Energy",
        "description": "Energy demand, energy supply, electricity, fuel, infrastructure, energy transition, energy security.",
    },
    "environment": {
        "display_name": "Environment",
        "description": "Emissions, pollution, climate, environmental impact, resource consumption, ecological effects.",
    },
    "economy": {
        "display_name": "Economy",
        "description": "Economic growth, investment, costs, prices, markets, government finances, business impact.",
    },
    "employment": {
        "display_name": "Employment & Workforce",
        "description": "Jobs, unemployment, workforce transition, skills, labor demand, occupational changes.",
    },
}

SYSTEM_PROMPT = """
You are a Domain Detection Expert for a multi-domain decision intelligence platform.
Your task is to evaluate a hypothetical scenario against EXACTLY FIVE supported domains:
1. automotive: Automotive & Technology (technology adoption, auto industry, innovation, manufacturing, transition)
2. energy: Energy (demand, supply, grid, fuel, infrastructure, security)
3. environment: Environment (emissions, pollution, climate, ecology, resources)
4. economy: Economy (growth, investment, costs, prices, markets, fiscal)
5. employment: Employment & Workforce (jobs, unemployment, labor, skills)

Return a JSON object containing a "domains" list where EACH domain item has:
- "name": string (one of: automotive, energy, environment, economy, employment)
- "display_name": string
- "relevance": float between 0.0 and 1.0
- "reason": string explaining relevance to scenario

Do NOT include any unsupported domains. Score relevance accurately (0.0 to 1.0).
"""


async def detect_domains(scenario: Scenario, threshold: float = 0.50) -> List[DetectedDomain]:
    """
    Dynamically assesses the relevance of supported domains for a given scenario.
    Returns sorted list of DetectedDomain objects meeting relevance threshold.
    """
    user_prompt = f"""Scenario: {scenario.original_text}
Subject: {scenario.subject}
Action: {scenario.action}
Entities: {', '.join(scenario.affected_entities)}

Evaluate domain relevance for automotive, energy, environment, economy, employment."""

    llm_result = await llm_service.generate_json(SYSTEM_PROMPT, user_prompt)

    if llm_result and "domains" in llm_result:
        try:
            detected_list = []
            for d in llm_result["domains"]:
                d_name = d.get("name", "").lower()
                if d_name in SUPPORTED_DOMAINS:
                    display_name = SUPPORTED_DOMAINS[d_name]["display_name"]
                    rel = max(0.0, min(1.0, float(d.get("relevance", 0.0))))
                    reason = d.get("reason", "Relevant to scenario context.")
                    detected_list.append(DetectedDomain(
                        name=d_name,
                        display_name=display_name,
                        relevance=rel,
                        reason=reason
                    ))
            
            # Sort descending by relevance
            detected_list.sort(key=lambda x: x.relevance, reverse=True)
            filtered = [d for d in detected_list if d.relevance >= threshold]
            if not filtered and detected_list:
                filtered = [detected_list[0]] # Return top domain if none exceed threshold
            
            if filtered:
                return filtered
        except Exception as e:
            logger.warning(f"Error processing LLM domain detection: {e}")

    # Fallback / Mock domain detector
    return _detect_domains_mock(scenario, threshold)


def _detect_domains_mock(scenario: Scenario, threshold: float = 0.50) -> List[DetectedDomain]:
    text = (scenario.original_text + " " + scenario.subject + " " + scenario.action + " " + " ".join(scenario.affected_entities)).lower()

    scores: Dict[str, Dict[str, Any]] = {
        "automotive": {"rel": 0.1, "reason": "Low direct automotive or technological impact."},
        "energy": {"rel": 0.1, "reason": "Minimal direct energy sector interaction."},
        "environment": {"rel": 0.1, "reason": "Secondary environmental impact."},
        "economy": {"rel": 0.1, "reason": "General macro-economic environment."},
        "employment": {"rel": 0.1, "reason": "Indirect labor market effect."},
    }

    # Car ban / Vehicle policy scenario
    if any(k in text for k in ["petrol", "diesel", "car", "vehicle", "auto", "ev"]):
        scores["automotive"] = {"rel": 0.96, "reason": "The policy directly alters the automotive market, manufacturing, and technological transition."}
        scores["energy"] = {"rel": 0.88, "reason": "Massive shift expected from fossil fuels to electricity and renewable grid power."}
        scores["environment"] = {"rel": 0.82, "reason": "Significant reduction in vehicular carbon emissions and urban air pollution."}
        scores["economy"] = {"rel": 0.74, "reason": "Substantial economic impact on automotive capital investments and oil import balance."}
        scores["employment"] = {"rel": 0.63, "reason": "Workforce restructuring across traditional auto manufacturing, mechanics, and EV tech."}

    # Interest rates / Monetary policy scenario
    elif any(k in text for k in ["interest rate", "central bank", "monetary", "inflation", "rate hike"]):
        scores["economy"] = {"rel": 0.95, "reason": "Directly influences borrowing costs, consumer spending, corporate investment, and economic growth."}
        scores["employment"] = {"rel": 0.78, "reason": "Higher interest rates typically slow hiring, business expansion, and labor demand."}
        scores["automotive"] = {"rel": 0.35, "reason": "Higher financing rates affect auto sales marginally."}
        scores["energy"] = {"rel": 0.20, "reason": "Indirect cost impact on energy infrastructure capital financing."}
        scores["environment"] = {"rel": 0.15, "reason": "Negligible direct environmental correlation."}

    # AI / Workforce Automation scenario
    elif any(k in text for k in ["ai", "automate", "automation", "customer service", "jobs", "workforce"]):
        scores["employment"] = {"rel": 0.95, "reason": "Direct technological displacement and skill transition across customer support occupations."}
        scores["automotive"] = {"rel": 0.85, "reason": "High technology adoption and enterprise AI software disruption."}
        scores["economy"] = {"rel": 0.72, "reason": "Productivity gains balanced against potential short-term wage and consumer spending compression."}
        scores["energy"] = {"rel": 0.25, "reason": "Increased data center power consumption for AI infrastructure."}
        scores["environment"] = {"rel": 0.15, "reason": "Minor indirect environmental footprint from computing hardware."}

    # Drought / Agricultural / Environmental disruption scenario
    elif any(k in text for k in ["drought", "agricultural", "crop", "water", "climate", "pollution"]):
        scores["environment"] = {"rel": 0.95, "reason": "Severe ecological and water resource depletion impacting regional climate stability."}
        scores["economy"] = {"rel": 0.85, "reason": "Food supply contraction driving inflation, agricultural revenue loss, and fiscal strain."}
        scores["energy"] = {"rel": 0.55, "reason": "Hydroelectric power generation capacity reduced during extended droughts."}
        scores["employment"] = {"rel": 0.50, "reason": "Agricultural labor displacement and rural economic migration."}
        scores["automotive"] = {"rel": 0.15, "reason": "Minimal direct relation to automotive sector."}

    else:
        # General scenario fallback scoring
        scores["economy"] = {"rel": 0.80, "reason": "Broad economic implications across affected sectors."}
        scores["employment"] = {"rel": 0.60, "reason": "Potential impacts on labor demand and industry workforce."}

    results = []
    for dom_name, info in SUPPORTED_DOMAINS.items():
        rel = scores[dom_name]["rel"]
        reason = scores[dom_name]["reason"]
        results.append(DetectedDomain(
            name=dom_name,
            display_name=info["display_name"],
            relevance=rel,
            reason=reason
        ))

    results.sort(key=lambda x: x.relevance, reverse=True)
    filtered = [r for r in results if r.relevance >= threshold]
    return filtered if filtered else [results[0]]
