from typing import List
from app.schemas.scenario import DetectedDomain, SelectedExpert

EXPERT_MAP = {
    "economy": "Economic Expert",
    "energy": "Energy Expert",
    "environment": "Environmental Expert",
    "automotive": "Automotive & Technology Expert",
    "employment": "Employment & Workforce Expert",
}


def select_experts(detected_domains: List[DetectedDomain]) -> List[SelectedExpert]:
    """
    Selects specialized expert agents matching the dynamically detected domains.
    """
    selected: List[SelectedExpert] = []
    for domain in detected_domains:
        expert_name = EXPERT_MAP.get(domain.name, f"{domain.display_name} Expert")
        selected.append(SelectedExpert(name=expert_name, domain=domain.name))
    return selected
