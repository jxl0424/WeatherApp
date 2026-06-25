"use client";

import { useState } from "react";

interface GeolocationState {
  loading: boolean;
  error: string | null;
  coords: { lat: number; lon: number } | null;
}

export function useGeolocation() {
  const [state, setState] = useState<GeolocationState>({
    loading: false,
    error: null,
    coords: null,
  });

  function reset() {
    setState({ loading: false, error: null, coords: null });
  }

  function locate() {
    if (!navigator.geolocation) {
      setState((s) => ({ ...s, error: "Geolocation is not supported by your browser." }));
      return;
    }
    setState({ loading: true, error: null, coords: null });
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => {
        setState({ loading: false, error: null, coords: { lat: coords.latitude, lon: coords.longitude } });
      },
      (err) => {
        setState({ loading: false, error: err.message, coords: null });
      },
    );
  }

  return { ...state, locate, reset };
}
