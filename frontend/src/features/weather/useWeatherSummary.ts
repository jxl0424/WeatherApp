"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/services/apiClient";
import { WeatherSummaryResponseSchema, type CurrentWeatherResponse, type WeatherSummaryResponse } from "@/types/weather";

export function useWeatherSummary(weatherData: CurrentWeatherResponse | undefined) {
  return useQuery<WeatherSummaryResponse>({
    queryKey: ["weatherSummary", weatherData?.resolved_location],
    queryFn: async () => {
      const raw = await api.post<unknown>("/advice/summary", {
        location: weatherData!.resolved_location,
        current: weatherData!.current,
        forecast: weatherData!.forecast.slice(0, 5),
      });
      return WeatherSummaryResponseSchema.parse(raw);
    },
    enabled: !!weatherData,
    staleTime: 5 * 60 * 1000,
  });
}
