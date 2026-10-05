'use client';

import { ExpertAnalysis } from '@/lib/api';

interface ExpertCardProps {
  analyses: ExpertAnalysis[];
}

export default function ExpertCard({ analyses }: ExpertCardProps) {
  const getImpactBadge = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      case 'medium':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'low':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      default:
        return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  const getExpertIcon = (domain: string) => {
    switch (domain.toLowerCase()) {
      case 'automotive':
        return '🚘';
      case 'energy':
        return '⚡';
      case 'environment':
        return '🌱';
      case 'economy':
        return '📈';
      case 'employment':
        return '👥';
      default:
        return '🧠';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-slate-100 flex items-center space-x-2">
          <span>Independent Expert Analyses</span>
          <span className="text-xs font-normal text-slate-400 bg-slate-900 border border-slate-800 px-2.5 py-0.5 rounded-full">
            Multi-Agent Reasoners
          </span>
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {analyses.map((analysis) => (
          <div
            key={analysis.expert}
            className="rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-950/90 border border-slate-800 p-6 space-y-5 shadow-xl hover:border-slate-700 transition"
          >
            {/* Expert Header */}
            <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{getExpertIcon(analysis.domain)}</span>
                <div>
                  <h4 className="font-bold text-slate-100 text-base">{analysis.expert}</h4>
                  <span className="text-xs text-slate-400 uppercase tracking-wider font-mono">
                    Domain: {analysis.domain}
                  </span>
                </div>
              </div>

              <span
                className={`text-xs font-bold font-mono px-3 py-1 rounded-full border uppercase tracking-wider ${getImpactBadge(
                  analysis.impact_level
                )}`}
              >
                {analysis.impact_level} Impact
              </span>
            </div>

            {/* Executive Summary */}
            <div className="space-y-1">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
                Executive Domain Summary
              </span>
              <p className="text-sm text-slate-300 leading-relaxed bg-slate-950/60 p-3 rounded-xl border border-slate-800/60">
                {analysis.summary}
              </p>
            </div>

            {/* Positive Impacts & Opportunities */}
            {analysis.positive_impacts.length > 0 && (
              <div className="space-y-1.5">
                <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider flex items-center space-x-1">
                  <span>✓ Positive Impacts & Opportunities</span>
                </span>
                <ul className="space-y-1 text-xs text-slate-300">
                  {analysis.positive_impacts.map((item, i) => (
                    <li key={i} className="flex items-start space-x-2">
                      <span className="text-emerald-400 font-bold">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Negative Impacts & Risks */}
            {(analysis.negative_impacts.length > 0 || analysis.risks.length > 0) && (
              <div className="space-y-1.5">
                <span className="text-xs font-semibold text-rose-400 uppercase tracking-wider flex items-center space-x-1">
                  <span>⚠ Risks & Challenges</span>
                </span>
                <ul className="space-y-1 text-xs text-slate-300">
                  {[...analysis.negative_impacts, ...analysis.risks].slice(0, 3).map((item, i) => (
                    <li key={i} className="flex items-start space-x-2">
                      <span className="text-rose-400 font-bold">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Key Factors */}
            {analysis.key_factors.length > 0 && (
              <div className="pt-2 border-t border-slate-800/60 text-xs text-slate-400 space-y-1">
                <span className="font-semibold text-slate-300 block">Critical Driving Factors:</span>
                <p className="text-slate-400 italic">{analysis.key_factors.join(' • ')}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
