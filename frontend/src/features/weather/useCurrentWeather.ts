"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/services/apiClient";
import { CurrentWeatherResponseSchema, type CurrentWeatherResponse } from "@/types/weather";

interface Params {
  location?: string;
  lat?: number;
  lon?: number;
  enabled?: boolean;
}

export function useCurrentWeather({ location, lat, lon, enabled = true }: Params) {
  const params = new URLSearchParams();
  if (location) params.set("location", location);
  if (lat != null) params.set("lat", String(lat));
  if (lon != null) params.set("lon", String(lon));

  return useQuery<CurrentWeatherResponse>({
    queryKey: ["currentWeather", location, lat, lon],
    queryFn: async () => {
      const raw = await api.get<unknown>(`/weather/current?${params}`);
      return CurrentWeatherResponseSchema.parse(raw);
    },
    enabled: enabled && (!!location || (lat != null && lon != null)),
  });
}
