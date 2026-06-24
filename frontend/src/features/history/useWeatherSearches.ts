"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { api } from "@/services/apiClient";
import {
  WeatherSearchListSchema,
  type UpdateSearchForm,
  type WeatherSearch,
  type WeatherSearchList,
} from "@/types/weather";

export function useWeatherSearches(limit = 20, offset = 0) {
  return useQuery<WeatherSearchList>({
    queryKey: ["weatherSearches", limit, offset],
    queryFn: async () => {
      const raw = await api.get<unknown>(`/weather?limit=${limit}&offset=${offset}`);
      return WeatherSearchListSchema.parse(raw);
    },
  });
}

export function useDeleteSearch() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.delete(`/weather/${id}`),
    onSuccess: () => {
      toast.success("Deleted.");
      qc.invalidateQueries({ queryKey: ["weatherSearches"] });
    },
    onError: (err: Error) => toast.error(err.message),
  });
}

export function useUpdateSearch() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateSearchForm }) =>
      api.put<WeatherSearch>(`/weather/${id}`, data),
    onSuccess: () => {
      toast.success("Updated.");
      qc.invalidateQueries({ queryKey: ["weatherSearches"] });
    },
    onError: (err: Error) => toast.error(err.message),
  });
}
