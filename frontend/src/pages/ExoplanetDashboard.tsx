import { useState, useEffect } from "react";
import { Orbit, Gauge, Clock, Telescope } from "lucide-react";
import ParameterSlider from "@/components/ParameterSlider";
import LightCurveChart from "@/components/LightCurveChart";
import FeatureImportanceChart from "@/components/FeatureImportanceChart";
import AIClassificationCard from "@/components/AIClassificationCard";
import PlanetStatsCard from "@/components/PlanetStatsCard";
import StarryBackground from "@/components/StarryBackground";
import { Ruler, Thermometer, Calendar, Globe } from "lucide-react";

type Classification = "CONFIRMED" | "CANDIDATE" | "FALSE POSITIVE";

export default function ExoplanetDashboard() {
  const [orbitalPeriod, setOrbitalPeriod] = useState(15.5);
  const [transitDepth, setTransitDepth] = useState(5000);
  const [transitDuration, setTransitDuration] = useState(3.5);

  const [lightCurveData, setLightCurveData] = useState<Array<{ time: number; flux: number }>>([]);
  const [classification, setClassification] = useState<Classification>("CONFIRMED");
  const [confidence, setConfidence] = useState(0.94);

  useEffect(() => {
    const newData = generateLightCurve(orbitalPeriod, transitDepth / 1000000, transitDuration);
    setLightCurveData(newData);

    const { classification: newClass, confidence: newConf } = getMockPrediction(
      orbitalPeriod,
      transitDepth,
      transitDuration
    );
    setClassification(newClass);
    setConfidence(newConf);
  }, [orbitalPeriod, transitDepth, transitDuration]);

  const generateLightCurve = (period: number, depth: number, duration: number) => {
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

      const flux = 1 - depth * transitProgress + (Math.random() * 0.0005 - 0.00025);

      data.push({
        time: parseFloat(time.toFixed(2)),
        flux: parseFloat(flux.toFixed(6)),
      });
    }

    return data;
  };

  const getMockPrediction = (
    period: number,
    depth: number,
    duration: number
  ): { classification: Classification; confidence: number } => {
    const periodScore = period > 0.5 && period < 50 ? 1 : 0.3;
    const depthScore = depth > 500 && depth < 15000 ? 1 : 0.4;
    const durationScore = duration > 0.5 && duration < 12 ? 1 : 0.5;

    const totalScore = (periodScore + depthScore + durationScore) / 3;

    if (totalScore > 0.75) {
      return {
        classification: "CONFIRMED",
        confidence: 0.85 + Math.random() * 0.14,
      };
    } else if (totalScore > 0.5) {
      return {
        classification: "CANDIDATE",
        confidence: 0.55 + Math.random() * 0.2,
      };
    } else {
      return {
        classification: "FALSE POSITIVE",
        confidence: 0.7 + Math.random() * 0.25,
      };
    }
  };

  const featureImportance = [
    {
      name: "Transit Depth",
      importance: transitDepth / 10000,
      color: "hsl(var(--chart-1))",
    },
    {
      name: "Orbital Period",
      importance: Math.min(orbitalPeriod / 100, 0.95),
      color: "hsl(var(--chart-2))",
    },
    {
      name: "Transit Duration",
      importance: Math.min(transitDuration / 24, 0.85),
      color: "hsl(var(--chart-3))",
    },
  ].sort((a, b) => b.importance - a.importance);

  const planetStats = [
    {
      label: "Radius",
      value: (Math.sqrt(transitDepth / 10000) * 1.5).toFixed(1),
      unit: "R⊕",
      icon: <Ruler className="w-4 h-4" />,
    },
    {
      label: "Temperature",
      value: Math.round(300 + (50 / orbitalPeriod) * 200).toString(),
      unit: "K",
      icon: <Thermometer className="w-4 h-4" />,
    },
    {
      label: "Orbital Period",
      value: orbitalPeriod.toFixed(1),
      unit: "days",
      icon: <Calendar className="w-4 h-4" />,
    },
    {
      label: "Mass",
      value: (Math.sqrt(transitDepth / 10000) * 2.5).toFixed(1),
      unit: "M⊕",
      icon: <Globe className="w-4 h-4" />,
    },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground">
      <StarryBackground />

      <div className="relative z-10">
        <header className="border-b border-border/50 bg-card/30 backdrop-blur-md sticky top-0 z-20">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-primary/10 border border-primary/20">
                <Telescope className="w-6 h-6 text-primary" />
              </div>
              <div>
                <h1 className="text-2xl font-heading font-bold text-foreground">
                  A World Away
                </h1>
                <p className="text-sm text-muted-foreground">
                  Exoplanet AI Analyzer - Real-time Discovery Dashboard
                </p>
              </div>
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <div className="space-y-4">
                <h2 className="text-lg font-heading font-semibold text-foreground flex items-center gap-2">
                  <Gauge className="w-5 h-5 text-primary" />
                  Planetary Parameters
                </h2>

                <ParameterSlider
                  label="Orbital Period"
                  value={orbitalPeriod}
                  min={0.5}
                  max={100}
                  step={0.5}
                  unit="days"
                  description="How often the planet transits"
                  icon={<Orbit className="w-5 h-5" />}
                  onChange={setOrbitalPeriod}
                />

                <ParameterSlider
                  label="Transit Depth"
                  value={transitDepth}
                  min={100}
                  max={10000}
                  step={100}
                  unit="ppm"
                  description="How much light is blocked"
                  icon={<Gauge className="w-5 h-5" />}
                  onChange={setTransitDepth}
                />

                <ParameterSlider
                  label="Transit Duration"
                  value={transitDuration}
                  min={0.5}
                  max={24}
                  step={0.5}
                  unit="hours"
                  description="How long the transit lasts"
                  icon={<Clock className="w-5 h-5" />}
                  onChange={setTransitDuration}
                />
              </div>

              <LightCurveChart data={lightCurveData} />
              <FeatureImportanceChart data={featureImportance} />
            </div>

            <div className="space-y-6">
              <AIClassificationCard
                classification={classification}
                confidence={confidence}
              />

              {classification === "CONFIRMED" && (
                <div className="animate-slide-in">
                  <PlanetStatsCard stats={planetStats} />
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
