'use client';

import { useState } from 'react';

interface ScenarioInputProps {
  onAnalyze: (scenario: string) => void;
  loading: boolean;
}

const PRESETS = [
  {
    label: "🚗 India Petrol & Diesel Car Ban 2035",
    text: "India bans the sale of new petrol and diesel cars from 2035.",
  },
  {
    label: "📈 Central Bank Rate Increase",
    text: "The central bank increases interest rates significantly.",
  },
  {
    label: "🤖 AI Customer Support Automation",
    text: "AI automates a large portion of customer service jobs.",
  },
  {
    label: "🌾 Multi-Year Agricultural Drought",
    text: "A severe drought reduces agricultural production for several years.",
  },
];

export default function ScenarioInput({ onAnalyze, loading }: ScenarioInputProps) {
  const [scenarioText, setScenarioText] = useState<string>('');
  const [inputError, setInputError] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!scenarioText.trim()) {
      setInputError('Please enter a hypothetical scenario to analyze.');
      return;
    }
    setInputError('');
    onAnalyze(scenarioText);
  };

  const handleSelectPreset = (text: string) => {
    setScenarioText(text);
    setInputError('');
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="relative rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-950/90 p-6 sm:p-8 border border-slate-800 shadow-2xl backdrop-blur-xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="scenario-input" className="block text-sm font-semibold text-slate-200">
              Hypothetical Decision or Policy Scenario
            </label>
            <textarea
              id="scenario-input"
              rows={4}
              value={scenarioText}
              onChange={(e) => {
                setScenarioText(e.target.value);
                if (inputError) setInputError('');
              }}
              placeholder="India bans the sale of new petrol and diesel cars from 2035."
              disabled={loading}
              className="w-full rounded-xl bg-slate-950 border border-slate-800 p-4 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-sm sm:text-base resize-none shadow-inner disabled:opacity-50"
            />
            {inputError && (
              <p className="text-xs text-rose-400 font-medium mt-1">{inputError}</p>
            )}
          </div>

          {/* Quick Scenario Preset Chips */}
          <div className="space-y-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
              Quick Test Scenarios:
            </span>
            <div className="flex flex-wrap gap-2">
              {PRESETS.map((preset, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSelectPreset(preset.text)}
                  disabled={loading}
                  className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700/90 text-slate-300 border border-slate-700/60 transition disabled:opacity-50 text-left hover:text-white"
                >
                  {preset.label}
                </button>
              ))}
            </div>
          </div>

          {/* Action Button */}
          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={loading || !scenarioText.trim()}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-bold text-sm bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 hover:from-indigo-600 hover:via-purple-600 hover:to-pink-600 text-white shadow-lg shadow-indigo-500/25 transition duration-200 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  <span>Processing Analysis...</span>
                </>
              ) : (
                <>
                  <span>Explore Parallel Universe</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
