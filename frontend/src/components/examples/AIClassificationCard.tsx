import { useState } from "react";
import AIClassificationCard from "../AIClassificationCard";
import { Button } from "@/components/ui/button";

export default function AIClassificationCardExample() {
  const [index, setIndex] = useState(0);
  
  const examples = [
    { classification: "CONFIRMED" as const, confidence: 0.94 },
    { classification: "CANDIDATE" as const, confidence: 0.67 },
    { classification: "FALSE POSITIVE" as const, confidence: 0.82 },
  ];

  return (
    <div className="w-full max-w-md space-y-4">
      <AIClassificationCard {...examples[index]} />
      <div className="flex justify-center">
        <Button
          onClick={() => setIndex((i) => (i + 1) % examples.length)}
          variant="outline"
          size="sm"
        >
          Next Classification
        </Button>
      </div>
    </div>
  );
}
