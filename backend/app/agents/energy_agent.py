from app.agents.base_agent import BaseAgent
from app.schemas.scenario import Scenario, ExpertAnalysis


class EnergyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Energy Expert",
            domain="energy",
            role="Energy System & Infrastructure Strategist",
            system_instructions=(
                "Focus on energy demand, fuel and electricity supply, power grid capacity, utility infrastructure, "
                "renewable transition, energy storage, fuel distribution networks, and energy security."
            ),
        )

    def _analyze_mock(self, scenario: Scenario) -> ExpertAnalysis:
        text = scenario.original_text.lower()
        if "petrol" in text or "diesel" in text or "car" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="high",
                summary="Phasing out combustion vehicles causes a structural demand pivot from liquid petroleum distillates to grid electricity and fast-charging distribution.",
                positive_impacts=[
                    "Dramatically increases demand for renewable electricity generation (solar, wind, hydro).",
                    "Accelerates commercial deployment of grid-scale battery storage and smart charging grids."
                ],
                negative_impacts=[
                    "Puts severe peak-load stress on distribution transformers and urban sub-stations.",
                    "Refineries face steep declines in gasoline demand, forcing structural shutdowns or retrofits."
                ],
                opportunities=[
                    "Expansion of nationwide EV charging networks and vehicle-to-grid (V2G) energy storage integration.",
                    "Growth in green hydrogen generation for heavy freight and transport applications."
                ],
                risks=[
                    "Local grid instability if EV charging coincides with peak residential power demand.",
                    "Grid capacity bottlenecks delaying rural charging infrastructure deployment."
                ],
                key_factors=[
                    "Rate of clean power generation expansion relative to EV adoption velocity.",
                    "Smart grid management software and dynamic pricing mechanisms."
                ],
                uncertainties=[
                    "Grid readiness and transformer manufacturing lead times over the transition timeline."
                ]
            )
        elif "drought" in text or "water" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="medium",
                summary="Water scarcity directly threatens thermal and hydroelectric power generation capacity.",
                positive_impacts=[
                    "Accelerates investment in water-independent renewable energy sources (solar PV, wind).",
                    "Drives adoption of closed-loop industrial cooling and dry-cooling power plant technology."
                ],
                negative_impacts=[
                    "Hydroelectric reservoir depletion leads to immediate regional power generation deficits.",
                    "Thermal and nuclear power plants forced to curtail output due to high cooling water temperatures."
                ],
                opportunities=[
                    "Deployment of distributed energy storage and solar microgrids to enhance regional grid resilience.",
                    "Incentivizes grid interconnection with neighboring regions to balance supply."
                ],
                risks=[
                    "Spikes in spot electricity prices during extreme heat and drought waves.",
                    "Increased reliance on fossil fuel peaking plants during hydro generation shortfalls."
                ],
                key_factors=[
                    "Duration of regional precipitation deficits and reservoir storage levels.",
                    "Share of solar and wind in the overall power mix."
                ],
                uncertainties=[
                    "Frequency of multi-year drought events under evolving climate baselines."
                ]
            )
        else:
            return super()._analyze_mock(scenario)
