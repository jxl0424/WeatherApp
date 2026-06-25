"use client";

import { useRef, useState, useEffect } from "react";
import { MessageCircle, Send, Loader2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/services/apiClient";
import { ChatResponseSchema, type ChatMessage, type CurrentWeatherResponse } from "@/types/weather";
import { ErrorMessage } from "@/components/ErrorMessage";

const SUGGESTIONS = [
  "What should I wear today?",
  "Best day this week for outdoor activities?",
  "Is it safe to travel in this weather?",
  "Will it rain this weekend?",
];

interface Props {
  weatherData: CurrentWeatherResponse;
}

export function WeatherChat({ weatherData }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send(text: string) {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    const userMsg: ChatMessage = { role: "user", content: trimmed };
    const nextHistory = [...messages, userMsg];
    setMessages(nextHistory);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      const raw = await api.post<unknown>("/advice/chat", {
        location: weatherData.resolved_location,
        current: weatherData.current,
        forecast: weatherData.forecast.slice(0, 5),
        history: messages,
        message: trimmed,
      });
      const { reply } = ChatResponseSchema.parse(raw);
      setMessages([...nextHistory, { role: "assistant", content: reply }]);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    send(input);
  }

  return (
    <Card className="flex flex-col">
      <CardHeader className="pb-2">
        <CardTitle className="text-base flex items-center gap-2">
          <MessageCircle className="h-4 w-4 text-blue-500" /> Weather Chat
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        {/* Suggestion chips — shown until first message */}
        {messages.length === 0 && (
          <div className="flex flex-wrap gap-1.5">
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => send(s)}
                className="text-xs px-2.5 py-1 rounded-full border border-border bg-muted/50 hover:bg-muted transition-colors text-muted-foreground hover:text-foreground"
              >
                {s}
              </button>
            ))}
          </div>
        )}

        {/* Message list */}
        {messages.length > 0 && (
          <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[85%] rounded-lg px-3 py-2 text-sm leading-relaxed ${
                    msg.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-foreground"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-muted rounded-lg px-3 py-2">
                  <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        )}

        {error != null && <ErrorMessage error={error} title="Chat unavailable" />}

        {/* Input */}
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about the weather…"
            disabled={loading}
            className="text-sm"
          />
          <Button type="submit" size="icon" disabled={!input.trim() || loading}>
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
