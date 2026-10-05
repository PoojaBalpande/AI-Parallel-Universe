from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class ScenarioRequest(BaseModel):
    scenario: str

    @field_validator("scenario")
    @classmethod
    def validate_scenario(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Scenario must be a string.")
        v = v.strip()
        if not v:
            raise ValueError("Scenario input cannot be empty.")
        if len(v) > 2000:
            raise ValueError("Scenario text is too long (maximum 2000 characters).")
        return v


class LocationInfo(BaseModel):
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None


class TimeInfo(BaseModel):
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    horizon_years: Optional[int] = None


class Scenario(BaseModel):
    original_text: str
    scenario_type: str
    subject: str
    action: str
    affected_entities: List[str] = Field(default_factory=list)
    location: Optional[LocationInfo] = None
    time: Optional[TimeInfo] = None
    magnitude: Optional[str] = None
    assumptions: List[str] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)


class DetectedDomain(BaseModel):
    name: str
    display_name: str
    relevance: float
    reason: str


class SelectedExpert(BaseModel):
    name: str
    domain: str


class ExpertAnalysis(BaseModel):
    expert: str
    domain: str
    impact_level: str
    summary: str
    positive_impacts: List[str] = Field(default_factory=list)
    negative_impacts: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    key_factors: List[str] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)


class Synthesis(BaseModel):
    overall_impact: str
    overall_summary: str
    key_positive_impacts: List[str] = Field(default_factory=list)
    key_negative_impacts: List[str] = Field(default_factory=list)
    major_risks: List[str] = Field(default_factory=list)
    major_opportunities: List[str] = Field(default_factory=list)
    cross_domain_effects: List[str] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)


class UniverseOutcome(BaseModel):
    title: str
    summary: str
    key_outcomes: List[str] = Field(default_factory=list)
    major_drivers: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)


class ParallelUniverses(BaseModel):
    optimistic: UniverseOutcome
    baseline: UniverseOutcome
    adverse: UniverseOutcome


class AnalysisResponse(BaseModel):
    scenario: Scenario
    domains: List[DetectedDomain]
    experts: List[SelectedExpert]
    analyses: List[ExpertAnalysis]
    synthesis: Synthesis
    parallel_universes: ParallelUniverses
