import PlanetStatsCard from "../PlanetStatsCard";
import { Ruler, Thermometer, Calendar, Globe } from "lucide-react";

export default function PlanetStatsCardExample() {
  const mockStats = [
    { label: "Radius", value: "1.2", unit: "R⊕", icon: <Ruler className="w-4 h-4" /> },
    { label: "Temperature", value: "450", unit: "K", icon: <Thermometer className="w-4 h-4" /> },
    { label: "Orbital Period", value: "15.5", unit: "days", icon: <Calendar className="w-4 h-4" /> },
    { label: "Mass", value: "3.8", unit: "M⊕", icon: <Globe className="w-4 h-4" /> },
  ];

  return (
    <div className="w-full max-w-2xl">
      <PlanetStatsCard stats={mockStats} />
    </div>
  );
}
