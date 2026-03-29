interface VideoPlayerProps {
  url: string;
}

export function VideoPlayer({ url }: VideoPlayerProps) {
  return (
    <div className="relative w-full aspect-video rounded-xl overflow-hidden bg-surface-lowest border border-surface-highest shadow-2xl">
      <video
        src={url}
        controls
        autoPlay
        className="w-full h-full object-cover"
        controlsList="nodownload"
      >
        Your browser does not support the video tag.
      </video>
    </div>
  );
}
