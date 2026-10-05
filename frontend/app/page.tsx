'use client';

import { useState } from 'react';
import ScenarioInput from '@/components/ScenarioInput';
import AnalysisResults from '@/components/AnalysisResults';
import { analyzeScenario, AnalysisResponse } from '@/lib/api';

export default function Home() {
  const [loading, setLoading] = useState<boolean>(false);
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [loadingStep, setLoadingStep] = useState<number>(0);

  const handleAnalyze = async (scenario: string) => {
    setLoading(true);
    setErrorMessage(null);
    setAnalysisData(null);
    setLoadingStep(1);

    // Simulate incremental pipeline steps for smooth loading animation
    const timer1 = setTimeout(() => setLoadingStep(2), 600);
    const timer2 = setTimeout(() => setLoadingStep(3), 1200);
    const timer3 = setTimeout(() => setLoadingStep(4), 1800);

    const result = await analyzeScenario(scenario);

    clearTimeout(timer1);
    clearTimeout(timer2);
    clearTimeout(timer3);

    setLoading(false);

    if (result.success && result.data) {
      setAnalysisData(result.data);
    } else {
      setErrorMessage(result.error || 'Failed to process scenario analysis.');
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Header Navigation */}
      <header className="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center font-black text-white shadow-lg shadow-indigo-500/30">
              PU
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white flex items-center space-x-2">
                <span>AI Parallel Universe</span>
              </h1>
              <p className="text-xs text-slate-400">
                Multi-Agent Decision Intelligence Engine
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Phase 1 MVP Active
            </span>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-10 space-y-10">
        {/* Hero Section */}
        <section className="text-center max-w-3xl mx-auto space-y-4 pt-2">
          <div className="inline-block px-4 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-indigo-400 text-xs font-semibold tracking-wide">
            HYPOTHETICAL DECISION INTELLIGENCE
          </div>
          <h2 className="text-4xl sm:text-5xl font-black tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
            Explore Parallel Futures Before Deciding
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            Enter a natural-language hypothetical decision or policy scenario. Our dynamic multi-agent pipeline dispatches specialized expert agents to analyze multi-domain impacts and project optimistic, baseline, and adverse parallel universe outcomes.
          </p>
        </section>

        {/* Input Form Section */}
        <section>
          <ScenarioInput onAnalyze={handleAnalyze} loading={loading} />
        </section>

        {/* Loading Pipeline State */}
        {loading && (
          <section className="max-w-xl mx-auto rounded-2xl bg-slate-900/80 border border-slate-800 p-6 space-y-4 shadow-xl">
            <div className="flex items-center space-x-3 pb-3 border-b border-slate-800">
              <div className="h-3 w-3 rounded-full bg-indigo-500 animate-ping" />
              <h3 className="text-sm font-bold text-slate-200">Executing Parallel Universe Pipeline</h3>
            </div>

            <div className="space-y-2.5 text-xs">
              {[
                { step: 1, label: 'Understanding & Parsing Scenario' },
                { step: 2, label: 'Detecting Affected Expert Domains' },
                { step: 3, label: 'Running Independent Expert Agents' },
                { step: 4, label: 'Synthesizing Multi-Domain Universes' },
              ].map((s) => (
                <div key={s.step} className="flex items-center space-x-3">
                  <span
                    className={`h-5 w-5 rounded-full flex items-center justify-center font-bold text-[10px] ${
                      loadingStep > s.step
                        ? 'bg-emerald-500 text-slate-950'
                        : loadingStep === s.step
                        ? 'bg-indigo-500 text-white animate-pulse'
                        : 'bg-slate-800 text-slate-500'
                    }`}
                  >
                    {loadingStep > s.step ? '✓' : s.step}
                  </span>
                  <span
                    className={`font-medium ${
                      loadingStep >= s.step ? 'text-slate-200' : 'text-slate-500'
                    }`}
                  >
                    {s.label}
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Error Message Alert */}
        {errorMessage && (
          <section className="max-w-2xl mx-auto rounded-2xl bg-rose-500/10 border border-rose-500/30 p-6 text-rose-300 space-y-2">
            <div className="flex items-center space-x-2 font-bold text-sm">
              <svg className="w-5 h-5 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Analysis Error</span>
            </div>
            <p className="text-xs font-mono">{errorMessage}</p>
          </section>
        )}

        {/* Analysis Results Dashboard */}
        {analysisData && (
          <section className="pt-4">
            <AnalysisResults data={analysisData} />
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 mt-16">
        <div className="max-w-7xl mx-auto px-6 text-center text-xs text-slate-500">
          AI Parallel Universe Decision Engine &bull; Phase 1 MVP Working System
        </div>
      </footer>
    </div>
  );
}
