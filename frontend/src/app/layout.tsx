import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import { Cloud, History } from "lucide-react";
import "./globals.css";
import { Providers } from "@/lib/providers";
import { AboutBanner } from "@/components/AboutBanner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AI Weather Travel Advisor",
  description: "AI-powered weather search and travel recommendations by Brendan Lee",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-background text-foreground">
        <Providers>
          <nav className="border-b bg-background/80 backdrop-blur sticky top-0 z-10">
            <div className="container mx-auto px-4 h-14 flex items-center gap-6 max-w-5xl">
              <Link href="/" className="flex items-center gap-2 font-semibold text-sm">
                <Cloud className="h-5 w-5 text-blue-500" /> Weather Advisor
              </Link>
              <Link href="/history" className="flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors">
                <History className="h-4 w-4" /> History
              </Link>
            </div>
          </nav>
          <main className="flex-1">{children}</main>
          <AboutBanner />
        </Providers>
      </body>
    </html>
  );
}
