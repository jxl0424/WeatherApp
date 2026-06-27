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
      <div className="rounded-lg bg-sky-50 dark:bg-sky-950/20 border border-sky-100 dark:border-sky-900/30 px-4 py-3 flex gap-3 items-start">
        <Sparkles className="h-4 w-4 mt-0.5 shrink-0 text-sky-400" />
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
    <div className="rounded-lg bg-sky-50 dark:bg-sky-950/20 border border-sky-100 dark:border-sky-900/30 px-4 py-3 flex gap-3 items-start">
      <Sparkles className="h-4 w-4 mt-0.5 shrink-0 text-sky-500" />
      <p className="leading-relaxed text-sm italic text-foreground/80">{data.summary}</p>
    </div>
  );
}
