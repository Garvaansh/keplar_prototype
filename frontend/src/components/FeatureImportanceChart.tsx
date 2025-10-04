import { Card } from "@/components/ui/card";
import { Bar, BarChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Sparkles } from "lucide-react";

interface FeatureData {
  name: string;
  importance: number;
  color: string;
}

interface FeatureImportanceChartProps {
  data: FeatureData[];
}

export default function FeatureImportanceChart({ data }: FeatureImportanceChartProps) {
  return (
    <Card className="p-4 border-primary/20 bg-card/50 backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-4">
        <div className="p-1.5 rounded-md bg-primary/10 text-primary">
          <Sparkles className="w-4 h-4" />
        </div>
        <div>
          <h3 className="font-heading text-base font-semibold text-foreground">
            AI Feature Importance
          </h3>
          <p className="text-xs text-muted-foreground">
            Which parameters drive the classification
          </p>
        </div>
      </div>

      <div className="relative">
        <ResponsiveContainer width="100%" height={180}>
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
          >
            <defs>
              {data.map((entry, index) => (
                <linearGradient key={index} id={`gradient-${index}`} x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor={entry.color} stopOpacity={0.8} />
                  <stop offset="100%" stopColor={entry.color} stopOpacity={1} />
                </linearGradient>
              ))}
            </defs>
            <XAxis
              type="number"
              stroke="hsl(var(--muted-foreground))"
              tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }}
              tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
            />
            <YAxis
              type="category"
              dataKey="name"
              stroke="hsl(var(--muted-foreground))"
              tick={{ fill: "hsl(var(--foreground))", fontSize: 13, fontWeight: 500 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "6px",
                backdropFilter: "blur(8px)",
              }}
              labelStyle={{ color: "hsl(var(--foreground))", fontWeight: 600 }}
              formatter={(value: number) => [`${(value * 100).toFixed(1)}%`, "Importance"]}
            />
            <Bar dataKey="importance" radius={[0, 4, 4, 0]} animationDuration={800}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={`url(#gradient-${index})`} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
