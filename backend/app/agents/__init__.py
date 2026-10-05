from app.agents.base_agent import BaseAgent
from app.agents.economy_agent import EconomyAgent
from app.agents.energy_agent import EnergyAgent
from app.agents.environment_agent import EnvironmentAgent
from app.agents.automotive_agent import AutomotiveAgent
from app.agents.employment_agent import EmploymentAgent

AGENT_REGISTRY = {
    "economy": EconomyAgent,
    "energy": EnergyAgent,
    "environment": EnvironmentAgent,
    "automotive": AutomotiveAgent,
    "employment": EmploymentAgent,
}

__all__ = [
    "BaseAgent",
    "EconomyAgent",
    "EnergyAgent",
    "EnvironmentAgent",
    "AutomotiveAgent",
    "EmploymentAgent",
    "AGENT_REGISTRY",
]

