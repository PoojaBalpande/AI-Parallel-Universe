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
