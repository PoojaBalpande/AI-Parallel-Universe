import pytest
from unittest.mock import AsyncMock, patch
import httpx
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)


@pytest.fixture(autouse=True)
def set_mock_mode_for_tests(monkeypatch):
    """
    Ensure standard tests default to LLM_MOCK_MODE=True so tests run deterministically without external API calls.
    """
    monkeypatch.setattr(settings, "LLM_MOCK_MODE", True)


def test_valid_scenario_analysis():
    """
    Test 2: Valid petrol/diesel car ban scenario
    """
    payload = {"scenario": "India bans the sale of new petrol and diesel cars from 2035."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()

    # Verify scenario structure
    assert "scenario" in data
    assert data["scenario"]["original_text"] == payload["scenario"]
    assert data["scenario"]["location"]["country"] == "India"
    assert data["scenario"]["time"]["start_year"] == 2035

    # Verify domains returned
    assert "domains" in data
    assert len(data["domains"]) > 0
    domain_names = [d["name"] for d in data["domains"]]
    assert "automotive" in domain_names
    assert "energy" in domain_names
    for d in data["domains"]:
        assert 0.0 <= d["relevance"] <= 1.0

    # Verify experts selected
    assert "experts" in data
    assert len(data["experts"]) == len(data["domains"])

    # Verify expert analyses returned
    assert "analyses" in data
    assert len(data["analyses"]) == len(data["experts"])
    for a in data["analyses"]:
        assert "expert" in a
        assert "domain" in a
        assert a["impact_level"] in ["high", "medium", "low"]
        assert len(a["positive_impacts"]) > 0

    # Verify synthesis
    assert "synthesis" in data
    assert "overall_impact" in data["synthesis"]
    assert "overall_summary" in data["synthesis"]
    assert "cross_domain_effects" in data["synthesis"]

    # Verify 3 parallel universes
    assert "parallel_universes" in data
    universes = data["parallel_universes"]
    assert "optimistic" in universes
    assert "baseline" in universes
    assert "adverse" in universes
    assert universes["optimistic"]["title"] != ""
    assert universes["baseline"]["title"] != ""
    assert universes["adverse"]["title"] != ""


def test_economic_scenario():
    """
    Test 3: Economic interest rate scenario
    """
    payload = {"scenario": "The central bank increases interest rates significantly."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    domain_names = [d["name"] for d in data["domains"]]
    assert "economy" in domain_names
    assert "employment" in domain_names


def test_technology_scenario():
    """
    Test 4: AI automation scenario
    """
    payload = {"scenario": "AI automates a large portion of customer service jobs."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    domain_names = [d["name"] for d in data["domains"]]
    assert "employment" in domain_names
    assert "automotive" in domain_names  # automotive & technology sector expert


def test_environment_scenario():
    """
    Test 5: Drought scenario
    """
    payload = {"scenario": "A severe drought reduces agricultural production for several years."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    domain_names = [d["name"] for d in data["domains"]]
    assert "environment" in domain_names
    assert "economy" in domain_names


def test_empty_input_validation():
    """
    Test 6: Empty input rejected
    """
    payload = {"scenario": "   "}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code in [400, 422]


def test_ambiguous_input():
    """
    Test 7: Ambiguous scenario without location or year
    """
    payload = {"scenario": "The government bans cars."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    scenario = data["scenario"]
    assert scenario["location"]["country"] is None
    assert scenario["time"]["start_year"] is None
    assert len(scenario["uncertainties"]) > 0


def test_llm_failure_in_live_mode_returns_error_response(monkeypatch):
    """
    Test failure handling: When LLM_MOCK_MODE=false and live LLM call fails,
    an explicit HTTP 502 error is returned and NO mock analysis is generated.
    """
    monkeypatch.setattr(settings, "LLM_MOCK_MODE", False)
    monkeypatch.setattr(settings, "LLM_API_KEY", "test-key-123")

    with patch("httpx.AsyncClient.post", side_effect=httpx.HTTPError("Simulated LLM network timeout")):
        payload = {"scenario": "India bans the sale of new petrol and diesel cars from 2035."}
        response = client.post("/api/analyze", json=payload)

        # Must return 502 Bad Gateway error instead of 200 OK mock analysis
        assert response.status_code == 502
        data = response.json()
        assert "LLM service failed" in data["detail"]
        assert "parallel_universes" not in data
        assert "analyses" not in data


def test_mock_mode_works_normally(monkeypatch):
    """
    Test mock mode: When LLM_MOCK_MODE=true, mock implementations generate complete analysis normally.
    """
    monkeypatch.setattr(settings, "LLM_MOCK_MODE", True)

    payload = {"scenario": "India bans the sale of new petrol and diesel cars from 2035."}
    response = client.post("/api/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "scenario" in data
    assert "parallel_universes" in data
    assert "optimistic" in data["parallel_universes"]

