import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getJobStatus, type JobStatus } from "@/api/client";
import { StepProgress, type StepStatusType } from "@/components/StepProgress";
import { RefreshCcw } from "lucide-react";

export function GeneratingPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const [status, setStatus] = useState<JobStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId) return;

    const interval = setInterval(async () => {
      try {
        const currentStatus = await getJobStatus(jobId);
        setStatus(currentStatus);

        if (currentStatus.status === "completed") {
          clearInterval(interval);
          navigate(`/result/${jobId}`);
        }

        if (currentStatus.status === "error") {
          clearInterval(interval);
          setError(currentStatus.error || "An unknown error occurred");
        }
      } catch (err) {
        clearInterval(interval);
        setError(err instanceof Error ? err.message : "Failed to fetch status");
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId, navigate]);

  const steps = {
    generating_script: (status?.steps?.generating_script || "pending") as StepStatusType,
    generating_voice: (status?.steps?.generating_voice || "pending") as StepStatusType,
    generating_visuals: (status?.steps?.generating_visuals || "pending") as StepStatusType,
    assembling_video: (status?.steps?.assembling_video || "pending") as StepStatusType,
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] w-full max-w-md mx-auto">
      <div className="text-center space-y-4 mb-12">
        <h2 className="font-serif text-3xl text-primary font-semibold tracking-tightest">
          PITCH MAKER
        </h2>
        <div className="inline-block bg-surface-highest px-3 py-1 rounded-md">
          <span className="text-xs font-medium text-on-surface/80 uppercase tracking-widest">
            {status?.status === "error" ? "Production Halted" : "In Production"}
          </span>
        </div>
      </div>

      <div className="w-full bg-surface-low/50 backdrop-blur-xl p-8 rounded-2xl border border-outline-ghost">
        <StepProgress steps={steps} />
      </div>

      {error && (
        <div className="mt-8 text-center space-y-4">
          <p className="text-red-400 bg-red-500/10 border border-red-500/20 px-4 py-3 rounded-lg text-sm">
            {error}
          </p>
          <button
            onClick={() => navigate("/")}
            className="flex items-center justify-center space-x-2 w-full px-6 py-3 bg-surface-highest text-on-surface rounded-md border border-outline-ghost hover:bg-surface-highest/80 transition-colors"
          >
            <RefreshCcw className="w-4 h-4" />
            <span>Start Over</span>
          </button>
        </div>
      )}
    </div>
  );
}
