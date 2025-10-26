"use client";

import { useState } from "react";
import { ApologyForm } from "@/components/ApologyForm";
import { ApologyResults } from "@/components/ApologyResults";
import { Header } from "@/components/Header";

export default function Home() {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async (data: any) => {
    setLoading(true);
    try {
      // Call API to generate apologies
      const response = await fetch("/api/v1/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Generation failed");
      }

      const result = await response.json();
      setResults(result);
    } catch (error) {
      console.error("Error generating apologies:", error);
      alert("Failed to generate apologies. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <Header />
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
            sorry.monster
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-300 mb-2">
            Apology-as-a-Service
          </p>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            LLM-powered apology generation with full control over tone, style, and sincerity
          </p>
        </div>

        {!results ? (
          <ApologyForm onGenerate={handleGenerate} loading={loading} />
        ) : (
          <ApologyResults results={results} onReset={() => setResults(null)} />
        )}
      </div>

      <footer className="text-center py-8 text-sm text-slate-500 dark:text-slate-400">
        <p>
          Powered by GPT-4 • Built with guardrails •{" "}
          <a
            href="https://oops.ninja"
            className="text-blue-600 hover:underline"
            target="_blank"
            rel="noopener noreferrer"
          >
            Try oops.ninja
          </a>{" "}
          for instant mode
        </p>
      </footer>
    </main>
  );
}
