"use client";

import { useEffect } from "react";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/sonner";
import { queryClient } from "./queryClient";
import { api } from "@/services/apiClient";

function BackendWarmup() {
  useEffect(() => {
    api.get("/health").catch(() => {});
  }, []);
  return null;
}

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <BackendWarmup />
      {children}
      <Toaster richColors position="top-right" />
    </QueryClientProvider>
  );
}
