from app.agents.base_agent import BaseAgent
from app.schemas.scenario import Scenario, ExpertAnalysis


class EconomyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Economic Expert",
            domain="economy",
            role="Macroeconomic & Financial Analyst",
            system_instructions=(
                "Focus on economic growth, investment, capital allocation, consumer costs, product prices, "
                "market dynamics, government fiscal health, trade balance, inflation, and private sector business impact."
            ),
        )

    def _analyze_mock(self, scenario: Scenario) -> ExpertAnalysis:
        text = scenario.original_text.lower()
        if "petrol" in text or "diesel" in text or "car" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="high",
                summary="The proposed transition will trigger significant capital reallocation across the auto supply chain, domestic energy production, and tax revenue streams.",
                positive_impacts=[
                    "Stimulates venture capital and industrial investment in electric mobility and charging infrastructure.",
                    "Long-term reduction in national crude oil import bills and currency exchange rate volatility."
                ],
                negative_impacts=[
                    "High upfront capital expenditure required for grid expansion and supply chain retooling.",
                    "Decline in fuel excise tax revenues for central and regional governments."
                ],
                opportunities=[
                    "Growth in domestic EV battery manufacturing, software integration, and recycling industries.",
                    "Potential to turn domestic EV ecosystem into a high-value export hub."
                ],
                risks=[
                    "Short-term consumer vehicle cost inflation prior to reaching battery cost parity.",
                    "Stranded assets in legacy petroleum refining and ICE component manufacturing."
                ],
                key_factors=[
                    "Battery cell raw material prices (lithium, nickel, cobalt).",
                    "Government subsidies, tax incentives, and public infrastructure financing."
                ],
                uncertainties=[
                    "Duration of consumer price premiums for zero-emission alternatives.",
                    "Macroeconomic inflationary pressures impacting infrastructure rollout speed."
                ]
            )
        elif "interest rate" in text or "monetary" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="high",
                summary="Monetary policy tightening elevates corporate borrowing costs and decelerates capital expenditure across credit-dependent industries.",
                positive_impacts=[
                    "Helps curb persistent inflationary pressures and stabilize price expectations.",
                    "Encourages capital discipline and prudent balance sheet management."
                ],
                negative_impacts=[
                    "Higher cost of capital slows mortgage activity, construction, and consumer credit growth.",
                    "Increased debt servicing burden for leveraged enterprises and sovereign debt."
                ],
                opportunities=[
                    "Higher yields for fixed-income investors and institutional asset managers.",
                    "Rebalancing of overvalued asset markets towards fundamental valuations."
                ],
                risks=[
                    "Risk of over-tightening leading to economic recession or credit crunch.",
                    "Increased corporate default risk among weaker borrowers."
                ],
                key_factors=[
                    "Inflation trajectory and central bank policy rate guidance.",
                    "Commercial banking sector liquidity and lending standards."
                ],
                uncertainties=[
                    "Time lag between interest rate hikes and broader economic slowdown."
                ]
            )
        elif "ai" in text or "automate" in text:
            return ExpertAnalysis(
                expert=self.name,
                domain=self.domain,
                impact_level="high",
                summary="Enterprise AI adoption accelerates labor productivity and operational margins while creating structural sector shifts.",
                positive_impacts=[
                    "Significant boost to labor productivity and corporate EBITDA margins in service sectors.",
                    "Deflationary pressure on enterprise software and customer operations costs."
                ],
                negative_impacts=[
                    "Potential aggregate demand suppression if displaced workers face extended unemployment.",
                    "Tax revenue impact on income taxes if wage shares shrink relative to capital returns."
                ],
                opportunities=[
                    "Creation of high-margin AI software, infrastructure, and consulting industries.",
                    "Enterprise efficiency gains leading to reinvestment in innovative R&D."
                ],
                risks=[
                    "Wealth concentration and growing capital vs labor income inequality.",
                    "Rapid obsolescence of existing enterprise technology stacks."
                ],
                key_factors=[
                    "Speed of enterprise AI integration and ROI realization.",
                    "Monetization models of primary AI model providers."
                ],
                uncertainties=[
                    "Net effect on total consumer purchasing power over a 5-10 year horizon."
                ]
            )
        else:
            return super()._analyze_mock(scenario)
