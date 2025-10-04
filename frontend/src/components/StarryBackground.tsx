export default function StarryBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
      <div className="absolute inset-0 bg-gradient-to-b from-background via-background to-primary/5" />
      
      <div className="stars absolute inset-0">
        {Array.from({ length: 100 }).map((_, i) => {
          const delay = Math.random() * 2;
          const duration = 2 + Math.random() * 3;
          return (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full animate-glow-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${delay}s`,
                animationDuration: `${duration}s`,
              }}
            />
          );
        })}
      </div>

      <div className="absolute top-1/4 -right-1/4 w-[600px] h-[600px] bg-primary/10 rounded-full blur-[120px] animate-glow-pulse" />
      <div className="absolute -bottom-1/4 -left-1/4 w-[500px] h-[500px] bg-chart-2/10 rounded-full blur-[100px] animate-glow-pulse" style={{ animationDelay: "1s" }} />
    </div>
  );
}
