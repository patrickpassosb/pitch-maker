import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getJobStatus, type JobStatus, getVideoUrl } from "@/api/client";
import { VideoPlayer } from "@/components/VideoPlayer";
import { Download, Plus } from "lucide-react";

export function ResultPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const [status, setStatus] = useState<JobStatus | null>(null);

  useEffect(() => {
    if (!jobId) return;
    
    getJobStatus(jobId)
      .then(setStatus)
      .catch(console.error);
  }, [jobId]);

  if (!status) return null;

  const videoUrl = status.video_url ? getVideoUrl(status.video_url) : null;

  return (
    <div className="flex flex-col items-center min-h-[80vh] w-full max-w-4xl mx-auto space-y-12">
      <div className="text-center space-y-4">
        <h1 className="font-serif text-4xl md:text-5xl text-primary font-semibold tracking-tightest">
          Your Pitch is Ready
        </h1>
        <p className="text-on-surface/60 text-lg font-medium tracking-widest uppercase">
          Production Complete
        </p>
      </div>

      <div className="w-full">
        {videoUrl && (
          <VideoPlayer url={videoUrl} />
        )}
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 w-full max-w-md">
        <a
          href={videoUrl || "#"}
          download
          className="w-full flex items-center justify-center space-x-2 bg-gradient-to-br from-primary to-primary-container text-on-primary font-semibold py-4 px-6 rounded-md shadow-glow hover:opacity-90 transition-opacity"
        >
          <Download className="w-5 h-5" />
          <span>Download MP4</span>
        </a>
        
        <button
          onClick={() => navigate("/")}
          className="w-full flex items-center justify-center space-x-2 bg-surface-highest border border-outline-ghost text-on-surface font-medium py-4 px-6 rounded-md hover:bg-surface-highest/80 transition-colors"
        >
          <Plus className="w-5 h-5" />
          <span>Create New Pitch</span>
        </button>
      </div>
    </div>
  );
}
