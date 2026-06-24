import { z } from "zod";

// ── API error envelope ────────────────────────────────────────────────────────

export const ApiErrorSchema = z.object({
  detail: z.string(),
  code: z.string(),
  fields: z.record(z.array(z.string())).nullable().optional(),
});
export type ApiError = z.infer<typeof ApiErrorSchema>;

// ── Current weather ───────────────────────────────────────────────────────────

export const CurrentWeatherSchema = z.object({
  temperature: z.number(),
  feels_like: z.number().nullable().optional(),
  humidity: z.number().nullable().optional(),
  wind_speed: z.number().nullable().optional(),
  condition: z.string(),
  condition_code: z.number(),
  aqi: z.number().nullable().optional(),
  aqi_label: z.string().nullable().optional(),
});
export type CurrentWeather = z.infer<typeof CurrentWeatherSchema>;

export const ForecastDaySchema = z.object({
  date: z.string(),
  temp_min: z.number(),
  temp_max: z.number(),
  condition: z.string(),
  condition_code: z.number(),
  precipitation_sum: z.number().nullable().optional(),
  wind_speed_max: z.number().nullable().optional(),
});
export type ForecastDay = z.infer<typeof ForecastDaySchema>;

export const CurrentWeatherResponseSchema = z.object({
  resolved_location: z.string(),
  latitude: z.number(),
  longitude: z.number(),
  current: CurrentWeatherSchema,
  forecast: z.array(ForecastDaySchema),
});
export type CurrentWeatherResponse = z.infer<typeof CurrentWeatherResponseSchema>;

// ── Saved weather search ──────────────────────────────────────────────────────

export const WeatherSearchSchema = z.object({
  id: z.number(),
  location_query: z.string(),
  resolved_location_name: z.string(),
  latitude: z.string(),
  longitude: z.string(),
  start_date: z.string(),
  end_date: z.string(),
  weather_condition: z.string(),
  temperature: z.string(),
  humidity: z.number().nullable(),
  wind_speed: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});
export type WeatherSearch = z.infer<typeof WeatherSearchSchema>;

export const WeatherSearchListSchema = z.object({
  total: z.number(),
  items: z.array(WeatherSearchSchema),
});
export type WeatherSearchList = z.infer<typeof WeatherSearchListSchema>;

// ── Create / update forms ─────────────────────────────────────────────────────

export const CreateSearchFormSchema = z.object({
  location_query: z.string().min(1, "Location is required"),
  start_date: z.string().min(1, "Start date is required"),
  end_date: z.string().min(1, "End date is required"),
}).refine((d) => d.end_date >= d.start_date, {
  message: "End date must be on or after start date",
  path: ["end_date"],
});
export type CreateSearchForm = z.infer<typeof CreateSearchFormSchema>;

export const UpdateSearchFormSchema = z.object({
  location_query: z.string().min(1).optional(),
  start_date: z.string().optional(),
  end_date: z.string().optional(),
});
export type UpdateSearchForm = z.infer<typeof UpdateSearchFormSchema>;

// ── AI advice ────────────────────────────────────────────────────────────────

export const AdviceResponseSchema = z.object({
  clothing: z.array(z.string()),
  packing: z.array(z.string()),
  activities: z.array(z.string()),
  travel_considerations: z.array(z.string()),
  warnings: z.array(z.string()),
});
export type AdviceResponse = z.infer<typeof AdviceResponseSchema>;

// ── AQI ──────────────────────────────────────────────────────────────────────

export const AQIResponseSchema = z.object({
  aqi: z.number().nullable(),
  label: z.string(),
  pm2_5: z.number().nullable().optional(),
  pm10: z.number().nullable().optional(),
});
export type AQIResponse = z.infer<typeof AQIResponseSchema>;
