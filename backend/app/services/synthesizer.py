import logging
from typing import List
from app.schemas.scenario import Scenario, DetectedDomain, ExpertAnalysis, Synthesis
from app.services.llm_service import llm_service

logger = logging.getLogger("ai_parallel_universe.synthesizer")

SYSTEM_PROMPT = """
You are the Executive Synthesizer for an AI Parallel Universe Decision Engine.
Synthesize independent domain analyses from multiple expert agents into a cohesive multi-domain executive summary.

Return JSON matching this schema:
{
  "overall_impact": "high", // "high", "medium", "low"
  "overall_summary": "Unified executive summary synthesized across all expert perspectives...",
  "key_positive_impacts": ["string"],
  "key_negative_impacts": ["string"],
  "major_risks": ["string"],
  "major_opportunities": ["string"],
  "cross_domain_effects": ["Inter-domain interactions, e.g. Energy grid stress impacting Economic investments"],
  "uncertainties": ["string"]
}
"""


async def synthesize_analyses(
    scenario: Scenario,
    domains: List[DetectedDomain],
    analyses: List[ExpertAnalysis]
) -> Synthesis:
    """
    Synthesizes independent expert domain analyses into an overarching synthesis report.
    """
    analyses_summary = ""
    for a in analyses:
        analyses_summary += f"\n--- EXPERT: {a.expert} (Domain: {a.domain}, Impact: {a.impact_level}) ---\n"
        analyses_summary += f"Summary: {a.summary}\n"
        analyses_summary += f"Positive Impacts: {', '.join(a.positive_impacts)}\n"
        analyses_summary += f"Negative Impacts: {', '.join(a.negative_impacts)}\n"
        analyses_summary += f"Opportunities: {', '.join(a.opportunities)}\n"
        analyses_summary += f"Risks: {', '.join(a.risks)}\n"

    user_prompt = f"""Scenario: {scenario.original_text}
Detected Domains: {', '.join([d.display_name for d in domains])}

Expert Analyses:
{analyses_summary}

Synthesize these independent findings into a multi-domain synthesis report."""

    llm_result = await llm_service.generate_json(SYSTEM_PROMPT, user_prompt)

    if llm_result:
        try:
            return Synthesis(**llm_result)
        except Exception as e:
            logger.warning(f"Error parsing LLM response for Synthesis: {e}")

    # Fallback / Mock synthesis logic
    return _synthesize_mock(scenario, domains, analyses)


def _synthesize_mock(scenario: Scenario, domains: List[DetectedDomain], analyses: List[ExpertAnalysis]) -> Synthesis:
    positives = []
    negatives = []
    risks = []
    opps = []
    cross_effects = []
    uncertainties = list(scenario.uncertainties)

    has_energy = any(a.domain == "energy" for a in analyses)
    has_auto = any(a.domain == "automotive" for a in analyses)
    has_econ = any(a.domain == "economy" for a in analyses)
    has_env = any(a.domain == "environment" for a in analyses)
    has_emp = any(a.domain == "employment" for a in analyses)

    for a in analyses:
        positives.extend(a.positive_impacts[:2])
        negatives.extend(a.negative_impacts[:2])
        risks.extend(a.risks[:2])
        opps.extend(a.opportunities[:2])
        uncertainties.extend(a.uncertainties[:1])

    if has_auto and has_energy:
        cross_effects.append("Surging EV adoption directly impacts power grid load management, requiring coordinated energy infrastructure investments.")
    if has_env and has_econ:
        cross_effects.append("Environmental regulatory constraints trigger upfront capital expenditures but lower long-term health and resource degradation costs.")
    if has_emp and has_econ:
        cross_effects.append("Workforce displacement and retraining velocity determine whether productivity gains translate into broad consumer spending growth.")

    if not cross_effects:
        cross_effects.append(f"Interdependencies observed between {', '.join([d.display_name for d in domains])} sectors.")

    # High impact if any expert reported high impact
    overall_impact = "high" if any(a.impact_level == "high" for a in analyses) else "medium"

    overall_summary = (
        f"The scenario '{scenario.subject}' drives profound multi-domain transformations. "
        f"Key interactions focus on balancing transitional disruption in {', '.join([d.display_name for d in domains])} "
        f"against long-term strategic opportunities."
    )

    return Synthesis(
        overall_impact=overall_impact,
        overall_summary=overall_summary,
        key_positive_impacts=positives[:4],
        key_negative_impacts=negatives[:4],
        major_risks=risks[:4],
        major_opportunities=opps[:4],
        cross_domain_effects=cross_effects,
        uncertainties=list(set(uncertainties))[:4]
    )
