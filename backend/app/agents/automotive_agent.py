from app.agents.base_agent import BaseAgent
from app.schemas.scenario import Scenario, ExpertAnalysis


class AutomotiveAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Automotive & Technology Expert",
            domain="automotive",
            role="Automotive Industry & Emerging Tech Specialist",
            system_instructions=(
                "Focus on technology adoption, automotive manufacturing, vehicle platform design, supply chain transformation, "
                "EV technology, autonomous systems, technological disruption, and digital manufacturing infrastructure."
            ),
        )

    def _analyze_mock(self, scenario: Scenario) -> ExpertAnalysis:
        text = scenario.original_text.lower()
        if "petrol" in text or "diesel" in text or "car" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="high",
                summary="The mandate accelerates the automotive industry's pivot from internal combustion engine platforms to software-defined electric vehicles.",
                positive_impacts=[
                    "Spurs massive R&D into solid-state battery chemistry, ultra-fast charging, and electric drive units.",
                    "Simplifies vehicle mechanical assembly through modular EV platform architectures."
                ],
                negative_impacts=[
                    "Legacy engine and transmission suppliers face structural obsolescence without product pivot.",
                    "High retooling costs for traditional OEM assembly plants."
                ],
                opportunities=[
                    "Integration of advanced driver-assistance systems (ADAS) and software-defined vehicle features.",
                    "Emergence of new domestic OEM market entrants unburdened by legacy ICE assets."
                ],
                risks=[
                    "Supply chain bottlenecks for specialized battery components and automotive-grade semiconductors.",
                    "Market consolidation leading to failure of slow-adapting legacy component suppliers."
                ],
                key_factors=[
                    "Battery cell cost reduction curve ($/kWh).",
                    "OEM software engineering capabilities and battery supply chain security."
                ],
                uncertainties=[
                    "Speed of technological convergence between autonomous features and electric drivetrains."
                ]
            )
        elif "ai" in text or "automate" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="high",
                summary="AI technology disruption re-architects enterprise software stacks, automation workflows, and human-computer interactions.",
                positive_impacts=[
                    "Rapid deployment of autonomous agents, modern software APIs, and automated customer workflows.",
                    "Dramatic acceleration of software development cycles and digital product iteration."
                ],
                negative_impacts=[
                    "Security vulnerabilities and data privacy risks in early enterprise AI model deployments.",
                    "High compute infrastructure expenditures for training and operating large models."
                ],
                opportunities=[
                    "Creation of next-generation autonomous software tooling and intelligent edge devices.",
                    "Hyper-personalized user interfaces and multi-modal customer experience platforms."
                ],
                risks=[
                    "Vendor lock-in with dominant proprietary AI foundation model providers.",
                    "Algorithmic hallucinations or system reliability failures in mission-critical applications."
                ],
                key_factors=[
                    "Compute availability, GPU supply chains, and model optimization techniques.",
                    "Enterprise governance and cybersecurity frameworks."
                ],
                uncertainties=[
                    "Pace of AI model capability scaling vs enterprise adoption speed."
                ]
            )
        else:
            return super()._analyze_mock(scenario)
