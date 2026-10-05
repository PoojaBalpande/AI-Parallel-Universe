import asyncio
import logging
from typing import List
from app.agents import AGENT_REGISTRY, BaseAgent
from app.schemas.scenario import Scenario, SelectedExpert, ExpertAnalysis

logger = logging.getLogger("ai_parallel_universe.agent_runner")


async def run_expert_agents(selected_experts: List[SelectedExpert], scenario: Scenario) -> List[ExpertAnalysis]:
    """
    Executes all selected expert agents concurrently and independently.
    Returns list of structured ExpertAnalysis objects.
    """
    tasks = []

    for expert_info in selected_experts:
        domain = expert_info.domain
        agent_cls = AGENT_REGISTRY.get(domain)

        if agent_cls:
            agent_instance: BaseAgent = agent_cls()
        else:
            # Fallback agent instance for any generic domain
            agent_instance = BaseAgent(
                name=expert_info.name,
                domain=domain,
                role=f"{domain.capitalize()} Specialist",
                system_instructions=f"Analyze scenario impact on {domain} sector."
            )

        logger.info(f"Dispatching independent task for agent: {agent_instance.name}")
        tasks.append(agent_instance.analyze(scenario))

    if not tasks:
        logger.warning("No expert agents were selected for execution.")
        return []

    # Run independent expert analyses in parallel
    analyses = await asyncio.gather(*tasks, return_exceptions=False)
    return list(analyses)
