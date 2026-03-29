import type { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-surface flex flex-col relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-primary/5 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-surface-highest/20 blur-[100px] rounded-full pointer-events-none" />
      
      <main className="flex-1 flex flex-col relative z-10 px-4 py-12 md:py-20 w-full max-w-5xl mx-auto">
        {children}
      </main>
    </div>
  );
}
