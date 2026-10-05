'use client';

import { Synthesis } from '@/lib/api';

interface SynthesisCardProps {
  synthesis: Synthesis;
}

export default function SynthesisCard({ synthesis }: SynthesisCardProps) {
  return (
    <div className="rounded-2xl bg-gradient-to-b from-slate-900 to-slate-950 border border-slate-800 p-6 sm:p-8 space-y-6 shadow-2xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h3 className="text-xl font-extrabold text-white flex items-center space-x-2">
            <span>Executive Multi-Domain Synthesis</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Unified cross-domain intelligence synthesized from independent expert agent evaluations
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <span className="text-xs text-slate-400 font-medium">Overall System Impact:</span>
          <span
            className={`px-3 py-1 rounded-full text-xs font-bold font-mono uppercase tracking-wider border ${
              synthesis.overall_impact.toLowerCase() === 'high'
                ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                : synthesis.overall_impact.toLowerCase() === 'medium'
                ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
            }`}
          >
            {synthesis.overall_impact}
          </span>
        </div>
      </div>

      {/* Overall Assessment */}
      <div className="space-y-2">
        <h4 className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">
          Unified Executive Assessment
        </h4>
        <p className="text-sm text-slate-200 leading-relaxed bg-slate-950 p-4 rounded-xl border border-slate-800 shadow-inner">
          {synthesis.overall_summary}
        </p>
      </div>

      {/* Grid: Opportunities & Risks */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Key Opportunities */}
        <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-900/30 space-y-2">
          <h5 className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center space-x-1.5">
            <span>✨ Strategic Opportunities</span>
          </h5>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {synthesis.major_opportunities.map((opp, i) => (
              <li key={i} className="flex items-start space-x-2">
                <span className="text-emerald-400 font-bold">•</span>
                <span>{opp}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Key Risks */}
        <div className="p-4 rounded-xl bg-rose-950/20 border border-rose-900/30 space-y-2">
          <h5 className="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center space-x-1.5">
            <span>⚠️ Major Risk Vectors</span>
          </h5>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {synthesis.major_risks.map((risk, i) => (
              <li key={i} className="flex items-start space-x-2">
                <span className="text-rose-400 font-bold">•</span>
                <span>{risk}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Cross Domain Interactions */}
      {synthesis.cross_domain_effects.length > 0 && (
        <div className="p-4 rounded-xl bg-indigo-950/20 border border-indigo-900/30 space-y-2">
          <h5 className="text-xs font-bold text-indigo-400 uppercase tracking-wider flex items-center space-x-1.5">
            <span>🔄 Cross-Domain Interdependencies</span>
          </h5>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {synthesis.cross_domain_effects.map((effect, i) => (
              <li key={i} className="flex items-start space-x-2">
                <span className="text-indigo-400 font-bold">⇄</span>
                <span>{effect}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
