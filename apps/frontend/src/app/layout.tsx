import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "sorry.monster - Apology-as-a-Service",
  description:
    "LLM-powered apology generation platform. Generate professional or satirical apologies instantly.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
