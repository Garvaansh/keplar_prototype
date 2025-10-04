import StarryBackground from "../StarryBackground";

export default function StarryBackgroundExample() {
  return (
    <div className="relative w-full h-96 bg-background">
      <StarryBackground />
      <div className="relative z-10 flex items-center justify-center h-full">
        <p className="text-foreground text-xl">Starry background with animated stars and nebula effects</p>
      </div>
    </div>
  );
}
