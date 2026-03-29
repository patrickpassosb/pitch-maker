export interface GenerateRequest {
  project_name: string;
  description: string;
  target_audience: string;
  key_features: string;
  duration_seconds: 30 | 60 | 90;
  visual_mode: "image" | "video";
}

export interface JobStatus {
  job_id: string;
  status: "processing" | "completed" | "error";
  current_step: string;
  steps: Record<string, string>;
  video_url: string | null;
  error: string | null;
}

const API_BASE = import.meta.env.VITE_API_URL || "/api";

export async function generatePitch(data: GenerateRequest): Promise<{ job_id: string; status: string }> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to start generation");
  return res.json();
}

export async function getJobStatus(jobId: string): Promise<JobStatus> {
  const res = await fetch(`${API_BASE}/status/${jobId}`);
  if (!res.ok) throw new Error("Failed to get status");
  return res.json();
}
