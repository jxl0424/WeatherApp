"use client";

import { useState } from "react";
import { Pencil, Trash2, Loader2, Download } from "lucide-react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter,
} from "@/components/ui/dialog";
import { ErrorMessage } from "@/components/ErrorMessage";
import { UpdateSearchFormSchema, type UpdateSearchForm, type WeatherSearch } from "@/types/weather";
import { useWeatherSearches, useDeleteSearch, useUpdateSearch } from "./useWeatherSearches";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export function SearchHistoryTable() {
  const { data, isLoading, isError, error } = useWeatherSearches();
  const deleteMutation = useDeleteSearch();
  const updateMutation = useUpdateSearch();
  const [editTarget, setEditTarget] = useState<WeatherSearch | null>(null);

  const { register, handleSubmit, reset, formState: { errors } } = useForm<UpdateSearchForm>({
    resolver: zodResolver(UpdateSearchFormSchema),
  });

  function openEdit(row: WeatherSearch) {
    setEditTarget(row);
    reset({
      location_query: row.location_query,
      start_date: row.start_date,
      end_date: row.end_date,
    });
  }

  function submitEdit(data: UpdateSearchForm) {
    if (!editTarget) return;
    updateMutation.mutate(
      { id: editTarget.id, data },
      { onSuccess: () => setEditTarget(null) },
    );
  }

  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorMessage error={error} title="Could not load history" />;
  if (!data?.items.length) return <p className="text-muted-foreground text-sm">No saved searches yet.</p>;

  return (
    <>
      <div className="flex justify-between items-center mb-3">
        <p className="text-sm text-muted-foreground">{data.total} saved searches</p>
        <div className="flex gap-2">
          {(["csv", "json", "md"] as const).map((fmt) => (
            <a key={fmt} href={`${BASE_URL}/weather/export?format=${fmt}`} download>
              <Button variant="outline" size="sm">
                <Download className="h-3 w-3 mr-1" /> {fmt.toUpperCase()}
              </Button>
            </a>
          ))}
        </div>
      </div>

      <div className="rounded-md border overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Location</TableHead>
              <TableHead>Dates</TableHead>
              <TableHead>Condition</TableHead>
              <TableHead>Temp</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.items.map((row) => (
              <TableRow key={row.id}>
                <TableCell>
                  <div className="font-medium">{row.resolved_location_name}</div>
                  <div className="text-xs text-muted-foreground">{row.location_query}</div>
                </TableCell>
                <TableCell className="text-sm">
                  {row.start_date} → {row.end_date}
                </TableCell>
                <TableCell>
                  <Badge variant="secondary">{row.weather_condition}</Badge>
                </TableCell>
                <TableCell>{Number(row.temperature).toFixed(1)}°C</TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="icon" onClick={() => openEdit(row)} title="Edit">
                    <Pencil className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => deleteMutation.mutate(row.id)}
                    disabled={deleteMutation.isPending}
                    title="Delete"
                    className="text-destructive hover:text-destructive"
                  >
                    {deleteMutation.isPending ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Trash2 className="h-4 w-4" />
                    )}
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* Edit dialog */}
      <Dialog open={!!editTarget} onOpenChange={(o) => !o && setEditTarget(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Search</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit(submitEdit)} className="space-y-4">
            <div>
              <Label htmlFor="edit_location">Location</Label>
              <Input id="edit_location" {...register("location_query")} />
              {errors.location_query && (
                <p className="text-destructive text-xs mt-1">{errors.location_query.message}</p>
              )}
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label htmlFor="edit_start">Start date</Label>
                <Input id="edit_start" type="date" {...register("start_date")} />
              </div>
              <div>
                <Label htmlFor="edit_end">End date</Label>
                <Input id="edit_end" type="date" {...register("end_date")} />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setEditTarget(null)}>
                Cancel
              </Button>
              <Button type="submit" disabled={updateMutation.isPending}>
                {updateMutation.isPending && <Loader2 className="h-4 w-4 animate-spin mr-2" />}
                Save changes
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </>
  );
}
