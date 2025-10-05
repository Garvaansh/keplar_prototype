import { useState } from "react";
import {
  Upload,
  Download,
  FileSpreadsheet,
  AlertCircle,
  CheckCircle2,
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface BatchUploadProps {
  onBatchComplete: (results: any[]) => void;
}

export default function BatchUpload({ onBatchComplete }: BatchUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string>("");

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      await processFile(file);
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await processFile(file);
    }
  };

  const processFile = async (file: File) => {
    if (!file.name.endsWith(".csv")) {
      setError("Please upload a CSV file");
      return;
    }

    setFileName(file.name);
    setError(null);
    setIsProcessing(true);
    setProgress(0);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        "http://localhost:8000/api/v1/batch-predict",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Batch processing failed");
      }

      // Simulate progress (since backend doesn't stream progress)
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 200);

      const result = await response.json();
      clearInterval(progressInterval);
      setProgress(100);

      // Pass results to parent (backend returns 'results' array)
      onBatchComplete(result.results || []);

      setTimeout(() => {
        setIsProcessing(false);
        setProgress(0);
        setFileName("");
      }, 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to process file");
      setIsProcessing(false);
      setProgress(0);
    }
  };

  const downloadTemplate = () => {
    const template = `koi_period,koi_depth,koi_duration,koi_impact,koi_model_snr
15.5,5000,3.5,0.5,50
87.3,2500,4.2,0.3,45
1.2,8000,2.1,0.7,65
365.25,3000,5.5,0.4,55`;

    const blob = new Blob([template], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "exoplanet_template.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Card className="p-6 border-primary/20 bg-card/50 backdrop-blur-sm">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileSpreadsheet className="w-5 h-5 text-primary" />
            <h3 className="font-heading text-lg font-semibold">
              Batch Processing
            </h3>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={downloadTemplate}
            className="gap-2"
          >
            <Download className="w-4 h-4" />
            Download Template
          </Button>
        </div>

        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center transition-all
            ${
              isDragging
                ? "border-primary bg-primary/5 scale-[1.02]"
                : "border-border hover:border-primary/50"
            }
            ${
              isProcessing ? "pointer-events-none opacity-60" : "cursor-pointer"
            }
          `}
        >
          <input
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            className="hidden"
            id="csv-upload"
            disabled={isProcessing}
          />

          <label htmlFor="csv-upload" className="cursor-pointer">
            {isProcessing ? (
              <div className="space-y-3">
                <div className="flex justify-center">
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                    <Upload className="w-6 h-6 text-primary animate-pulse" />
                  </div>
                </div>
                <p className="text-sm text-muted-foreground">
                  Processing {fileName}...
                </p>
                <Progress value={progress} className="h-2" />
                <p className="text-xs text-muted-foreground">
                  {progress}% complete
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                <div className="flex justify-center">
                  <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                    <Upload className="w-6 h-6 text-primary" />
                  </div>
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground">
                    Drop CSV file here or click to browse
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Upload exoplanet data for batch predictions
                  </p>
                </div>
              </div>
            )}
          </label>
        </div>

        {error && (
          <div className="flex items-center gap-2 p-3 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive text-sm">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {progress === 100 && !error && (
          <div className="flex items-center gap-2 p-3 bg-confirmed/10 border border-confirmed/20 rounded-lg text-confirmed text-sm animate-fade-in">
            <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
            <span>Batch processing completed successfully!</span>
          </div>
        )}
      </div>
    </Card>
  );
}
