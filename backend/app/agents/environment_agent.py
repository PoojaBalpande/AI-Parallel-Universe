from app.agents.base_agent import BaseAgent
from app.schemas.scenario import Scenario, ExpertAnalysis


class EnvironmentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Environmental Expert",
            domain="environment",
            role="Climate & Ecological Sustainability Specialist",
            system_instructions=(
                "Focus on greenhouse gas emissions, tailpipe and industrial pollution, air quality, climate mitigation, "
                "resource extraction footprint, waste management, battery recycling, and ecological stability."
            ),
        )

    def _analyze_mock(self, scenario: Scenario) -> ExpertAnalysis:
        text = scenario.original_text.lower()
        if "petrol" in text or "diesel" in text or "car" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="high",
                summary="Eliminating internal combustion sales significantly mitigates tailpipe greenhouse gases and particulate pollution in urban centers.",
                positive_impacts=[
                    "Substantial reduction in nitrogen oxides (NOx), fine particulate matter (PM2.5), and CO2 emissions.",
                    "Direct improvement in urban air quality index (AQI) and associated public health outcomes."
                ],
                negative_impacts=[
                    "Increased environmental footprint from critical mineral mining (lithium, cobalt, rare earths).",
                    "E-waste management challenges from end-of-life battery pack disposal if unmanaged."
                ],
                opportunities=[
                    "Establishment of closed-loop circular battery recycling supply chains.",
                    "Decarbonization of urban transport sector aligning with net-zero carbon targets."
                ],
                risks=[
                    "Ecological degradation around lithium extraction sites without stringent environmental oversight.",
                    "Upstream emissions leakage if electricity grid remains heavily dependent on coal."
                ],
                key_factors=[
                    "Speed of power grid decarbonization.",
                    "Enforcement of circular battery recycling and ethical mining standards."
                ],
                uncertainties=[
                    "Lifecycle net carbon savings depending on regional power grid emissions intensity."
                ]
            )
        elif "drought" in text or "agriculture" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="high",
                summary="Protracted drought causes severe soil degradation, biodiversity strain, and groundwater depletion.",
                positive_impacts=[
                    "Encourages ecosystem restoration, watershed conservation, and regenerative agriculture practices.",
                    "Heightens public and policy focus on climate adaptation and water management policies."
                ],
                negative_impacts=[
                    "Irreversible loss of topsoil, vegetation cover, and localized ecosystem habitats.",
                    "Depletion of subterranean aquifers leading to land subsidence."
                ],
                opportunities=[
                    "Widespread deployment of precision irrigation and drought-resistant crop cultivation.",
                    "Expansion of protected wetland habitats and reforestation initiatives."
                ],
                risks=[
                    "Increased risk of catastrophic wildland fires and desertification.",
                    "Permanent loss of agricultural ecological viability in vulnerable regions."
                ],
                key_factors=[
                    "Groundwater extraction regulation and soil moisture conservation.",
                    "Regional temperature trends and microclimate stability."
                ],
                uncertainties=[
                    "Irreversibility of soil degradation thresholds under prolonged dry spells."
                ]
            )
        else:
            return super()._analyze_mock(scenario)
