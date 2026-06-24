import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { useGeolocation } from "@/hooks/useGeolocation";

describe("useGeolocation", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("starts with no coords and no error", () => {
    const { result } = renderHook(() => useGeolocation());
    expect(result.current.coords).toBeNull();
    expect(result.current.error).toBeNull();
    expect(result.current.loading).toBe(false);
  });

  it("sets error when geolocation is unsupported", () => {
    Object.defineProperty(global.navigator, "geolocation", {
      value: undefined,
      configurable: true,
    });
    const { result } = renderHook(() => useGeolocation());
    act(() => result.current.locate());
    expect(result.current.error).toMatch(/not supported/i);
  });
});
