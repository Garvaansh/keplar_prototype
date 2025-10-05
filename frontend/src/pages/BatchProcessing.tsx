import { useState } from "react";
import { Telescope, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import BatchUpload from "@/components/BatchUpload";
import BatchResultsTable from "@/components/BatchResultsTable";
import BatchDetailView from "@/components/BatchDetailView";
import StarryBackground from "@/components/StarryBackground";

interface BatchResult {
  id: number;
  row: number;
  prediction: string;
  confidence: number;
  period: number;
  depth: number;
  duration: number;
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
}

export default function BatchProcessing() {
  const [results, setResults] = useState<BatchResult[]>([]);
  const [selectedResult, setSelectedResult] = useState<{
    result: BatchResult;
    index: number;
  } | null>(null);

  const handleBatchComplete = (batchResults: any[]) => {
    setResults(batchResults);
  };

  const handleRowClick = (result: BatchResult, index: number) => {
    setSelectedResult({ result, index });
  };

  const handleCloseDetail = () => {
    setSelectedResult(null);
  };

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
                    Batch Processing
                  </h1>
                  <p className="text-sm text-muted-foreground">
                    Upload CSV files for bulk exoplanet predictions
                  </p>
                </div>
              </div>
              <Button
                variant="outline"
                className="gap-2"
                onClick={() => window.history.back()}
              >
                <ArrowLeft className="w-4 h-4" />
                Back to Dashboard
              </Button>
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-6 space-y-6">
          <BatchUpload onBatchComplete={handleBatchComplete} />

          {results.length > 0 && (
            <BatchResultsTable results={results} onRowClick={handleRowClick} />
          )}
        </main>
      </div>

      {selectedResult && (
        <BatchDetailView
          result={selectedResult.result}
          index={selectedResult.index}
          onClose={handleCloseDetail}
        />
      )}
    </div>
  );
}
