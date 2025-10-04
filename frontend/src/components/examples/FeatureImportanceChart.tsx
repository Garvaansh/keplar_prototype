import FeatureImportanceChart from "../FeatureImportanceChart";

export default function FeatureImportanceChartExample() {
  const mockData = [
    { name: "Transit Depth", importance: 0.85, color: "hsl(var(--chart-1))" },
    { name: "Orbital Period", importance: 0.72, color: "hsl(var(--chart-2))" },
    { name: "Transit Duration", importance: 0.58, color: "hsl(var(--chart-3))" },
  ];

  return (
    <div className="w-full max-w-3xl">
      <FeatureImportanceChart data={mockData} />
    </div>
  );
}
