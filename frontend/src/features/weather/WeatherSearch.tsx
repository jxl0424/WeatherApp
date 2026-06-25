"use client";

import { useState } from "react";
import { MapPin, Search, Loader2, Navigation, CloudSun } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useGeolocation } from "@/hooks/useGeolocation";
import { useCurrentWeather } from "./useCurrentWeather";
import { WeatherCard } from "./WeatherCard";
import { ForecastGrid } from "@/features/forecast/ForecastGrid";
import { AdvicePanel } from "@/features/advice/AdvicePanel";
import { SaveSearchForm } from "@/features/history/SaveSearchForm";
import { ErrorMessage } from "@/components/ErrorMessage";

export function WeatherSearch() {
  const [inputValue, setInputValue] = useState("");
  const [submittedLocation, setSubmittedLocation] = useState("");
  const geo = useGeolocation();

  const locationQuery = useCurrentWeather({
    location: submittedLocation || undefined,
    enabled: !!submittedLocation,
  });

  const geoQuery = useCurrentWeather({
    lat: geo.coords?.lat,
    lon: geo.coords?.lon,
    enabled: !!geo.coords,
  });

  const activeQuery = geo.coords ? geoQuery : locationQuery;
  const weatherData = activeQuery.data;

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = inputValue.trim();
    if (!trimmed) return;
    geo.reset();
    setSubmittedLocation(trimmed);
  }

  function handleLocate() {
    setSubmittedLocation("");
    setInputValue("");
    geo.locate();
  }

  return (
    <div className="space-y-6">
      {/* Search bar */}
      <form onSubmit={handleSearch} className="flex gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            className="pl-9"
            placeholder="City, zip code, landmark, GPS coordinates…"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            aria-label="Location search"
          />
        </div>
        <Button type="submit" disabled={!inputValue.trim()}>
          Search
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={handleLocate}
          disabled={geo.loading}
          title="Use my current location"
        >
          {geo.loading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Navigation className="h-4 w-4" />
          )}
        </Button>
      </form>

      {/* Geolocation error */}
      {geo.error && (
        <ErrorMessage error={new Error(geo.error)} title="Location access denied" />
      )}

      {/* Loading */}
      {activeQuery.isLoading && (
        <div className="flex items-center gap-2 text-muted-foreground animate-pulse">
          <Loader2 className="h-4 w-4 animate-spin" />
          Fetching weather…
        </div>
      )}

      {/* API error */}
      {activeQuery.isError && (
        <ErrorMessage error={activeQuery.error} title="Could not load weather" />
      )}

      {/* Empty state */}
      {!weatherData && !activeQuery.isLoading && !activeQuery.isError && !geo.error && (
        <div className="flex flex-col items-center gap-3 py-16 text-muted-foreground">
          <CloudSun className="h-12 w-12 opacity-30" />
          <p className="text-sm">Search a city, landmark, or use your current location to get started.</p>
        </div>
      )}

      {/* Results */}
      {weatherData && (
        <div className="space-y-6">
          <div className="flex items-center gap-2 text-muted-foreground text-sm">
            <MapPin className="h-3 w-3" />
            {weatherData.resolved_location}
          </div>
          <WeatherCard current={weatherData.current} />
          <ForecastGrid forecast={weatherData.forecast} />
          <div className="grid md:grid-cols-2 gap-4">
            <SaveSearchForm resolvedLocation={weatherData.resolved_location} />
            <AdvicePanel key={weatherData.resolved_location} weatherData={weatherData} />
          </div>
        </div>
      )}
    </div>
  );
}
