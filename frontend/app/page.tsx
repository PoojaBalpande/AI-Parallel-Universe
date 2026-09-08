'use client';

import { useState, useEffect } from 'react';
import { fetchHealthStatus, HealthCheckResult } from '@/lib/api';

export default function Home() {
  const [healthState, setHealthState] = useState<HealthCheckResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [lastChecked, setLastChecked] = useState<string>('');

  const checkHealth = async () => {
    setLoading(true);
    const result = await fetchHealthStatus();
    setHealthState(result);
    setLoading(false);
    setLastChecked(new Date().toLocaleTimeString());
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Header */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/30">
              AI
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white">
                AI Parallel Universe Decision Engine
              </h1>
              <p className="text-xs text-slate-400">
                Generalized Multi-Agent Simulation Intelligence
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              Phase 0 — Foundation
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-10 space-y-8">
        {/* Hero Section */}
        <section className="text-center max-w-3xl mx-auto space-y-4 pt-4">
          <div className="inline-block px-4 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-slate-300 text-xs font-medium tracking-wide">
            Phase 0 Development Setup & System Health
          </div>
          <h2 className="text-4xl sm:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
            System Foundation & Connectivity
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            Exploring parallel future outcomes through evidence-based multi-agent consensus. Phase 0 verifies connectivity between the Next.js client interface and the FastAPI microservice engine.
          </p>
        </section>

        {/* Backend Connectivity Status Card */}
        <section className="max-w-2xl mx-auto">
          <div className="relative group rounded-2xl bg-gradient-to-b from-slate-900 to-slate-950 p-1 border border-slate-800 shadow-2xl transition duration-300 hover:border-slate-700">
            <div className="p-6 sm:p-8 space-y-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="relative">
                    <span
                      className={`block h-3.5 w-3.5 rounded-full ${
                        loading
                          ? 'bg-amber-400 animate-ping'
                          : healthState?.success
                          ? 'bg-emerald-500 shadow-lg shadow-emerald-500/50'
                          : 'bg-rose-500 shadow-lg shadow-rose-500/50'
                      }`}
                    />
                    <span
                      className={`absolute inset-0 h-3.5 w-3.5 rounded-full ${
                        loading
                          ? 'bg-amber-400'
                          : healthState?.success
                          ? 'bg-emerald-500'
                          : 'bg-rose-500'
                      }`}
                    />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg text-white">Backend Server Status</h3>
                    <p className="text-xs text-slate-400">
                      {loading
                        ? 'Pinging backend health endpoint...'
                        : healthState?.success
                        ? 'Connected to FastAPI backend'
                        : 'Backend service unreachable'}
                    </p>
                  </div>
                </div>

                <button
                  onClick={checkHealth}
                  disabled={loading}
                  className="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition disabled:opacity-50 flex items-center space-x-2"
                >
                  <svg
                    className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    />
                  </svg>
                  <span>{loading ? 'Checking...' : 'Re-check Connection'}</span>
                </button>
              </div>

              {/* Status Indicator Bar */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 border-t border-slate-800/80">
                <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800">
                  <span className="block text-xs text-slate-400 font-medium">Health Status</span>
                  <span className="text-sm font-bold mt-1 block">
                    {loading ? (
                      <span className="text-slate-500">Checking...</span>
                    ) : healthState?.success ? (
                      <span className="text-emerald-400 flex items-center space-x-1.5">
                        <span>● Connected</span>
                      </span>
                    ) : (
                      <span className="text-rose-400 flex items-center space-x-1.5">
                        <span>● Disconnected</span>
                      </span>
                    )}
                  </span>
                </div>

                <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800">
                  <span className="block text-xs text-slate-400 font-medium">Service Name</span>
                  <span className="text-sm font-mono font-semibold text-slate-200 mt-1 block truncate">
                    {healthState?.data?.service || 'ai-parallel-universe-backend'}
                  </span>
                </div>

                <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800">
                  <span className="block text-xs text-slate-400 font-medium">API Version</span>
                  <span className="text-sm font-mono font-semibold text-indigo-400 mt-1 block">
                    v{healthState?.data?.version || '0.1.0'}
                  </span>
                </div>
              </div>

              {/* Debugging Details */}
              <div className="space-y-2 pt-2 text-xs text-slate-400">
                <div className="flex justify-between items-center bg-slate-950 p-3 rounded-lg border border-slate-800/60 font-mono">
                  <span>Endpoint Target:</span>
                  <span className="text-slate-300">
                    {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/health
                  </span>
                </div>
                {healthState?.latencyMs !== undefined && (
                  <div className="flex justify-between items-center px-1">
                    <span>Roundtrip Latency:</span>
                    <span className="text-slate-300 font-mono">{healthState.latencyMs} ms</span>
                  </div>
                )}
                {lastChecked && (
                  <div className="flex justify-between items-center px-1">
                    <span>Last Synced:</span>
                    <span className="text-slate-400">{lastChecked}</span>
                  </div>
                )}
                {healthState?.error && (
                  <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-300 font-mono mt-2">
                    {healthState.error}
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* Pipeline Architecture Roadmap Preview */}
        <section className="space-y-4 pt-6 max-w-4xl mx-auto">
          <div className="text-center space-y-1">
            <h3 className="text-xl font-bold text-slate-200">System Architecture Roadmap</h3>
            <p className="text-xs text-slate-400">Planned Multi-Agent Pipeline Stages</p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { step: '01', name: 'Scenario Parsing', desc: 'Hypothetical natural language input' },
              { step: '02', name: 'Domain Detection', desc: 'Identify affected sectors & fields' },
              { step: '03', name: 'Expert Selection', desc: 'Dispatch specialized domain agents' },
              { step: '04', name: 'Multi-Agent Analysis', desc: 'Independent evidence-backed reasoning' },
              { step: '05', name: 'Conflict Analysis', desc: 'Detect agreement & divergence' },
              { step: '06', name: 'Future Scenarios', desc: 'Generate high-probability branches' },
              { step: '07', name: 'Causal Modeling', desc: 'Temporal flow & impact graph' },
              { step: '08', name: 'Decision Engine', desc: 'Actionable policy insights' },
            ].map((stage, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl bg-slate-900/40 border border-slate-800/80 hover:border-slate-700 transition"
              >
                <span className="text-xs font-mono font-semibold text-indigo-400">{stage.step}</span>
                <h4 className="text-sm font-semibold text-slate-200 mt-1">{stage.name}</h4>
                <p className="text-xs text-slate-400 mt-1 leading-snug">{stage.desc}</p>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6">
        <div className="max-w-6xl mx-auto px-6 text-center text-xs text-slate-400">
          AI Parallel Universe Decision Engine &bull; Phase 0 Foundation Complete
        </div>
      </footer>
    </div>
  );
}
