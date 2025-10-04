import { Card } from "@/components/ui/card";
import { Globe, Thermometer, Ruler, Calendar } from "lucide-react";

interface PlanetStat {
  label: string;
  value: string;
  unit: string;
  icon: React.ReactNode;
}

interface PlanetStatsCardProps {
  stats: PlanetStat[];
}

export default function PlanetStatsCard({ stats }: PlanetStatsCardProps) {
  return (
    <Card className="p-4 border-primary/20 bg-card/50 backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-4">
        <div className="p-1.5 rounded-md bg-primary/10 text-primary">
          <Globe className="w-4 h-4" />
        </div>
        <div>
          <h3 className="font-heading text-base font-semibold text-foreground">
            Planet Characteristics
          </h3>
          <p className="text-xs text-muted-foreground">
            Calculated properties for confirmed planets
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {stats.map((stat, index) => (
          <div
            key={index}
            className="p-3 rounded-lg bg-muted/30 border border-border/50 hover-elevate transition-all duration-300"
          >
            <div className="flex items-center gap-1.5 mb-1.5">
              <div className="text-primary">{stat.icon}</div>
              <span className="text-xs font-medium text-muted-foreground">
                {stat.label}
              </span>
            </div>
            <div className="flex items-baseline gap-1">
              <span className="font-mono text-lg font-bold text-foreground">
                {stat.value}
              </span>
              <span className="text-xs text-muted-foreground">{stat.unit}</span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
