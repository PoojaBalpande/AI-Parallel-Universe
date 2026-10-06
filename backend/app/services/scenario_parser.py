import re
import logging
from typing import Optional, List, Dict, Any
from app.schemas.scenario import Scenario, LocationInfo, TimeInfo
from app.services.llm_service import llm_service, LLMServiceError

logger = logging.getLogger("ai_parallel_universe.parser")


SYSTEM_PROMPT = """
You are a Scenario Parsing System for a decision intelligence engine.
Analyze the user's hypothetical scenario and decompose it into structured components.

Return JSON matching this schema:
{
  "original_text": "string",
  "scenario_type": "string",  // e.g. government_policy, economic_policy, tech_disruption, climate_event
  "subject": "string",
  "action": "string",
  "affected_entities": ["string"],
  "location": { "country": "string or null", "region": "string or null", "city": "string or null" },
  "time": { "start_year": integer or null, "end_year": integer or null, "horizon_years": integer or null },
  "magnitude": "string or null",
  "assumptions": ["string"],
  "uncertainties": ["string"]
}

RULES:
1. Do NOT mention or detect domains here.
2. Do NOT invent missing facts. If facts like country or start year are missing, leave them null and state the ambiguity in "uncertainties".
"""


async def parse_scenario(scenario_text: str) -> Scenario:
    """
    Parses natural language scenario text into a structured Scenario object.
    """
    scenario_text_clean = scenario_text.strip()

    if llm_service.is_mock_mode:
        return _parse_scenario_mock(scenario_text_clean)

    user_prompt = f"Decompose the following scenario:\n\"{scenario_text_clean}\""
    llm_result = await llm_service.generate_json(SYSTEM_PROMPT, user_prompt)

    try:
        llm_result["original_text"] = scenario_text_clean
        return Scenario(**llm_result)
    except Exception as e:
        logger.error(f"Failed to validate LLM response into Scenario schema: {e}")
        raise LLMServiceError(f"Failed to validate LLM response into Scenario schema: {e}") from e



def _parse_scenario_mock(text: str) -> Scenario:
    lower = text.lower()

    # Extract year if present
    years = [int(y) for y in re.findall(r"\b(20\d{2}|19\d{2})\b", text)]
    time_info = TimeInfo(start_year=years[0]) if years else TimeInfo()

    # Extract location if present
    location_info = LocationInfo()
    if "india" in lower:
        location_info.country = "India"
    elif "united states" in lower or "us" in lower or "usa" in lower:
        location_info.country = "United States"
    elif "china" in lower:
        location_info.country = "China"
    elif "europe" in lower or "eu" in lower:
        location_info.region = "Europe"

    # Determine type, subject, action, entities
    scenario_type = "policy_or_event"
    subject = "target sector"
    action = "implementation"
    affected_entities: List[str] = []
    assumptions: List[str] = ["Implementation proceeds as announced."]
    uncertainties: List[str] = []

    if "petrol" in lower or "diesel" in lower or "car" in lower or "auto" in lower:
        scenario_type = "government_policy"
        subject = "petrol and diesel vehicles"
        action = "ban sales"
        affected_entities = ["petrol vehicles", "diesel vehicles", "automotive manufacturers", "fuel stations"]
        assumptions.append("Alternative transport and EV infrastructure will be developed.")
    elif "interest rate" in lower or "central bank" in lower or "inflation" in lower:
        scenario_type = "economic_policy"
        subject = "interest rates"
        action = "monetary policy tightening"
        affected_entities = ["commercial banks", "borrowers", "investors", "real estate"]
        assumptions.append("Central bank maintains rate policy for the foreseeable term.")
    elif "ai" in lower or "automates" in lower or "automation" in lower:
        scenario_type = "technology_disruption"
        subject = "AI customer service automation"
        action = "workforce automation"
        affected_entities = ["customer support workers", "technology vendors", "enterprise services"]
        assumptions.append("AI capabilities continue to advance reliably.")
    elif "drought" in lower or "climate" in lower or "agriculture" in lower:
        scenario_type = "climate_event"
        subject = "agricultural production"
        action = "environmental disruption"
        affected_entities = ["farming sector", "food supply chain", "rural economies"]
        assumptions.append("Drought severity persists over multiple crop cycles.")
    else:
        subject = "specified domain"
        action = "scenario action"
        affected_entities = ["affected stakeholders", "related industries"]

    if not location_info.country and not location_info.region:
        uncertainties.append("Geographic scope is not explicitly specified in the scenario.")

    if not years:
        uncertainties.append("Timeline and starting year are unspecified.")

    return Scenario(
        original_text=text,
        scenario_type=scenario_type,
        subject=subject,
        action=action,
        affected_entities=affected_entities,
        location=location_info,
        time=time_info,
        magnitude=None,
        assumptions=assumptions,
        uncertainties=uncertainties,
    )
