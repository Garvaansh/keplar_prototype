import { useState } from "react";
import { Slider } from "@/components/ui/slider";
import { Card } from "@/components/ui/card";

interface ParameterSliderProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  unit: string;
  description: string;
  icon: React.ReactNode;
  onChange: (value: number) => void;
}

export default function ParameterSlider({
  label,
  value,
  min,
  max,
  step,
  unit,
  description,
  icon,
  onChange,
}: ParameterSliderProps) {
  const [showTooltip, setShowTooltip] = useState(false);

  const percentage = ((value - min) / (max - min)) * 100;

  return (
    <Card className="p-4 border-primary/20 bg-card/50 backdrop-blur-sm hover-elevate transition-all duration-300">
      <div className="space-y-3">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-md bg-primary/10 text-primary">
              {icon}
            </div>
            <div>
              <h3 className="font-heading text-sm font-semibold text-foreground">{label}</h3>
              <p className="text-xs text-muted-foreground">{description}</p>
            </div>
          </div>
          <div className="text-right">
            <div className="font-mono text-lg font-semibold text-primary">
              {value.toFixed(step < 1 ? 1 : 0)}
            </div>
            <div className="text-xs text-muted-foreground">{unit}</div>
          </div>
        </div>

        <div className="relative pt-1">
          <Slider
            value={[value]}
            min={min}
            max={max}
            step={step}
            onValueChange={(vals) => onChange(vals[0])}
            onPointerEnter={() => setShowTooltip(true)}
            onPointerLeave={() => setShowTooltip(false)}
            className="relative"
            data-testid={`slider-${label.toLowerCase().replace(/\s+/g, '-')}`}
          />
          
          <div className="absolute top-0 left-0 w-full h-1 rounded-full bg-muted/30 -z-10" />
          <div 
            className="absolute top-0 left-0 h-1 rounded-full bg-gradient-to-r from-primary/50 to-primary transition-all duration-300"
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>
    </Card>
  );
}
