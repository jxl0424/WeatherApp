"use client";

import { Sparkles } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { useWeatherSummary } from "@/features/weather/useWeatherSummary";
import type { CurrentWeatherResponse } from "@/types/weather";

interface Props {
  weatherData: CurrentWeatherResponse;
}

export function WeatherSummary({ weatherData }: Props) {
  const { data, isLoading } = useWeatherSummary(weatherData);

  if (isLoading) {
    return (
      <div className="flex gap-2 items-start text-sm text-muted-foreground">
        <Sparkles className="h-4 w-4 mt-0.5 shrink-0 text-yellow-500" />
        <div className="space-y-1.5 flex-1">
          <Skeleton className="h-3 w-full" />
          <Skeleton className="h-3 w-5/6" />
          <Skeleton className="h-3 w-4/6" />
        </div>
      </div>
    );
  }

  if (!data?.summary) return null;

  return (
    <div className="flex gap-2 items-start text-sm text-muted-foreground">
      <Sparkles className="h-4 w-4 mt-0.5 shrink-0 text-yellow-500" />
      <p className="leading-relaxed">{data.summary}</p>
    </div>
  );
}
