import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  Zap,
  Loader2,
} from "lucide-react";

type Classification = "CONFIRMED" | "CANDIDATE" | "FALSE POSITIVE";

interface AIClassificationCardProps {
  classification: Classification;
  confidence: number;
  isLoading?: boolean;
}

const classificationConfig = {
  CONFIRMED: {
    icon: CheckCircle,
    color: "confirmed",
    bgColor: "bg-confirmed/10",
    borderColor: "border-confirmed/30",
    textColor: "text-confirmed",
    label: "CONFIRMED",
    description: "High-confidence exoplanet detection",
  },
  CANDIDATE: {
    icon: AlertTriangle,
    color: "candidate",
    bgColor: "bg-candidate/10",
    borderColor: "border-candidate/30",
    textColor: "text-candidate",
    label: "CANDIDATE",
    description: "Potential exoplanet requiring further analysis",
  },
  "FALSE POSITIVE": {
    icon: XCircle,
    color: "false-positive",
    bgColor: "bg-false-positive/10",
    borderColor: "border-false-positive/30",
    textColor: "text-false-positive",
    label: "FALSE POSITIVE",
    description: "Not an exoplanet",
  },
};

export default function AIClassificationCard({
  classification,
  confidence,
  isLoading = false,
}: AIClassificationCardProps) {
  const config = classificationConfig[classification];
  const Icon = config.icon;

  return (
    <Card
      className={`p-4 border-2 ${config.borderColor} ${config.bgColor} backdrop-blur-sm animate-fade-in`}
    >
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <div className={`p-1.5 rounded-md ${config.bgColor}`}>
            <Zap className="w-4 h-4 text-primary" />
          </div>
          <div>
            <h3 className="font-heading text-base font-semibold text-foreground">
              AI Classification
            </h3>
            <p className="text-xs text-muted-foreground">
              Real-time analysis result
            </p>
          </div>
        </div>

        <div className="flex items-center justify-center py-4">
          <div className="relative">
            <div
              className={`absolute inset-0 ${config.bgColor} rounded-full blur-xl opacity-50 animate-glow-pulse`}
            />
            {isLoading ? (
              <Loader2 className="w-16 h-16 text-primary relative z-10 animate-spin" />
            ) : (
              <Icon className={`w-16 h-16 ${config.textColor} relative z-10`} />
            )}
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Badge
              variant="outline"
              className={`${config.bgColor} ${config.textColor} border-current text-sm px-3 py-1 font-semibold`}
              data-testid="classification-badge"
            >
              {config.label}
            </Badge>
            <span className={`font-mono text-xl font-bold ${config.textColor}`}>
              {(confidence * 100).toFixed(1)}%
            </span>
          </div>

          <Progress
            value={confidence * 100}
            className="h-2"
            data-testid="confidence-progress"
          />

          <p className="text-xs text-center text-muted-foreground pt-1">
            {config.description}
          </p>
        </div>
      </div>
    </Card>
  );
}
