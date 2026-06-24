import { History } from "lucide-react";
import { SearchHistoryTable } from "@/features/history/SearchHistoryTable";

export const metadata = { title: "Search History — AI Weather Travel Advisor" };

export default function HistoryPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <header className="mb-6">
        <div className="flex items-center gap-2 mb-1">
          <History className="h-6 w-6 text-blue-500" />
          <h1 className="text-xl font-bold">Search History</h1>
        </div>
        <p className="text-muted-foreground text-sm">
          All saved weather searches. Edit dates and locations, delete records, or export the full dataset.
        </p>
      </header>
      <SearchHistoryTable />
    </div>
  );
}
