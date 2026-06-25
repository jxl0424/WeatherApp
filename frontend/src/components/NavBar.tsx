"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Cloud, History } from "lucide-react";
import { cn } from "@/lib/utils";

export function NavBar() {
  const pathname = usePathname();

  return (
    <nav className="border-b bg-background/80 backdrop-blur sticky top-0 z-10">
      <div className="container mx-auto px-4 h-14 flex items-center gap-6 max-w-5xl">
        <Link
          href="/"
          className={cn(
            "flex items-center gap-2 text-sm font-semibold transition-colors",
            pathname === "/" ? "text-foreground" : "text-muted-foreground hover:text-foreground",
          )}
        >
          <Cloud className="h-5 w-5 text-blue-500" /> Weather Advisor
        </Link>
        <Link
          href="/history"
          className={cn(
            "flex items-center gap-1 text-sm transition-colors",
            pathname === "/history" ? "text-foreground font-medium" : "text-muted-foreground hover:text-foreground",
          )}
        >
          <History className="h-4 w-4" /> History
        </Link>
      </div>
    </nav>
  );
}
