"use client";

import * as LucideIcons from "lucide-react";
import { Wind, Droplets, Eye, Thermometer } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import type { CurrentWeather } from "@/types/weather";
import { wmoIcon, wmoGradient, formatTemp } from "@/utils/weather";

interface Props {
  current: CurrentWeather;
}

export function WeatherCard({ current }: Props) {
  const { icon } = wmoIcon(current.condition_code);
  const gradient = wmoGradient(current.condition_code);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const Icon = (LucideIcons as any)[icon] as React.ElementType;

  return (
    <Card className={`bg-gradient-to-br ${gradient} border-0 shadow-xl overflow-hidden`}>
      <CardContent className="pt-7 pb-6 px-6">
        <div className="flex items-start justify-between mb-6">
          {Icon && <Icon className="h-20 w-20 text-white/90 drop-shadow" />}
          <div className="text-right text-white">
            <p className="text-6xl font-bold leading-none drop-shadow">{formatTemp(current.temperature)}</p>
            <p className="text-lg text-white/80 mt-1">{current.condition}</p>
          </div>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {current.feels_like != null && (
            <StatPill icon={<Thermometer className="h-3 w-3" />} label="Feels like" value={formatTemp(current.feels_like)} />
          )}
          {current.humidity != null && (
            <StatPill icon={<Droplets className="h-3 w-3" />} label="Humidity" value={`${current.humidity}%`} />
          )}
          {current.wind_speed != null && (
            <StatPill icon={<Wind className="h-3 w-3" />} label="Wind" value={`${current.wind_speed} km/h`} />
          )}
          {current.aqi != null && (
            <div className="bg-white/15 rounded-xl px-3 py-2.5 text-white">
              <p className="text-xs text-white/70 flex items-center gap-1 mb-1">
                <Eye className="h-3 w-3" /> Air Quality
              </p>
              <p className="font-semibold text-sm">{current.aqi_label}</p>
              <p className="text-xs text-white/60">AQI {current.aqi}</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

function StatPill({ label, value, icon }: { label: string; value: string; icon: React.ReactNode }) {
  return (
    <div className="bg-white/15 rounded-xl px-3 py-2.5 text-white">
      <p className="text-xs text-white/70 flex items-center gap-1 mb-1">{icon}{label}</p>
      <p className="font-semibold text-sm">{value}</p>
    </div>
  );
}
