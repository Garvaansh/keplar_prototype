import { Card } from "@/components/ui/card";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Activity } from "lucide-react";

interface LightCurveChartProps {
  data: Array<{ time: number; flux: number }>;
}

export default function LightCurveChart({ data }: LightCurveChartProps) {
  return (
    <Card className="p-4 border-primary/20 bg-card/50 backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-4">
        <div className="p-1.5 rounded-md bg-primary/10 text-primary">
          <Activity className="w-4 h-4" />
        </div>
        <div>
          <h3 className="font-heading text-base font-semibold text-foreground">
            Transit Light Curve
          </h3>
          <p className="text-xs text-muted-foreground">
            Real-time brightness variation during planetary transit
          </p>
        </div>
      </div>

      <div className="relative">
        <ResponsiveContainer width="100%" height={220}>
          <AreaChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="fluxGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity={0.8} />
                <stop offset="50%" stopColor="hsl(var(--primary))" stopOpacity={0.3} />
                <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
            <XAxis
              dataKey="time"
              stroke="hsl(var(--muted-foreground))"
              tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }}
              label={{ value: "Time (hours)", position: "insideBottom", offset: -5, fill: "hsl(var(--muted-foreground))" }}
            />
            <YAxis
              stroke="hsl(var(--muted-foreground))"
              tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }}
              label={{ value: "Normalized Flux", angle: -90, position: "insideLeft", fill: "hsl(var(--muted-foreground))" }}
              domain={[0.985, 1.005]}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "6px",
                backdropFilter: "blur(8px)",
              }}
              labelStyle={{ color: "hsl(var(--foreground))", fontFamily: "var(--font-mono)" }}
              itemStyle={{ color: "hsl(var(--primary))", fontFamily: "var(--font-mono)" }}
            />
            <Area
              type="monotone"
              dataKey="flux"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              fill="url(#fluxGradient)"
              dot={false}
              animationDuration={500}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
