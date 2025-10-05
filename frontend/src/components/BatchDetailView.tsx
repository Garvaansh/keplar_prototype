import { X } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import LightCurveChart from "@/components/LightCurveChart";
import FeatureImportanceChart from "@/components/FeatureImportanceChart";
import PlanetStatsCard from "@/components/PlanetStatsCard";
import { Ruler, Thermometer, Calendar, Globe } from "lucide-react";

interface DetailViewProps {
  result: {
    id: number;
    row: number;
    period: number;
    depth: number;
    duration: number;
    prediction: string;
    confidence: number;
    snr?: number;
    prob_confirmed?: number;
    prob_candidate?: number;
    prob_false_positive?: number;
    feature_importance?: Record<string, number>;
    light_curve_params?: any;
    warnings?: number;
    warning_details?: string[];
    status: string;
    has_warnings?: boolean;
  };
  index: number;
  onClose: () => void;
}

export default function BatchDetailView({
  result,
  index,
  onClose,
}: DetailViewProps) {
  const getClassificationColor = (prediction: string) => {
    switch (prediction) {
      case "CONFIRMED":
        return "bg-confirmed/20 text-confirmed border-confirmed";
      case "CANDIDATE":
        return "bg-candidate/20 text-candidate border-candidate";
      case "FALSE POSITIVE":
        return "bg-false-positive/20 text-false-positive border-false-positive";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  // Generate feature importance data from backend response
  const featureImportanceData = result.feature_importance
    ? Object.entries(result.feature_importance)
        .map(([name, importance], idx) => ({
          name: name.replace("koi_", "").replace(/_/g, " "),
          importance,
          color: [
            "hsl(var(--chart-1))",
            "hsl(var(--chart-2))",
            "hsl(var(--chart-3))",
            "hsl(var(--chart-4))",
            "hsl(var(--chart-5))",
          ][idx % 5],
        }))
        .sort((a, b) => b.importance - a.importance)
        .slice(0, 5) // Top 5 features
    : [];

  // Calculate planet stats
  const planetStats = [
    {
      label: "Radius",
      value: (Math.sqrt(result.depth / 10000) * 1.5).toFixed(1),
      unit: "R⊕",
      icon: <Ruler className="w-4 h-4" />,
    },
    {
      label: "Temperature",
      value: Math.round(300 + (50 / result.period) * 200).toString(),
      unit: "K",
      icon: <Thermometer className="w-4 h-4" />,
    },
    {
      label: "Orbital Period",
      value: result.period.toFixed(1),
      unit: "days",
      icon: <Calendar className="w-4 h-4" />,
    },
    {
      label: "Mass",
      value: (Math.sqrt(result.depth / 10000) * 2.5).toFixed(1),
      unit: "M⊕",
      icon: <Globe className="w-4 h-4" />,
    },
  ];

  // Generate mock light curve
  const lightCurveData = generateMockLightCurve(
    result.period,
    result.depth / 1000000,
    result.duration
  );

  function generateMockLightCurve(
    period: number,
    depth: number,
    duration: number
  ) {
    const points = 100;
    const data = [];
    const totalTime = Math.min(period * 0.3, 10);

    for (let i = 0; i < points; i++) {
      const time = (i / points) * totalTime;
      const transitCenter = totalTime / 2;
      const transitWidth = duration / 2;

      const inTransit = Math.abs(time - transitCenter) < transitWidth;
      const transitProgress = inTransit
        ? 1 - Math.cos((Math.PI * (time - transitCenter)) / transitWidth) / 2
        : 0;

      const flux =
        1 - depth * transitProgress + (Math.random() * 0.0005 - 0.00025);

      data.push({
        time: parseFloat(time.toFixed(2)),
        flux: parseFloat(flux.toFixed(6)),
      });
    }

    return data;
  }

  return (
    <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
      <Card className="w-full max-w-6xl max-h-[90vh] overflow-auto bg-card border-primary/20">
        <div className="sticky top-0 bg-card/95 backdrop-blur-sm border-b border-border p-6 z-10">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-3">
                <h2 className="text-2xl font-heading font-bold">
                  Prediction Details #{index + 1}
                </h2>
                <Badge
                  variant="outline"
                  className={`${getClassificationColor(
                    result.prediction
                  )} text-sm px-3 py-1`}
                >
                  {result.prediction}
                </Badge>
                <span className="font-mono text-lg text-primary">
                  {(result.confidence * 100).toFixed(1)}%
                </span>
              </div>
              <p className="text-sm text-muted-foreground">
                Period: {result.period.toFixed(2)} days · Depth:{" "}
                {result.depth.toFixed(0)} ppm · Duration:{" "}
                {result.duration.toFixed(2)} hrs
              </p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={onClose}
              className="rounded-full"
            >
              <X className="w-5 h-5" />
            </Button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <LightCurveChart data={lightCurveData} />
              {featureImportanceData.length > 0 && (
                <FeatureImportanceChart data={featureImportanceData} />
              )}
            </div>

            <div className="space-y-6">
              <PlanetStatsCard stats={planetStats} />
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
