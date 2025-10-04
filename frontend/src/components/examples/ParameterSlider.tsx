import { useState } from "react";
import ParameterSlider from "../ParameterSlider";
import { Orbit } from "lucide-react";

export default function ParameterSliderExample() {
  const [value, setValue] = useState(15);

  return (
    <div className="w-full max-w-2xl">
      <ParameterSlider
        label="Orbital Period"
        value={value}
        min={0.5}
        max={100}
        step={0.5}
        unit="days"
        description="How often the planet transits"
        icon={<Orbit className="w-5 h-5" />}
        onChange={setValue}
      />
    </div>
  );
}
