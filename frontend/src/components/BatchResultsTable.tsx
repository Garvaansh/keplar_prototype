import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Download,
  Search,
  ChevronUp,
  ChevronDown,
  Eye,
  FileSpreadsheet,
} from "lucide-react";

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

interface BatchResultsTableProps {
  results: BatchResult[];
  onRowClick: (result: BatchResult, index: number) => void;
}

export default function BatchResultsTable({
  results,
  onRowClick,
}: BatchResultsTableProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortColumn, setSortColumn] = useState<keyof BatchResult | null>(null);
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("desc");

  const handleSort = (column: keyof BatchResult) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("desc");
    }
  };

  const filteredAndSorted = results
    .filter((result) => {
      const searchLower = searchTerm.toLowerCase();
      return (
        result.prediction.toLowerCase().includes(searchLower) ||
        result.period.toString().includes(searchLower) ||
        result.confidence.toString().includes(searchLower)
      );
    })
    .sort((a, b) => {
      if (!sortColumn) return 0;
      const aVal = a[sortColumn];
      const bVal = b[sortColumn];

      // Handle undefined values
      if (aVal === undefined && bVal === undefined) return 0;
      if (aVal === undefined) return 1;
      if (bVal === undefined) return -1;

      const multiplier = sortDirection === "asc" ? 1 : -1;
      return aVal > bVal ? multiplier : -multiplier;
    });

  const downloadResults = () => {
    const headers = [
      "Period (days)",
      "Depth (ppm)",
      "Duration (hrs)",
      "Classification",
      "Confidence",
    ];
    const csv = [
      headers.join(","),
      ...results.map((r) =>
        [
          r.period,
          r.depth,
          r.duration,
          r.prediction,
          (r.confidence * 100).toFixed(1) + "%",
        ].join(",")
      ),
    ].join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `predictions_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const getClassificationColor = (prediction: string) => {
    switch (prediction) {
      case "CONFIRMED":
        return "bg-confirmed/20 text-confirmed border-confirmed";
      case "CANDIDATE":
        return "bg-candidate/20 text-candidate border-candidate";
      case "FALSE POSITIVE":
        return "bg-false-positive/20 text-false-positive border-false-positive";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const SortIcon = ({ column }: { column: keyof BatchResult }) => {
    if (sortColumn !== column) return null;
    return sortDirection === "asc" ? (
      <ChevronUp className="w-4 h-4" />
    ) : (
      <ChevronDown className="w-4 h-4" />
    );
  };

  return (
    <Card className="p-6 border-primary/20 bg-card/50 backdrop-blur-sm">
      <div className="space-y-4">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <FileSpreadsheet className="w-5 h-5 text-primary" />
            <h3 className="font-heading text-lg font-semibold">
              Batch Results ({results.length})
            </h3>
          </div>
          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search results..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-9 w-64"
              />
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={downloadResults}
              className="gap-2"
            >
              <Download className="w-4 h-4" />
              Export
            </Button>
          </div>
        </div>

        <div className="rounded-lg border border-border overflow-hidden">
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow className="bg-muted/50">
                  <TableHead className="w-[100px]">#</TableHead>
                  <TableHead
                    className="cursor-pointer select-none hover:bg-muted/50"
                    onClick={() => handleSort("period")}
                  >
                    <div className="flex items-center gap-1">
                      Period (days)
                      <SortIcon column="period" />
                    </div>
                  </TableHead>
                  <TableHead
                    className="cursor-pointer select-none hover:bg-muted/50"
                    onClick={() => handleSort("depth")}
                  >
                    <div className="flex items-center gap-1">
                      Depth (ppm)
                      <SortIcon column="depth" />
                    </div>
                  </TableHead>
                  <TableHead
                    className="cursor-pointer select-none hover:bg-muted/50"
                    onClick={() => handleSort("duration")}
                  >
                    <div className="flex items-center gap-1">
                      Duration (hrs)
                      <SortIcon column="duration" />
                    </div>
                  </TableHead>
                  <TableHead
                    className="cursor-pointer select-none hover:bg-muted/50"
                    onClick={() => handleSort("prediction")}
                  >
                    <div className="flex items-center gap-1">
                      Classification
                      <SortIcon column="prediction" />
                    </div>
                  </TableHead>
                  <TableHead
                    className="cursor-pointer select-none hover:bg-muted/50"
                    onClick={() => handleSort("confidence")}
                  >
                    <div className="flex items-center gap-1">
                      Confidence
                      <SortIcon column="confidence" />
                    </div>
                  </TableHead>
                  <TableHead className="w-[100px] text-right">Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredAndSorted.length === 0 ? (
                  <TableRow>
                    <TableCell
                      colSpan={7}
                      className="text-center py-8 text-muted-foreground"
                    >
                      No results found
                    </TableCell>
                  </TableRow>
                ) : (
                  filteredAndSorted.map((result, index) => (
                    <TableRow
                      key={index}
                      className="cursor-pointer hover:bg-muted/30 transition-colors"
                      onClick={() => onRowClick(result, index)}
                    >
                      <TableCell className="font-mono text-muted-foreground">
                        {index + 1}
                      </TableCell>
                      <TableCell className="font-mono">
                        {result.period.toFixed(2)}
                      </TableCell>
                      <TableCell className="font-mono">
                        {result.depth.toFixed(0)}
                      </TableCell>
                      <TableCell className="font-mono">
                        {result.duration.toFixed(2)}
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant="outline"
                          className={`${getClassificationColor(
                            result.prediction
                          )} text-xs`}
                        >
                          {result.prediction}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <div className="flex-1 bg-muted rounded-full h-2 overflow-hidden">
                            <div
                              className="bg-primary h-full transition-all"
                              style={{ width: `${result.confidence * 100}%` }}
                            />
                          </div>
                          <span className="font-mono text-sm min-w-[45px]">
                            {(result.confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="gap-1"
                          onClick={(e) => {
                            e.stopPropagation();
                            onRowClick(result, index);
                          }}
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </div>
      </div>
    </Card>
  );
}
