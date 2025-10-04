import LightCurveChart from "../LightCurveChart";

export default function LightCurveChartExample() {
  const mockData = Array.from({ length: 100 }, (_, i) => {
    const time = (i / 100) * 10;
    const transitCenter = 5;
    const transitWidth = 1.5;
    const depth = 0.01;
    
    const inTransit = Math.abs(time - transitCenter) < transitWidth;
    const transitProgress = inTransit 
      ? 1 - Math.cos((Math.PI * (time - transitCenter)) / transitWidth) / 2
      : 0;
    
    const flux = 1 - (depth * transitProgress) + (Math.random() * 0.001 - 0.0005);
    
    return { time: parseFloat(time.toFixed(2)), flux: parseFloat(flux.toFixed(6)) };
  });

  return (
    <div className="w-full max-w-4xl">
      <LightCurveChart data={mockData} />
    </div>
  );
}
