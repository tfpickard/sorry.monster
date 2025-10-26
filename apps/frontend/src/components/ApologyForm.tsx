"use client";

import { useState } from "react";

interface ApologyFormProps {
  onGenerate: (data: any) => void;
  loading: boolean;
}

export function ApologyForm({ onGenerate, loading }: ApologyFormProps) {
  const [incident, setIncident] = useState({
    summary: "",
    who: "customers",
    what: "",
    when: "",
    harm: "",
    severity: "medium",
    evidence: "",
  });

  const [sliders, setSliders] = useState({
    contrition: 65,
    legal_hedging: 30,
    memes: 0,
  });

  const [channels, setChannels] = useState<string[]>(["twitter"]);
  const [tone, setTone] = useState("earnest");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const data = {
      mode: "generate",
      incident: {
        ...incident,
        who: [incident.who],
        stakeholders: [incident.who],
        jurisdictions: [],
        evidence: incident.evidence ? incident.evidence.split(",").map((e) => e.trim()) : [],
      },
      sliders,
      strategy: {
        scapegoat: { type: null, intensity: 0 },
        distraction: { type: null, intensity: 0 },
        responsibility_split: { brand: 0.5, external: 0.5 },
        victimless_frame: false,
        self_credentialing: [],
      },
      tone,
      channels,
      locale: "en-US",
    };

    onGenerate(data);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-8">
      <div className="space-y-6">
        {/* Incident Details */}
        <div>
          <h2 className="text-2xl font-bold mb-4">Incident Details</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Summary *</label>
              <input
                type="text"
                value={incident.summary}
                onChange={(e) => setIncident({ ...incident, summary: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg dark:bg-slate-700 dark:border-slate-600"
                placeholder="Brief incident description"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">What Happened *</label>
              <textarea
                value={incident.what}
                onChange={(e) => setIncident({ ...incident, what: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg dark:bg-slate-700 dark:border-slate-600"
                rows={3}
                placeholder="Detailed description of the incident"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Harm Caused *</label>
              <textarea
                value={incident.harm}
                onChange={(e) => setIncident({ ...incident, harm: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg dark:bg-slate-700 dark:border-slate-600"
                rows={2}
                placeholder="Description of harm or impact"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Affected</label>
                <select
                  value={incident.who}
                  onChange={(e) => setIncident({ ...incident, who: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg dark:bg-slate-700 dark:border-slate-600"
                >
                  <option value="customers">Customers</option>
                  <option value="employees">Employees</option>
                  <option value="partners">Partners</option>
                  <option value="public">Public</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Severity</label>
                <select
                  value={incident.severity}
                  onChange={(e) => setIncident({ ...incident, severity: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg dark:bg-slate-700 dark:border-slate-600"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Evidence (comma-separated)
              </label>
              <input
                type="text"
                value={incident.evidence}
                onChange={(e) => setIncident({ ...incident, evidence: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg dark:bg-slate-700 dark:border-slate-600"
                placeholder="e.g., rollback done, refund job queued"
              />
            </div>
          </div>
        </div>

        {/* Tone Controls */}
        <div>
          <h2 className="text-2xl font-bold mb-4">Tone & Style</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Contrition: {sliders.contrition}
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={sliders.contrition}
                onChange={(e) =>
                  setSliders({ ...sliders, contrition: parseInt(e.target.value) })
                }
                className="w-full"
              />
              <p className="text-xs text-slate-500 mt-1">
                0-20: neutral | 21-59: partial ownership | 60+: explicit responsibility
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Legal Hedging: {sliders.legal_hedging}
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={sliders.legal_hedging}
                onChange={(e) =>
                  setSliders({ ...sliders, legal_hedging: parseInt(e.target.value) })
                }
                className="w-full"
              />
              <p className="text-xs text-slate-500 mt-1">
                0-20: plain | 21-59: qualifiers | 60+: safe-harbor language
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Memes: {sliders.memes}</label>
              <input
                type="range"
                min="0"
                max="100"
                value={sliders.memes}
                onChange={(e) => setSliders({ ...sliders, memes: parseInt(e.target.value) })}
                className="w-full"
              />
              <p className="text-xs text-slate-500 mt-1">
                0-10: none | 11-40: subtle | 41-70: tasteful | 71+: overt
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Overall Tone</label>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg dark:bg-slate-700 dark:border-slate-600"
              >
                <option value="earnest">Earnest</option>
                <option value="warm">Warm</option>
                <option value="dry">Dry</option>
                <option value="stoic">Stoic</option>
                <option value="cheeky">Cheeky</option>
              </select>
            </div>
          </div>
        </div>

        {/* Channels */}
        <div>
          <h2 className="text-2xl font-bold mb-4">Channels</h2>
          <div className="grid grid-cols-3 gap-4">
            {[
              "twitter",
              "linkedin",
              "press_release",
              "ceo_letter",
              "customer_email",
              "status_page",
            ].map((channel) => (
              <label key={channel} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={channels.includes(channel)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setChannels([...channels, channel]);
                    } else {
                      setChannels(channels.filter((c) => c !== channel));
                    }
                  }}
                  className="rounded"
                />
                <span className="text-sm capitalize">{channel.replace("_", " ")}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-slate-400 disabled:cursor-not-allowed"
        >
          {loading ? "Generating..." : "Generate Apologies"}
        </button>
      </div>
    </form>
  );
}
