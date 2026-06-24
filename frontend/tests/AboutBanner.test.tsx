import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { AboutBanner } from "@/components/AboutBanner";

describe("AboutBanner", () => {
  it("shows candidate name", () => {
    render(<AboutBanner />);
    expect(screen.getByText(/Brendan Lee/)).toBeTruthy();
  });

  it("shows PM Accelerator description", () => {
    render(<AboutBanner />);
    expect(document.body.textContent).toContain("Product Manager Accelerator");
  });

  it("has a LinkedIn link", () => {
    render(<AboutBanner />);
    const link = screen.getByRole("link");
    expect(link.getAttribute("href")).toContain("linkedin.com");
  });
});
