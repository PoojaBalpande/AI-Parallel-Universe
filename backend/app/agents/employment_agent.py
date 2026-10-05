from app.agents.base_agent import BaseAgent
from app.schemas.scenario import Scenario, ExpertAnalysis


class EmploymentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Employment & Workforce Expert",
            domain="employment",
            role="Labor Economics & Workforce Development Specialist",
            system_instructions=(
                "Focus on labor demand, job creation, employment displacement, workforce retraining, "
                "skill requirement shifts, wage trends, vocational transition, and labor market structural changes."
            ),
        )

    def _analyze_mock(self, scenario: Scenario) -> ExpertAnalysis:
        text = scenario.original_text.lower()
        if "petrol" in text or "diesel" in text or "car" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="medium",
                summary="Workforce structural transition shifting labor from traditional ICE mechanics and manufacturing to electrical, software, and battery technicians.",
                positive_impacts=[
                    "Creation of high-skilled engineering, battery technology, and charging station installation jobs.",
                    "Higher average wages for technical specialists skilled in high-voltage electrical systems."
                ],
                negative_impacts=[
                    "Displacement of workers in ICE engine manufacturing, exhaust systems, and traditional auto repair.",
                    "Risk of frictional unemployment in regions heavily reliant on traditional auto manufacturing."
                ],
                opportunities=[
                    "Large-scale national vocational retraining programs for electrical mechanics and EV technicians.",
                    "Growth in technical certification programs for clean tech workforce."
                ],
                risks=[
                    "Skill mismatch gap if legacy auto workers are not adequately retrained.",
                    "Regional economic distress in traditional automotive manufacturing hubs."
                ],
                key_factors=[
                    "Government and industry funding for workforce upskilling and reskilling.",
                    "Flexibility of labor market institutions to absorb displaced workers."
                ],
                uncertainties=[
                    "Total net job creation versus net job displacement ratio over the multi-year transition."
                ]
            )
        elif "ai" in text or "automate" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="high",
                summary="AI customer support automation creates immediate labor displacement in entry-level service roles while spurring demand for AI system managers.",
                positive_impacts=[
                    "Demand surge for AI prompt engineers, workflow orchestrators, data curators, and AI QA specialists.",
                    "Shift in human labor focus toward complex problem-solving and high-empathy customer escalations."
                ],
                negative_impacts=[
                    "Significant reduction in entry-level customer service representative headcount.",
                    "Downward wage pressure on routine administrative and support occupations."
                ],
                opportunities=[
                    "Rapid skill transition into digital support management and automated workflow operations.",
                    "Growth in specialized remote technical support roles supervising automated agents."
                ],
                risks=[
                    "Structural unemployment for entry-level workers lacking digital literacy.",
                    "Reduction in traditional entry-level career stepping stones into corporate management."
                ],
                key_factors=[
                    "Speed of AI agent adoption across enterprise customer service departments.",
                    "Availability of fast-track digital skills training programs."
                ],
                uncertainties=[
                    "Rate at which new AI-enabled occupations emerge to absorb displaced service workers."
                ]
            )
        else:
            return super()._analyze_mock(scenario)
