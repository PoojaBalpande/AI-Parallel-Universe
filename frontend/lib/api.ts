export interface HealthStatusResponse {
  status: string;
  service: string;
  version: string;
}

export interface HealthCheckResult {
  success: boolean;
  data?: HealthStatusResponse;
  error?: string;
  latencyMs?: number;
}

export interface LocationInfo {
  country?: string | null;
  region?: string | null;
  city?: string | null;
}

export interface TimeInfo {
  start_year?: number | null;
  end_year?: number | null;
  horizon_years?: number | null;
}

export interface Scenario {
  original_text: string;
  scenario_type: string;
  subject: string;
  action: string;
  affected_entities: string[];
  location?: LocationInfo | null;
  time?: TimeInfo | null;
  magnitude?: string | null;
  assumptions: string[];
  uncertainties: string[];
}

export interface DetectedDomain {
  name: string;
  display_name: string;
  relevance: number;
  reason: string;
}

export interface SelectedExpert {
  name: string;
  domain: string;
}

export interface ExpertAnalysis {
  expert: string;
  domain: string;
  impact_level: 'high' | 'medium' | 'low' | string;
  summary: string;
  positive_impacts: string[];
  negative_impacts: string[];
  opportunities: string[];
  risks: string[];
  key_factors: string[];
  uncertainties: string[];
}

export interface Synthesis {
  overall_impact: 'high' | 'medium' | 'low' | string;
  overall_summary: string;
  key_positive_impacts: string[];
  key_negative_impacts: string[];
  major_risks: string[];
  major_opportunities: string[];
  cross_domain_effects: string[];
  uncertainties: string[];
}

export interface UniverseOutcome {
  title: string;
  summary: string;
  key_outcomes: string[];
  major_drivers: string[];
  risks: string[];
}

export interface ParallelUniverses {
  optimistic: UniverseOutcome;
  baseline: UniverseOutcome;
  adverse: UniverseOutcome;
}

export interface AnalysisResponse {
  scenario: Scenario;
  domains: DetectedDomain[];
  experts: SelectedExpert[];
  analyses: ExpertAnalysis[];
  synthesis: Synthesis;
  parallel_universes: ParallelUniverses;
}

export interface AnalysisApiResult {
  success: boolean;
  data?: AnalysisResponse;
  error?: string;
  latencyMs?: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchHealthStatus(): Promise<HealthCheckResult> {
  const startTime = performance.now();
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
      cache: 'no-store',
    });

    const latencyMs = Math.round(performance.now() - startTime);

    if (!response.ok) {
      return {
        success: false,
        error: `HTTP Error ${response.status}: ${response.statusText}`,
        latencyMs,
      };
    }

    const data: HealthStatusResponse = await response.json();
    return {
      success: true,
      data,
      latencyMs,
    };
  } catch (error) {
    const latencyMs = Math.round(performance.now() - startTime);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to communicate with backend server',
      latencyMs,
    };
  }
}

export async function analyzeScenario(scenario: string): Promise<AnalysisApiResult> {
  const startTime = performance.now();
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ scenario }),
    });

    const latencyMs = Math.round(performance.now() - startTime);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: response.statusText }));
      const errorMsg = typeof errorData.detail === 'string'
        ? errorData.detail
        : Array.isArray(errorData.detail)
        ? errorData.detail.map((e: { msg?: string }) => e.msg || 'Validation error').join(', ')
        : 'Analysis request failed';

      return {
        success: false,
        error: errorMsg,
        latencyMs,
      };
    }

    const data: AnalysisResponse = await response.json();
    return {
      success: true,
      data,
      latencyMs,
    };
  } catch (error) {
    const latencyMs = Math.round(performance.now() - startTime);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to reach backend analysis server',
      latencyMs,
    };
  }
}
