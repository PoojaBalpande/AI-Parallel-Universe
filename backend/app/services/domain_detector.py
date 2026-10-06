import logging
from typing import Any, Dict, List

from app.schemas.scenario import Scenario, DetectedDomain
from app.services.llm_service import llm_service, LLMServiceError


logger = logging.getLogger("ai_parallel_universe.domain_detector")


SUPPORTED_DOMAINS = {
    "automotive": {
        "display_name": "Automotive & Technology",
        "description": (
            "Technology adoption, automotive industry, technological "
            "disruption, manufacturing, innovation, infrastructure, "
            "technology transition."
        ),
    },
    "energy": {
        "display_name": "Energy",
        "description": (
            "Energy demand, energy supply, electricity, fuel, "
            "infrastructure, energy transition, energy security."
        ),
    },
    "environment": {
        "display_name": "Environment",
        "description": (
            "Emissions, pollution, climate, environmental impact, "
            "resource consumption, ecological effects."
        ),
    },
    "economy": {
        "display_name": "Economy",
        "description": (
            "Economic growth, investment, costs, prices, markets, "
            "government finances, business impact."
        ),
    },
    "employment": {
        "display_name": "Employment & Workforce",
        "description": (
            "Jobs, unemployment, workforce transition, skills, "
            "labor demand, occupational changes."
        ),
    },
}


SYSTEM_PROMPT = """
You are a Domain Detection Expert for a multi-domain decision intelligence platform.

Your task is to evaluate a hypothetical scenario against EXACTLY FIVE supported domains:

1. automotive: Automotive & Technology
   Technology adoption, auto industry, innovation, manufacturing, transition.

2. energy: Energy
   Demand, supply, grid, fuel, infrastructure, energy security.

3. environment: Environment
   Emissions, pollution, climate, ecology, resources.

4. economy: Economy
   Growth, investment, costs, prices, markets, fiscal impact.

5. employment: Employment & Workforce
   Jobs, unemployment, labor, skills, workforce transition.

Return a JSON object containing a "domains" list.

Each domain item must contain:

{
    "name": "string",
    "display_name": "string",
    "relevance": 0.0,
    "reason": "string"
}

Rules:

- "name" must be one of:
  automotive, energy, environment, economy, employment

- "display_name" must correspond to the supported domain.

- "relevance" must be a float between 0.0 and 1.0.

- "reason" must explain why the domain is relevant or not relevant
  to the scenario.

- Do NOT include unsupported domains.

- Evaluate all five supported domains.

- Score relevance accurately based on the actual scenario.
"""


async def detect_domains(
    scenario: Scenario,
    threshold: float = 0.50,
) -> List[DetectedDomain]:
    """
    Dynamically assesses the relevance of supported domains
    for a given scenario.

    Only domains meeting the relevance threshold are returned.

    Boundary behavior:
        0.49 -> excluded
        0.50 -> included
        0.51 -> included
    """

    # ---------------------------------------------------------
    # MOCK MODE
    # ---------------------------------------------------------
    if llm_service.is_mock_mode:
        return _detect_domains_mock(scenario, threshold)

    # ---------------------------------------------------------
    # LIVE MODE
    # ---------------------------------------------------------
    user_prompt = f"""
Scenario: {scenario.original_text}

Subject: {scenario.subject}

Action: {scenario.action}

Entities: {', '.join(scenario.affected_entities)}

Evaluate domain relevance for:
automotive, energy, environment, economy, employment.

Return relevance scores between 0.0 and 1.0.
"""

    llm_result = await llm_service.generate_json(
        SYSTEM_PROMPT,
        user_prompt,
    )

    try:
        if not llm_result:
            raise ValueError(
                "LLM returned an empty domain detection response."
            )

        detected_list: List[DetectedDomain] = []

        # -----------------------------------------------------
        # PROCESS LLM DOMAIN RESULTS
        # -----------------------------------------------------
        for domain_data in llm_result.get("domains", []):

            domain_name = domain_data.get("name", "").lower().strip()

            # Ignore unsupported domains
            if domain_name not in SUPPORTED_DOMAINS:
                logger.warning(
                    "Ignoring unsupported domain returned by LLM: %s",
                    domain_name,
                )
                continue

            display_name = SUPPORTED_DOMAINS[domain_name][
                "display_name"
            ]

            # Clamp relevance between 0.0 and 1.0
            relevance = max(
                0.0,
                min(
                    1.0,
                    float(domain_data.get("relevance", 0.0)),
                ),
            )

            reason = domain_data.get(
                "reason",
                "Relevant to scenario context.",
            )

            detected_list.append(
                DetectedDomain(
                    name=domain_name,
                    display_name=display_name,
                    relevance=relevance,
                    reason=reason,
                )
            )

        # -----------------------------------------------------
        # SORT BY RELEVANCE
        # -----------------------------------------------------
        detected_list.sort(
            key=lambda domain: domain.relevance,
            reverse=True,
        )

        # -----------------------------------------------------
        # APPLY EXACT THRESHOLD
        # -----------------------------------------------------
        filtered = [
            domain
            for domain in detected_list
            if domain.relevance >= threshold
        ]

        # -----------------------------------------------------
        # IMPORTANT:
        # Do NOT force-select the highest domain when none
        # reaches the threshold.
        #
        # Therefore:
        # 0.49 -> excluded
        # 0.50 -> included
        # 0.51 -> included
        # -----------------------------------------------------
        if filtered:
            return filtered

        raise ValueError(
            f"No domains met the relevance threshold of {threshold}."
        )

    except LLMServiceError:
        # Preserve the original LLM service failure.
        raise

    except Exception as e:
        logger.error(
            "Error processing LLM domain detection: %s",
            e,
        )

        raise LLMServiceError(
            f"Failed to process LLM domain detection: {e}"
        ) from e


def _detect_domains_mock(
    scenario: Scenario,
    threshold: float = 0.50,
) -> List[DetectedDomain]:
    """
    Deterministic mock domain detection used only when
    LLM_MOCK_MODE=true.
    """

    text = (
        scenario.original_text
        + " "
        + scenario.subject
        + " "
        + scenario.action
        + " "
        + " ".join(scenario.affected_entities)
    ).lower()

    scores: Dict[str, Dict[str, Any]] = {
        "automotive": {
            "rel": 0.1,
            "reason": (
                "Low direct automotive or technological impact."
            ),
        },
        "energy": {
            "rel": 0.1,
            "reason": (
                "Minimal direct energy sector interaction."
            ),
        },
        "environment": {
            "rel": 0.1,
            "reason": (
                "Secondary environmental impact."
            ),
        },
        "economy": {
            "rel": 0.1,
            "reason": (
                "General macro-economic environment."
            ),
        },
        "employment": {
            "rel": 0.1,
            "reason": (
                "Indirect labor market effect."
            ),
        },
    }

    # ---------------------------------------------------------
    # CAR BAN / VEHICLE POLICY
    # ---------------------------------------------------------
    if any(
        keyword in text
        for keyword in [
            "petrol",
            "diesel",
            "car",
            "vehicle",
            "auto",
            "ev",
        ]
    ):
        scores["automotive"] = {
            "rel": 0.96,
            "reason": (
                "The policy directly alters the automotive market, "
                "manufacturing, and technological transition."
            ),
        }

        scores["energy"] = {
            "rel": 0.88,
            "reason": (
                "Massive shift expected from fossil fuels "
                "to electricity and renewable grid power."
            ),
        }

        scores["environment"] = {
            "rel": 0.82,
            "reason": (
                "Significant reduction in vehicular carbon "
                "emissions and urban air pollution."
            ),
        }

        scores["economy"] = {
            "rel": 0.74,
            "reason": (
                "Substantial economic impact on automotive "
                "capital investments and oil import balance."
            ),
        }

        scores["employment"] = {
            "rel": 0.63,
            "reason": (
                "Workforce restructuring across traditional "
                "auto manufacturing, mechanics, and EV technology."
            ),
        }

    # ---------------------------------------------------------
    # INTEREST RATES / MONETARY POLICY
    # ---------------------------------------------------------
    elif any(
        keyword in text
        for keyword in [
            "interest rate",
            "central bank",
            "monetary",
            "inflation",
            "rate hike",
        ]
    ):
        scores["economy"] = {
            "rel": 0.95,
            "reason": (
                "Directly influences borrowing costs, consumer "
                "spending, corporate investment, and economic growth."
            ),
        }

        scores["employment"] = {
            "rel": 0.78,
            "reason": (
                "Higher interest rates typically slow hiring, "
                "business expansion, and labor demand."
            ),
        }

        scores["automotive"] = {
            "rel": 0.35,
            "reason": (
                "Higher financing rates affect auto sales marginally."
            ),
        }

        scores["energy"] = {
            "rel": 0.20,
            "reason": (
                "Indirect cost impact on energy infrastructure "
                "capital financing."
            ),
        }

        scores["environment"] = {
            "rel": 0.15,
            "reason": (
                "Negligible direct environmental correlation."
            ),
        }

    # ---------------------------------------------------------
    # AI / WORKFORCE AUTOMATION
    # ---------------------------------------------------------
    elif any(
        keyword in text
        for keyword in [
            "ai",
            "automate",
            "automation",
            "customer service",
            "jobs",
            "workforce",
        ]
    ):
        scores["employment"] = {
            "rel": 0.95,
            "reason": (
                "Direct technological displacement and skill "
                "transition across customer support occupations."
            ),
        }

        scores["automotive"] = {
            "rel": 0.85,
            "reason": (
                "High technology adoption and enterprise AI "
                "software disruption."
            ),
        }

        scores["economy"] = {
            "rel": 0.72,
            "reason": (
                "Productivity gains balanced against potential "
                "short-term wage and consumer spending compression."
            ),
        }

        scores["energy"] = {
            "rel": 0.25,
            "reason": (
                "Increased data center power consumption "
                "for AI infrastructure."
            ),
        }

        scores["environment"] = {
            "rel": 0.15,
            "reason": (
                "Minor indirect environmental footprint "
                "from computing hardware."
            ),
        }

    # ---------------------------------------------------------
    # DROUGHT / AGRICULTURAL / ENVIRONMENTAL DISRUPTION
    # ---------------------------------------------------------
    elif any(
        keyword in text
        for keyword in [
            "drought",
            "agricultural",
            "crop",
            "water",
            "climate",
            "pollution",
        ]
    ):
        scores["environment"] = {
            "rel": 0.95,
            "reason": (
                "Severe ecological and water resource depletion "
                "impacting regional climate stability."
            ),
        }

        scores["economy"] = {
            "rel": 0.85,
            "reason": (
                "Food supply contraction driving inflation, "
                "agricultural revenue loss, and fiscal strain."
            ),
        }

        scores["energy"] = {
            "rel": 0.55,
            "reason": (
                "Hydroelectric power generation capacity reduced "
                "during extended droughts."
            ),
        }

        scores["employment"] = {
            "rel": 0.50,
            "reason": (
                "Agricultural labor displacement and rural "
                "economic migration."
            ),
        }

        scores["automotive"] = {
            "rel": 0.15,
            "reason": (
                "Minimal direct relation to automotive sector."
            ),
        }

    # ---------------------------------------------------------
    # GENERAL SCENARIO FALLBACK
    # ---------------------------------------------------------
    else:
        scores["economy"] = {
            "rel": 0.80,
            "reason": (
                "Broad economic implications across "
                "affected sectors."
            ),
        }

        scores["employment"] = {
            "rel": 0.60,
            "reason": (
                "Potential impacts on labor demand and "
                "industry workforce."
            ),
        }

    # ---------------------------------------------------------
    # BUILD MOCK RESULTS
    # ---------------------------------------------------------
    results: List[DetectedDomain] = []

    for domain_name, domain_info in SUPPORTED_DOMAINS.items():

        relevance = scores[domain_name]["rel"]
        reason = scores[domain_name]["reason"]

        results.append(
            DetectedDomain(
                name=domain_name,
                display_name=domain_info["display_name"],
                relevance=relevance,
                reason=reason,
            )
        )

    # Sort by relevance
    results.sort(
        key=lambda domain: domain.relevance,
        reverse=True,
    )

    # Apply the SAME threshold rule in mock mode
    filtered = [
        domain
        for domain in results
        if domain.relevance >= threshold
    ]

    if filtered:
        return filtered

    raise ValueError(
        f"No domains met the relevance threshold of {threshold}."
    )