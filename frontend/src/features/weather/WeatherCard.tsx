"use client";

import * as LucideIcons from "lucide-react";
import { Wind, Droplets, Eye } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { CurrentWeather } from "@/types/weather";
import { wmoIcon, aqiBadgeVariant, formatTemp } from "@/utils/weather";

interface Props {
  current: CurrentWeather;
}

export function WeatherCard({ current }: Props) {
  const { icon, color } = wmoIcon(current.condition_code);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const Icon = (LucideIcons as any)[icon] as React.ElementType;

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-3 text-3xl">
          {Icon && <Icon className={`h-10 w-10 ${color}`} />}
          <span>{formatTemp(current.temperature)}</span>
          <span className="text-base font-normal text-muted-foreground ml-2">{current.condition}</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
          {current.feels_like != null && (
            <Stat label="Feels like" value={formatTemp(current.feels_like)} />
          )}
          {current.humidity != null && (
            <Stat label="Humidity" value={`${current.humidity}%`} icon={<Droplets className="h-3 w-3" />} />
          )}
          {current.wind_speed != null && (
            <Stat label="Wind" value={`${current.wind_speed} km/h`} icon={<Wind className="h-3 w-3" />} />
          )}
          {current.aqi != null && (
            <div className="flex flex-col gap-1">
              <span className="text-muted-foreground flex items-center gap-1">
                <Eye className="h-3 w-3" /> Air Quality
              </span>
              <div className="flex items-center gap-1.5">
                <Badge variant={aqiBadgeVariant(current.aqi)}>{current.aqi_label}</Badge>
                <span className="text-xs text-muted-foreground">AQI {current.aqi}</span>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

function Stat({ label, value, icon }: { label: string; value: string; icon?: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-1">
      <span className="text-muted-foreground flex items-center gap-1">{icon}{label}</span>
      <span className="font-semibold">{value}</span>
    </div>
  );
}
