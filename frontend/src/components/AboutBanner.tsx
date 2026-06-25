import { ExternalLink } from "lucide-react";

export function AboutBanner() {
  return (
    <footer className="border-t bg-muted/40 py-6 mt-12">
      <div className="container mx-auto px-4 text-sm text-muted-foreground space-y-1">
        <p className="font-semibold text-foreground">Brendan Lee — AI Engineer Intern</p>
        <p>
          <span className="font-medium text-foreground">Product Manager Accelerator (PMA)</span> is a world-class
          program that helps aspiring and current product managers land their dream PM roles, advance their careers,
          and connect with a global community of product leaders through mentorship, real-world projects, and
          expert-led training.
        </p>
        <a
          href="https://www.linkedin.com/company/product-manager-accelerator/"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-primary hover:underline"
        >
          LinkedIn: Product Manager Accelerator <ExternalLink className="h-3 w-3" />
        </a>
      </div>
    </footer>
  );
}
