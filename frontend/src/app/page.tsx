import { Cloud } from "lucide-react";
import { WeatherSearch } from "@/features/weather/WeatherSearch";

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <header className="mb-8">
        <div className="flex items-center gap-3 mb-1">
          <Cloud className="h-8 w-8 text-blue-500" />
          <h1 className="text-2xl font-bold">AI Weather Travel Advisor</h1>
        </div>
        <p className="text-muted-foreground text-sm">
          Search any location for current weather, a 5-day forecast, air quality, and AI-powered travel advice.
        </p>
      </header>
      <WeatherSearch />
    </div>
  );
}
