"use client";

import { useMutation } from "@tanstack/react-query";
import { api } from "@/services/apiClient";
import { ResolveLocationResponseSchema, type ResolveLocationResponse } from "@/types/weather";

export function useResolveLocation() {
  return useMutation<ResolveLocationResponse, Error, string>({
    mutationFn: async (query: string) => {
      const raw = await api.post<unknown>("/advice/resolve-location", { query });
      return ResolveLocationResponseSchema.parse(raw);
    },
  });
}
