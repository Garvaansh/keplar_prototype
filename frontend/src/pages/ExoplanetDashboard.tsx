import { useState, useEffect } from "react";
import { Orbit, Gauge, Clock, Telescope, FileSpreadsheet } from "lucide-react";
import { Ruler, Thermometer, Calendar, Globe } from "lucide-react";
import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import ParameterSlider from "@/components/ParameterSlider";
import LightCurveChart from "@/components/LightCurveChart";
import FeatureImportanceChart from "@/components/FeatureImportanceChart";
import AIClassificationCard from "@/components/AIClassificationCard";
import PlanetStatsCard from "@/components/PlanetStatsCard";
import StarryBackground from "@/components/StarryBackground";
import { getPrediction, getLightCurve } from "@/lib/api";

type Classification = "CONFIRMED" | "CANDIDATE" | "FALSE POSITIVE";

export default function ExoplanetDashboard() {
  const [orbitalPeriod, setOrbitalPeriod] = useState(15.5);
  const [transitDepth, setTransitDepth] = useState(5000);
  const [transitDuration, setTransitDuration] = useState(3.5);

  const [lightCurveData, setLightCurveData] = useState<
    Array<{ time: number; flux: number }>
  >([]);
  const [classification, setClassification] =
    useState<Classification>("CONFIRMED");
  const [confidence, setConfidence] = useState(0.94);
  const [featureImportanceData, setFeatureImportanceData] = useState<
    Array<{ name: string; importance: number; color: string }>
  >([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPredictionAndLightCurve = async () => {
      setIsLoading(true);
      setError(null);

      try {
        // Fetch light curve from backend
        const lightCurveResponse = await getLightCurve(
          orbitalPeriod,
          transitDepth,
          transitDuration,
          0.5 // impact parameter
        );

        // Convert API format {x, y} to {time, flux}
        const convertedData = lightCurveResponse.data.map((point) => ({
          time: point.x,
          flux: point.y,
        }));
        setLightCurveData(convertedData);

        // Calculate derived parameters for better prediction
        const estimatedRadius = Math.sqrt(transitDepth / 10000) * 1.5; // Earth radii
        const estimatedTemp = Math.round(300 + (50 / orbitalPeriod) * 200); // Kelvin
        const estimatedSNR = Math.min(
          100,
          (transitDepth / 100) * (1 / (transitDuration / 24))
        ); // Signal-to-noise

        // Fetch prediction from backend with enhanced parameters
        const predictionResponse = await getPrediction({
          transit: {
            koi_period: orbitalPeriod,
            koi_depth: transitDepth,
            koi_duration: transitDuration,
            koi_impact: 0.5,
            koi_model_snr: estimatedSNR,
          },
          planet: {
            koi_prad: estimatedRadius,
            koi_teq: estimatedTemp,
            koi_insol: 1380 / Math.pow(orbitalPeriod / 365, 0.5), // Rough insolation estimate
          },
          star: {
            koi_steff: 5778, // Sun-like star
            koi_slogg: 4.44,
            koi_srad: 1.0,
          },
          flags: {
            koi_fpflag_nt: 0,
            koi_fpflag_ss: 0,
            koi_fpflag_co: 0,
            koi_fpflag_ec: 0,
            koi_score: 0.8, // Default good score
          },
        });

        setClassification(predictionResponse.prediction);
        setConfidence(predictionResponse.confidence);

        // Convert feature importance to chart format
        const colors = [
          "hsl(var(--chart-1))",
          "hsl(var(--chart-2))",
          "hsl(var(--chart-3))",
          "hsl(var(--chart-4))",
          "hsl(var(--chart-5))",
        ];

        const importanceArray = Object.entries(
          predictionResponse.feature_importance
        )
          .map(([name, importance], index) => ({
            name: name.replace("koi_", "").replace("_", " "),
            importance,
            color: colors[index % colors.length],
          }))
          .sort((a, b) => b.importance - a.importance)
          .slice(0, 5); // Top 5 features

        setFeatureImportanceData(importanceArray);
      } catch (err) {
        console.error("Failed to fetch prediction:", err);
        setError(
          err instanceof Error ? err.message : "Failed to fetch prediction"
        );

        // Fallback to mock data on error
        const mockData = generateMockLightCurve(
          orbitalPeriod,
          transitDepth / 1000000,
          transitDuration
        );
        setLightCurveData(mockData);
      } finally {
        setIsLoading(false);
      }
    };

    // Debounce API calls
    const timeoutId = setTimeout(fetchPredictionAndLightCurve, 300);
    return () => clearTimeout(timeoutId);
  }, [orbitalPeriod, transitDepth, transitDuration]);

  // Fallback function for generating mock data if API fails
  const generateMockLightCurve = (
    period: number,
    depth: number,
    duration: number
  ) => {
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
  };

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
            <div className="flex items-center justify-between">
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
              <Link href="/batch">
                <Button variant="outline" className="gap-2">
                  <FileSpreadsheet className="w-4 h-4" />
                  Batch Processing
                </Button>
              </Link>
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

              {error && (
                <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive text-sm">
                  ⚠️ {error} (Using fallback data)
                </div>
              )}

              <LightCurveChart data={lightCurveData} />
              <FeatureImportanceChart data={featureImportanceData} />
            </div>

            <div className="space-y-6">
              <AIClassificationCard
                classification={classification}
                confidence={confidence}
                isLoading={isLoading}
              />

              {!isLoading && (
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
