"use client";

import * as LucideIcons from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import type { ForecastDay } from "@/types/weather";
import { wmoIcon, formatTemp } from "@/utils/weather";

interface Props {
  forecast: ForecastDay[];
}

export function ForecastGrid({ forecast }: Props) {
  const days = forecast.slice(0, 5);

  return (
    <div>
      <h2 className="text-sm font-medium text-muted-foreground mb-3">5-Day Forecast</h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
        {days.map((day) => (
          <ForecastCard key={day.date} day={day} />
        ))}
      </div>
    </div>
  );
}

function ForecastCard({ day }: { day: ForecastDay }) {
  const { icon, color } = wmoIcon(day.condition_code);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const Icon = (LucideIcons as any)[icon] as React.ElementType;

  const label = new Date(day.date + "T12:00:00Z").toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  });

  return (
    <Card className="text-center">
      <CardContent className="pt-4 pb-3 px-2 flex flex-col items-center gap-1">
        <p className="text-xs text-muted-foreground font-medium">{label}</p>
        {Icon && <Icon className={`h-6 w-6 ${color} my-1`} />}
        <p className="text-xs text-muted-foreground">{day.condition}</p>
        <div className="flex gap-2 text-sm font-semibold mt-1">
          <span>{formatTemp(day.temp_max)}</span>
          <span className="text-muted-foreground font-normal">{formatTemp(day.temp_min)}</span>
        </div>
        {(day.precipitation_sum ?? 0) > 0 && (
          <p className="text-xs text-blue-500">{day.precipitation_sum}mm rain</p>
        )}
      </CardContent>
    </Card>
  );
}
