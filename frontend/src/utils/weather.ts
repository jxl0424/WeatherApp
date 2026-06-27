// Maps WMO weather code to a Tailwind gradient class for the hero card.
export function wmoGradient(code: number): string {
  if (code === 0) return "from-amber-400 via-orange-300 to-sky-400";
  if (code <= 2) return "from-sky-500 to-blue-400";
  if (code <= 3) return "from-slate-500 to-slate-400";
  if (code <= 48) return "from-gray-600 to-slate-500";
  if (code <= 55) return "from-cyan-600 to-blue-500";
  if (code <= 65) return "from-blue-700 to-blue-900";
  if (code <= 75) return "from-slate-600 to-blue-400";
  if (code <= 82) return "from-blue-700 to-blue-900";
  return "from-purple-800 to-indigo-900";
}

// Maps WMO weather code to a Lucide icon name and color class.
export function wmoIcon(code: number): { icon: string; color: string } {
  if (code === 0) return { icon: "Sun", color: "text-yellow-400" };
  if (code <= 2) return { icon: "CloudSun", color: "text-yellow-300" };
  if (code === 3) return { icon: "Cloud", color: "text-gray-400" };
  if (code <= 48) return { icon: "CloudFog", color: "text-gray-400" };
  if (code <= 55) return { icon: "CloudDrizzle", color: "text-blue-400" };
  if (code <= 65) return { icon: "CloudRain", color: "text-blue-500" };
  if (code <= 75) return { icon: "Snowflake", color: "text-blue-200" };
  if (code <= 82) return { icon: "CloudRain", color: "text-blue-600" };
  return { icon: "CloudLightning", color: "text-purple-500" };
}

export function aqiColor(aqi: number | null | undefined): string {
  if (aqi == null) return "text-gray-400";
  if (aqi <= 50) return "text-green-500";
  if (aqi <= 100) return "text-yellow-500";
  if (aqi <= 150) return "text-orange-500";
  if (aqi <= 200) return "text-red-500";
  return "text-purple-700";
}

export function aqiBadgeVariant(aqi: number | null | undefined): "default" | "secondary" | "destructive" | "outline" {
  if (aqi == null || aqi <= 50) return "secondary";
  if (aqi <= 100) return "outline";
  return "destructive";
}

export function formatTemp(temp: number | string): string {
  const n = Number(temp);
  return `${n % 1 === 0 ? n : n.toFixed(1)}°C`;
}
