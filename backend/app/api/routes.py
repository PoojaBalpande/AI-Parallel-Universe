import logging
from fastapi import APIRouter, HTTPException, status
from app.config import settings
from app.schemas.health import HealthResponse
from app.schemas.scenario import ScenarioRequest, AnalysisResponse
from app.services.scenario_parser import parse_scenario
from app.services.domain_detector import detect_domains
from app.services.expert_selector import select_experts
from app.services.agent_runner import run_expert_agents
from app.services.synthesizer import synthesize_analyses
from app.services.universe_generator import generate_parallel_universes

logger = logging.getLogger("ai_parallel_universe.routes")

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Backend Health Check",
    description="Returns backend status, service name, and API version."
)
async def get_health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="ai-parallel-universe-backend",
        version=settings.APP_VERSION
    )


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Analyze Hypothetical Scenario",
    description="Decomposes scenario, detects affected domains, dispatches expert agents, synthesizes findings, and projects parallel universes."
)
async def analyze_scenario(payload: ScenarioRequest) -> AnalysisResponse:
    try:
        logger.info(f"Received scenario analysis request: '{payload.scenario[:60]}...'")

        # 1. Parse Scenario
        scenario_obj = await parse_scenario(payload.scenario)

        # 2. Detect Domains
        detected_domains = await detect_domains(scenario_obj)

        # 3. Select Experts
        selected_experts = select_experts(detected_domains)

        # 4. Multi-Agent Independent Analysis
        expert_analyses = await run_expert_agents(selected_experts, scenario_obj)

        # 5. Synthesize Analyses
        synthesis_result = await synthesize_analyses(scenario_obj, detected_domains, expert_analyses)

        # 6. Generate Parallel Universes
        universes_result = await generate_parallel_universes(scenario_obj, synthesis_result)

        return AnalysisResponse(
            scenario=scenario_obj,
            domains=detected_domains,
            experts=selected_experts,
            analyses=expert_analyses,
            synthesis=synthesis_result,
            parallel_universes=universes_result
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as exc:
        logger.error(f"Error processing scenario analysis: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process parallel universe scenario analysis."
        )

