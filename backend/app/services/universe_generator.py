import logging
from app.schemas.scenario import Scenario, Synthesis, ParallelUniverses, UniverseOutcome
from app.services.llm_service import llm_service

logger = logging.getLogger("ai_parallel_universe.universe_generator")

SYSTEM_PROMPT = """
You are the Parallel Universe Generation Engine.
Based on the scenario and synthesized multi-agent analysis, project THREE distinct plausible future outcomes:
1. optimistic: A favorable but plausible future where opportunities are maximized and risks are mitigated.
2. baseline: The most central, likely future given current trends and moderate execution.
3. adverse: A plausible future where key risks materialize and implementation faces major obstacles.

Return JSON matching this schema:
{
  "optimistic": {
    "title": "Optimistic Future Title",
    "summary": "Favorable future summary...",
    "key_outcomes": ["string"],
    "major_drivers": ["string"],
    "risks": ["string"]
  },
  "baseline": {
    "title": "Baseline Future Title",
    "summary": "Central baseline future summary...",
    "key_outcomes": ["string"],
    "major_drivers": ["string"],
    "risks": ["string"]
  },
  "adverse": {
    "title": "Adverse Future Title",
    "summary": "Challenging adverse future summary...",
    "key_outcomes": ["string"],
    "major_drivers": ["string"],
    "risks": ["string"]
  }
}

Do NOT attach fake percentage probabilities (e.g. 30%, 50%).
"""


async def generate_parallel_universes(scenario: Scenario, synthesis: Synthesis) -> ParallelUniverses:
    """
    Generates Optimistic, Baseline, and Adverse parallel universe outcomes based on synthesized evidence.
    """
    user_prompt = f"""Scenario: {scenario.original_text}
Subject: {scenario.subject}
Action: {scenario.action}

Synthesized Summary: {synthesis.overall_summary}
Major Opportunities: {', '.join(synthesis.major_opportunities)}
Major Risks: {', '.join(synthesis.major_risks)}
Cross Domain Effects: {', '.join(synthesis.cross_domain_effects)}

Generate the three parallel universe outcomes."""

    llm_result = await llm_service.generate_json(SYSTEM_PROMPT, user_prompt)

    if llm_result:
        try:
            return ParallelUniverses(
                optimistic=UniverseOutcome(**llm_result["optimistic"]),
                baseline=UniverseOutcome(**llm_result["baseline"]),
                adverse=UniverseOutcome(**llm_result["adverse"]),
            )
        except Exception as e:
            logger.warning(f"Error parsing LLM parallel universe response: {e}")

    # Fallback / Mock Universe Generator
    return _generate_universes_mock(scenario, synthesis)


def _generate_universes_mock(scenario: Scenario, synthesis: Synthesis) -> ParallelUniverses:
    subject = scenario.subject or "the policy target"
    action = scenario.action or "implementation"

    optimistic = UniverseOutcome(
        title="Accelerated & Seamless Transition",
        summary=f"Rapid innovation, effective policy execution, and strong investment drive a smooth, prosperous outcome for {subject}.",
        key_outcomes=[
            f"Rapid adoption of next-generation solutions related to {subject}.",
            "High private capital inflows and expansion of high-wage jobs.",
            "Minimal supply disruption with net positive environmental and economic gains."
        ],
        major_drivers=[
            "Proactive government infrastructure subsidies and policy alignment.",
            "Technological breakthroughs reducing implementation costs ahead of schedule."
        ],
        risks=[
            "Localized infrastructure bottlenecks under unexpectedly high adoption speeds."
        ]
    )

    baseline = UniverseOutcome(
        title="Gradual & Pragmatic Transition",
        summary=f"The transition proceeds along a central timeline, balancing steady progress against moderate cost and infrastructure friction.",
        key_outcomes=[
            f"Steady incremental rollout of {action} with moderate sector adjustment.",
            "Managed workforce retraining keeping unemployment changes within normal bands.",
            "Balanced economic impact with temporary price adjustments before long-term stabilization."
        ],
        major_drivers=[
            "Standard policy enforcement and market demand expansion.",
            "Gradual supply chain capacity expansion."
        ],
        risks=[
            "Sub-optimal coordination between regional regulatory bodies.",
            "Short-term cost increases for early adopters."
        ]
    )

    adverse = UniverseOutcome(
        title="Constrained & Friction-Heavy Transition",
        summary=f"Implementation faces severe supply bottlenecks, regulatory delays, and cost overruns, triggering political and economic backlash.",
        key_outcomes=[
            f"Delayed timeline for {subject} transition due to supply chain and infrastructure deficits.",
            "Increased consumer and industry resistance caused by elevated costs.",
            "Structural displacement of legacy industry workers without sufficient retraining absorption."
        ],
        major_drivers=[
            "Critical material shortages and elevated global supply costs.",
            "Regulatory gridlock and inadequate public infrastructure funding."
        ],
        risks=[
            "Stranded capital assets in legacy sectors and diminished international competitiveness.",
            "Public pressure leading to policy rollbacks or extended deadline exemptions."
        ]
    )

    return ParallelUniverses(
        optimistic=optimistic,
        baseline=baseline,
        adverse=adverse
    )
