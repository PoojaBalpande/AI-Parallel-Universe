from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "ok"})
    service: str = Field(..., json_schema_extra={"example": "ai-parallel-universe-backend"})
    version: str = Field(..., json_schema_extra={"example": "0.1.0"})

