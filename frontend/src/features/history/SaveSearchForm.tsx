"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { BookmarkPlus, Loader2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { api } from "@/services/apiClient";
import { CreateSearchFormSchema, type CreateSearchForm, type WeatherSearch } from "@/types/weather";

interface Props {
  locationQuery: string;
}

export function SaveSearchForm({ locationQuery }: Props) {
  const qc = useQueryClient();
  const { register, handleSubmit, formState: { errors }, reset } = useForm<CreateSearchForm>({
    resolver: zodResolver(CreateSearchFormSchema),
    defaultValues: { location_query: locationQuery },
  });

  const mutation = useMutation({
    mutationFn: (data: CreateSearchForm) =>
      api.post<WeatherSearch>("/weather", data),
    onSuccess: () => {
      toast.success("Search saved!");
      qc.invalidateQueries({ queryKey: ["weatherSearches"] });
      reset({ location_query: locationQuery });
    },
    onError: (err: Error) => toast.error(err.message),
  });

  const today = new Date().toISOString().split("T")[0];

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-base flex items-center gap-2">
          <BookmarkPlus className="h-4 w-4" /> Save Search
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit((d) => mutation.mutate(d))} className="space-y-3">
          <div>
            <Label htmlFor="location_query">Location</Label>
            <Input id="location_query" {...register("location_query")} />
            {errors.location_query && (
              <p className="text-destructive text-xs mt-1">{errors.location_query.message}</p>
            )}
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <Label htmlFor="start_date">Start date</Label>
              <Input id="start_date" type="date" defaultValue={today} min={today} {...register("start_date")} />
              {errors.start_date && (
                <p className="text-destructive text-xs mt-1">{errors.start_date.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="end_date">End date</Label>
              <Input id="end_date" type="date" defaultValue={today} min={today} {...register("end_date")} />
              {errors.end_date && (
                <p className="text-destructive text-xs mt-1">{errors.end_date.message}</p>
              )}
            </div>
          </div>
          <Button type="submit" className="w-full" disabled={mutation.isPending}>
            {mutation.isPending && <Loader2 className="h-4 w-4 animate-spin mr-2" />}
            Save
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
