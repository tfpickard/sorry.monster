"use client";

interface ApologyResultsProps {
  results: any;
  onReset: () => void;
}

export function ApologyResults({ results, onReset }: ApologyResultsProps) {
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert("Copied to clipboard!");
  };

  return (
    <div className="space-y-8">
      {/* Metrics */}
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold mb-4">Risk & Quality Metrics</h2>
        <div className="grid grid-cols-5 gap-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-red-600">
              {(results.metrics.pr_risk * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-slate-600 dark:text-slate-400">PR Risk</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-orange-600">
              {(results.metrics.legal_risk * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Legal Risk</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">
              {(results.metrics.ethics_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Ethics Score</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">
              {(results.metrics.clarity_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Clarity</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {(results.metrics.sincerity_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Sincerity</div>
          </div>
        </div>

        {results.detectors.non_apology && (
          <div className="mt-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
            <p className="text-sm text-yellow-800 dark:text-yellow-200">
              ⚠️ Non-apology pattern detected
            </p>
          </div>
        )}

        {results.adjustments.length > 0 && (
          <div className="mt-4">
            <h3 className="font-semibold mb-2">Adjustments Applied:</h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-slate-600 dark:text-slate-400">
              {results.adjustments.map((adj: string, i: number) => (
                <li key={i}>{adj}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Drafts */}
      {Object.entries(results.drafts).map(([channel, draft]: [string, any]) => (
        <div key={channel} className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-4 capitalize">{channel.replace("_", " ")}</h2>

          <div className="space-y-6">
            {/* Useful Variant */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold text-green-600">
                  ✓ Useful (Professional)
                </h3>
                <button
                  onClick={() => copyToClipboard(draft.useful)}
                  className="text-sm bg-slate-200 dark:bg-slate-700 px-3 py-1 rounded hover:bg-slate-300 dark:hover:bg-slate-600"
                >
                  Copy
                </button>
              </div>
              <div className="bg-slate-50 dark:bg-slate-900 p-4 rounded-lg whitespace-pre-wrap">
                {draft.useful}
              </div>
            </div>

            {/* Pointless Variant */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold text-purple-600">
                  ☆ Pointless (Satirical)
                </h3>
                <button
                  onClick={() => copyToClipboard(draft.pointless)}
                  className="text-sm bg-slate-200 dark:bg-slate-700 px-3 py-1 rounded hover:bg-slate-300 dark:hover:bg-slate-600"
                >
                  Copy
                </button>
              </div>
              <div className="bg-slate-50 dark:bg-slate-900 p-4 rounded-lg whitespace-pre-wrap">
                {draft.pointless}
              </div>
            </div>

            {/* Redlines */}
            {draft.redlines.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold mb-2 text-red-600">
                  Evasion/Spin Phrases:
                </h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-slate-600 dark:text-slate-400">
                  {draft.redlines.map((redline: string, i: number) => (
                    <li key={i}>{redline}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      ))}

      {/* Reset Button */}
      <div className="text-center">
        <button
          onClick={onReset}
          className="bg-slate-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-slate-700"
        >
          Generate Another Apology
        </button>
      </div>
    </div>
  );
}
