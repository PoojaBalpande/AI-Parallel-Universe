'use client';

import { AnalysisResponse } from '@/lib/api';
import DomainCard from './DomainCard';
import ExpertCard from './ExpertCard';
import SynthesisCard from './SynthesisCard';
import UniverseCard from './UniverseCard';

interface AnalysisResultsProps {
  data: AnalysisResponse;
}

export default function AnalysisResults({ data }: AnalysisResultsProps) {
  const { scenario, domains, analyses, synthesis, parallel_universes } = data;

  return (
    <div className="w-full max-w-6xl mx-auto space-y-10">
      {/* 1. Scenario Understanding Breakdown Card */}
      <section className="rounded-2xl bg-gradient-to-b from-slate-900 to-slate-950 border border-slate-800 p-6 sm:p-8 space-y-6 shadow-2xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800">
          <div>
            <span className="text-xs font-mono font-semibold text-indigo-400 uppercase tracking-widest block">
              Step 01 — Deconstructed Scenario
            </span>
            <h2 className="text-2xl font-extrabold text-white mt-1">
              Scenario Understanding & Structure
            </h2>
          </div>
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-mono font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            Type: {scenario.scenario_type}
          </span>
        </div>

        {/* Original Scenario Prompt */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
            Input Scenario:
          </span>
          <p className="text-base font-semibold text-slate-100 italic">
            "{scenario.original_text}"
          </p>
        </div>

        {/* Structured Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
          <div className="p-3.5 rounded-xl bg-slate-900/50 border border-slate-800">
            <span className="text-xs text-slate-400 block font-medium">Subject</span>
            <span className="text-sm font-semibold text-slate-200 mt-1 block truncate">
              {scenario.subject}
            </span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/50 border border-slate-800">
            <span className="text-xs text-slate-400 block font-medium">Core Action</span>
            <span className="text-sm font-semibold text-slate-200 mt-1 block truncate">
              {scenario.action}
            </span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/50 border border-slate-800">
            <span className="text-xs text-slate-400 block font-medium">Geographic Scope</span>
            <span className="text-sm font-semibold text-indigo-400 mt-1 block truncate">
              {scenario.location?.country || scenario.location?.region || 'Global / Unspecified'}
            </span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/50 border border-slate-800">
            <span className="text-xs text-slate-400 block font-medium">Target Horizon</span>
            <span className="text-sm font-semibold text-indigo-400 mt-1 block truncate">
              {scenario.time?.start_year ? `From ${scenario.time.start_year}` : 'Immediate / Open'}
            </span>
          </div>
        </div>

        {/* Entities, Assumptions, Uncertainties */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2 text-xs">
          {scenario.affected_entities.length > 0 && (
            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/80 space-y-1">
              <span className="font-semibold text-slate-300 block">Affected Target Entities</span>
              <p className="text-slate-400">{scenario.affected_entities.join(', ')}</p>
            </div>
          )}

          {scenario.assumptions.length > 0 && (
            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-800/80 space-y-1">
              <span className="font-semibold text-slate-300 block">Key Assumptions</span>
              <p className="text-slate-400">{scenario.assumptions.join(' • ')}</p>
            </div>
          )}

          {scenario.uncertainties.length > 0 && (
            <div className="p-3.5 rounded-xl bg-amber-950/20 border border-amber-900/30 space-y-1">
              <span className="font-semibold text-amber-400 block">Explicit Uncertainties</span>
              <p className="text-slate-300">{scenario.uncertainties.join(' • ')}</p>
            </div>
          )}
        </div>
      </section>

      {/* 2. Detected Domains Section */}
      <section>
        <DomainCard domains={domains} />
      </section>

      {/* 3. Independent Expert Analyses */}
      <section>
        <ExpertCard analyses={analyses} />
      </section>

      {/* 4. Executive Synthesis */}
      <section>
        <SynthesisCard synthesis={synthesis} />
      </section>

      {/* 5. Parallel Universes */}
      <section>
        <UniverseCard universes={parallel_universes} />
      </section>
    </div>
  );
}
