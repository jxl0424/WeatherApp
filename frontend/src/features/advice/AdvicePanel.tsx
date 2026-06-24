"use client";

import { useState } from "react";
import { Sparkles, Loader2, Shirt, Backpack, MapPin, AlertTriangle, Activity } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api } from "@/services/apiClient";
import { AdviceResponseSchema, type AdviceResponse, type CurrentWeatherResponse } from "@/types/weather";
import { ErrorMessage } from "@/components/ErrorMessage";

interface Props {
  weatherData: CurrentWeatherResponse;
}

export function AdvicePanel({ weatherData }: Props) {
  const [advice, setAdvice] = useState<AdviceResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);

  async function generate() {
    setLoading(true);
    setError(null);
    try {
      const raw = await api.post<unknown>("/advice", {
        location: weatherData.resolved_location,
        current: weatherData.current,
        forecast: weatherData.forecast.slice(0, 5),
      });
      setAdvice(AdviceResponseSchema.parse(raw));
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-base flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-yellow-500" /> AI Travel Advisor
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <Button onClick={generate} disabled={loading} className="w-full">
          {loading ? (
            <><Loader2 className="h-4 w-4 animate-spin mr-2" /> Generating advice…</>
          ) : (
            <><Sparkles className="h-4 w-4 mr-2" /> Get Travel Advice</>
          )}
        </Button>

        {error != null && <ErrorMessage error={error} title="AI advisor unavailable" />}

        {advice && (
          <div className="space-y-3 text-sm">
            <AdviceSection icon={<Shirt className="h-3 w-3" />} title="Clothing" items={advice.clothing} />
            <AdviceSection icon={<Backpack className="h-3 w-3" />} title="Packing" items={advice.packing} />
            <AdviceSection icon={<Activity className="h-3 w-3" />} title="Activities" items={advice.activities} />
            <AdviceSection icon={<MapPin className="h-3 w-3" />} title="Travel Tips" items={advice.travel_considerations} />
            {advice.warnings.length > 0 && (
              <AdviceSection icon={<AlertTriangle className="h-3 w-3 text-destructive" />} title="Warnings" items={advice.warnings} variant="warning" />
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function AdviceSection({
  icon, title, items, variant,
}: {
  icon: React.ReactNode;
  title: string;
  items: string[];
  variant?: "warning";
}) {
  if (!items.length) return null;
  return (
    <div>
      <p className={`font-medium flex items-center gap-1 mb-1 ${variant === "warning" ? "text-destructive" : ""}`}>
        {icon} {title}
      </p>
      <ul className="space-y-1">
        {items.map((item, i) => (
          <li key={i} className="flex gap-2 text-muted-foreground">
            <span className="text-primary">•</span> {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
