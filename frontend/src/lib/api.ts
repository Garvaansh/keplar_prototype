/**
 * 🚀 Exoplanet API Client
 * Connects React frontend to FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

// Type definitions matching backend models
export interface TransitParameters {
  koi_period: number;
  koi_depth: number;
  koi_duration: number;
  koi_impact?: number;
  koi_model_snr?: number;
}

export interface PredictionRequest {
  transit: TransitParameters;
  planet?: {
    koi_prad?: number;
    koi_teq?: number;
    koi_insol?: number;
  };
  star?: {
    koi_steff?: number;
    koi_slogg?: number;
    koi_srad?: number;
  };
  flags?: {
    koi_fpflag_nt?: number;
    koi_fpflag_ss?: number;
    koi_fpflag_co?: number;
    koi_fpflag_ec?: number;
    koi_score?: number;
  };
}

export interface PredictionResponse {
  prediction: "CONFIRMED" | "CANDIDATE" | "FALSE POSITIVE";
  confidence: number;
  probabilities: Record<string, number>;
  feature_importance: Record<string, number>;
  validation_warnings: string[];
  light_curve_params: Record<string, number>;
  explanation: string;
}

export interface LightCurvePoint {
  x: number;
  y: number;
}

export interface LightCurveResponse {
  data: LightCurvePoint[];
  metadata: {
    period: number;
    depth_ppm: number;
    duration_hours: number;
    impact: number;
    num_points: number;
    time_span_days: number;
    depth_fraction: number;
  };
  chart_config: {
    type: string;
    xlabel: string;
    ylabel: string;
    title: string;
  };
}

/**
 * Get prediction from the ML model
 */
export async function getPrediction(
  params: PredictionRequest
): Promise<PredictionResponse> {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Prediction failed" }));
    throw new Error(error.detail || "Prediction failed");
  }

  return response.json();
}

/**
 * Get light curve data from backend
 */
export async function getLightCurve(
  period: number,
  depth: number,
  duration: number,
  impact: number = 0.5
): Promise<LightCurveResponse> {
  const response = await fetch(
    `${API_BASE_URL}/light-curve/${period}/${depth}/${duration}?impact=${impact}`
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Light curve generation failed" }));
    throw new Error(error.detail || "Light curve generation failed");
  }

  return response.json();
}

/**
 * Check API health
 */
export async function checkHealth(): Promise<{ status: string; timestamp: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error("API health check failed");
  }

  return response.json();
}

/**
 * Get feature bounds for validation
 */
export async function getFeatureBounds(): Promise<Record<string, { min: number; max: number }>> {
  const response = await fetch(`${API_BASE_URL}/feature-bounds`);
  
  if (!response.ok) {
    throw new Error("Failed to fetch feature bounds");
  }

  return response.json();
}
