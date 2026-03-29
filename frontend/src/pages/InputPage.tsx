import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { generatePitch, type GenerateRequest } from "@/api/client";
import { cn } from "@/lib/utils";
import { Loader2 } from "lucide-react";

export function InputPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<GenerateRequest>({
    project_name: "",
    description: "",
    target_audience: "",
    key_features: "",
    duration_seconds: 60,
    visual_mode: "image",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await generatePitch(formData);
      navigate(`/generating/${res.job_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-full w-full max-w-2xl mx-auto space-y-12">
      <div className="text-center space-y-4">
        <h1 className="font-serif text-5xl md:text-6xl text-primary font-semibold tracking-tightest">
          PITCH MAKER
        </h1>
        <p className="text-on-surface/60 text-lg md:text-xl font-medium tracking-widest uppercase">
          Turn your project into a cinematic pitch
        </p>
      </div>

      <form 
        onSubmit={handleSubmit}
        className="w-full bg-surface-highest/50 backdrop-blur-2xl p-8 md:p-10 rounded-2xl border border-outline-ghost shadow-2xl flex flex-col space-y-8"
      >
        {error && (
          <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-lg text-sm">
            {error}
          </div>
        )}

        <div className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="project_name" className="text-sm font-medium text-on-surface/80 uppercase tracking-widest">
              Project Name
            </label>
            <input
              id="project_name"
              required
              value={formData.project_name}
              onChange={e => setFormData({ ...formData, project_name: e.target.value })}
              className="w-full bg-surface-lowest border-b border-outline-variant px-4 py-3 text-on-surface placeholder:text-on-surface/30 focus:outline-none focus:border-primary focus:shadow-[0_1px_0_0_#f2c062] transition-all rounded-t-md"
              placeholder="e.g., Pitch Maker"
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="description" className="text-sm font-medium text-on-surface/80 uppercase tracking-widest">
              What does it do?
            </label>
            <textarea
              id="description"
              required
              rows={3}
              value={formData.description}
              onChange={e => setFormData({ ...formData, description: e.target.value })}
              className="w-full bg-surface-lowest border-b border-outline-variant px-4 py-3 text-on-surface placeholder:text-on-surface/30 focus:outline-none focus:border-primary focus:shadow-[0_1px_0_0_#f2c062] transition-all rounded-t-md resize-none"
              placeholder="Describe your project in 2-3 sentences..."
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="target_audience" className="text-sm font-medium text-on-surface/80 uppercase tracking-widest">
              Who is it for?
            </label>
            <input
              id="target_audience"
              required
              value={formData.target_audience}
              onChange={e => setFormData({ ...formData, target_audience: e.target.value })}
              className="w-full bg-surface-lowest border-b border-outline-variant px-4 py-3 text-on-surface placeholder:text-on-surface/30 focus:outline-none focus:border-primary focus:shadow-[0_1px_0_0_#f2c062] transition-all rounded-t-md"
              placeholder="e.g., Hackathon participants, developers"
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="key_features" className="text-sm font-medium text-on-surface/80 uppercase tracking-widest">
              Key Features
            </label>
            <textarea
              id="key_features"
              required
              rows={4}
              value={formData.key_features}
              onChange={e => setFormData({ ...formData, key_features: e.target.value })}
              className="w-full bg-surface-lowest border-b border-outline-variant px-4 py-3 text-on-surface placeholder:text-on-surface/30 focus:outline-none focus:border-primary focus:shadow-[0_1px_0_0_#f2c062] transition-all rounded-t-md resize-none"
              placeholder="List 3-5 key features, one per line..."
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <label className="text-sm font-medium text-on-surface/80 uppercase tracking-widest">
                Pitch Duration
              </label>
              <div className="flex bg-surface-lowest rounded-lg p-1 border border-outline-variant">
                {[30, 60, 90].map(duration => (
                  <button
                    key={duration}
                    type="button"
                    onClick={() => setFormData({ ...formData, duration_seconds: duration as 30 | 60 | 90 })}
                    className={cn(
                      "flex-1 py-2 text-sm font-medium rounded-md transition-all",
                      formData.duration_seconds === duration
                        ? "bg-surface-highest text-primary shadow-sm"
                        : "text-on-surface/60 hover:text-on-surface"
                    )}
                  >
                    {duration}s
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-3">
              <label className="text-sm font-medium text-on-surface/80 uppercase tracking-widest">
                Visual Style
              </label>
              <div className="flex bg-surface-lowest rounded-lg p-1 border border-outline-variant">
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, visual_mode: "image" })}
                  className={cn(
                    "flex-1 py-2 text-sm font-medium rounded-md transition-all flex flex-col items-center justify-center",
                    formData.visual_mode === "image"
                      ? "bg-surface-highest text-primary shadow-sm"
                      : "text-on-surface/60 hover:text-on-surface"
                  )}
                >
                  <span>AI Images</span>
                  <span className="text-[10px] opacity-70 font-normal">Fast & reliable</span>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, visual_mode: "video" })}
                  className={cn(
                    "flex-1 py-2 text-sm font-medium rounded-md transition-all flex flex-col items-center justify-center",
                    formData.visual_mode === "video"
                      ? "bg-surface-highest text-primary shadow-sm"
                      : "text-on-surface/60 hover:text-on-surface"
                  )}
                >
                  <span>AI Video</span>
                  <span className="text-[10px] opacity-70 font-normal">Cinematic (Slower)</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-br from-primary to-primary-container text-on-primary font-semibold py-4 rounded-md shadow-glow hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 text-lg"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Starting Production...</span>
            </>
          ) : (
            <span>Generate Cinematic Pitch &rarr;</span>
          )}
        </button>
      </form>
    </div>
  );
}
