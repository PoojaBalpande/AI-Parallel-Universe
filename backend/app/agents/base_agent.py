import logging
from typing import List, Dict, Any, Optional
from app.schemas.scenario import Scenario, ExpertAnalysis
from app.services.llm_service import llm_service

logger = logging.getLogger("ai_parallel_universe.agents")


class BaseAgent:
    """
    Abstract Base Agent class for domain-specific expert analysis.
    """

    def __init__(self, name: str, domain: str, role: str, system_instructions: str):
        self.name = name
        self.domain = domain
        self.role = role
        self.system_instructions = system_instructions

    async def analyze(self, scenario: Scenario) -> ExpertAnalysis:
        """
        Executes independent expert domain analysis for the given scenario.
        """
        system_prompt = f"""
You are the {self.name} ({self.role}).
{self.system_instructions}

Analyze the provided hypothetical scenario strictly from the perspective of your expert domain ({self.domain}).
Do not attempt to analyze outside your domain or rely on opinions from other experts.

Return a valid JSON object matching this schema:
{{
  "expert": "{self.name}",
  "domain": "{self.domain}",
  "impact_level": "high", // "high", "medium", or "low"
  "summary": "Concise executive analysis from your domain perspective...",
  "positive_impacts": ["string"],
  "negative_impacts": ["string"],
  "opportunities": ["string"],
  "risks": ["string"],
  "key_factors": ["string"],
  "uncertainties": ["string"]
}}
"""

        user_prompt = f"""Scenario: {scenario.original_text}
Scenario Type: {scenario.scenario_type}
Subject: {scenario.subject}
Action: {scenario.action}
Affected Entities: {', '.join(scenario.affected_entities)}
Location: {scenario.location.model_dump() if scenario.location else 'Not specified'}
Timeline: {scenario.time.model_dump() if scenario.time else 'Not specified'}
Known Assumptions: {', '.join(scenario.assumptions)}
Known Uncertainties: {', '.join(scenario.uncertainties)}

Provide your independent domain analysis."""

        llm_result = await llm_service.generate_json(system_prompt, user_prompt)

        if llm_result:
            try:
                llm_result["expert"] = self.name
                llm_result["domain"] = self.domain
                return ExpertAnalysis(**llm_result)
            except Exception as e:
                logger.warning(f"Error parsing LLM response for expert {self.name}: {e}")

        # Fallback to dynamic mock response generator specific to subclass domain
        return self._analyze_mock(scenario)

    def _analyze_mock(self, scenario: Scenario) -> ExpertAnalysis:
        """
        Fallback mock generator to be overridden by domain sub-agents or handled generically.
        """
        return ExpertAnalysis(
            expert=self.name,
            domain=self.domain,
            impact_level="medium",
            summary=f"Independent analysis by {self.name} on '{scenario.subject}'.",
            positive_impacts=[f"Potential domain efficiency gains in {self.domain}."],
            negative_impacts=[f"Short-term transitional costs in {self.domain}."],
            opportunities=[f"Innovation in {self.domain} solutions."],
            risks=[f"Unintended regulatory or market friction in {self.domain}."],
            key_factors=[f"Pace of implementation for {scenario.action}."],
            uncertainties=scenario.uncertainties or [f"Long-term policy stability in {self.domain}."]
        )
