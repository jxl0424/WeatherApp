import { WeatherSearch } from "@/features/weather/WeatherSearch";

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <WeatherSearch />
    </div>
  );
}
