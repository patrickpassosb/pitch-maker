import { cn } from "@/lib/utils";
import { PenTool, Mic, Image as ImageIcon, Film, CheckCircle2, Loader2, AlertCircle } from "lucide-react";

export type StepStatusType = "pending" | "in_progress" | "completed" | "error";

interface StepProgressProps {
  steps: {
    generating_script: StepStatusType;
    generating_voice: StepStatusType;
    generating_visuals: StepStatusType;
    assembling_video: StepStatusType;
  };
}

export function StepProgress({ steps }: StepProgressProps) {
  const stepsConfig = [
    { key: "generating_script", label: "Writing cinematic script...", icon: PenTool },
    { key: "generating_voice", label: "Generating voiceover...", icon: Mic },
    { key: "generating_visuals", label: "Creating visuals...", icon: ImageIcon },
    { key: "assembling_video", label: "Assembling final video...", icon: Film },
  ] as const;

  return (
    <div className="flex flex-col space-y-6">
      {stepsConfig.map((step, index) => {
        const status = steps[step.key];
        const Icon = step.icon;
        const isActive = status === "in_progress";
        const isCompleted = status === "completed";
        const isError = status === "error";

        return (
          <div key={step.key} className="flex items-center space-x-4 relative">
            {/* Connection Line */}
            {index < stepsConfig.length - 1 && (
              <div className="absolute left-6 top-10 bottom-[-1.5rem] w-px bg-surface-low -z-10" />
            )}
            
            <div
              className={cn(
                "flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center border transition-all duration-500",
                isActive ? "border-primary bg-primary/10 shadow-glow" : 
                isCompleted ? "border-green-500/50 bg-green-500/10" : 
                isError ? "border-red-500/50 bg-red-500/10" :
                "border-surface-highest bg-surface-lowest"
              )}
            >
              {isCompleted ? (
                <CheckCircle2 className="w-5 h-5 text-green-500" />
              ) : isError ? (
                <AlertCircle className="w-5 h-5 text-red-500" />
              ) : isActive ? (
                <Loader2 className="w-5 h-5 text-primary animate-spin" />
              ) : (
                <Icon className="w-5 h-5 text-surface-highest" />
              )}
            </div>
            
            <div className="flex-1">
              <p
                className={cn(
                  "font-medium text-lg transition-colors duration-500",
                  isActive ? "text-primary" : 
                  isCompleted ? "text-on-surface" : 
                  isError ? "text-red-400" :
                  "text-surface-highest"
                )}
              >
                {step.label}
              </p>
              {isError && (
                <p className="text-sm text-red-500/80 mt-1">
                  Task failed. Please try again.
                </p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
