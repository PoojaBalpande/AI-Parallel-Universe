'use client';

import { DetectedDomain } from '@/lib/api';

interface DomainCardProps {
  domains: DetectedDomain[];
}

export default function DomainCard({ domains }: DomainCardProps) {
  const getDomainIcon = (name: string) => {
    switch (name.toLowerCase()) {
      case 'automotive':
        return '🚗';
      case 'energy':
        return '⚡';
      case 'environment':
        return '🌱';
      case 'economy':
        return '📊';
      case 'employment':
        return '👥';
      default:
        return '🌐';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-slate-100 flex items-center space-x-2">
          <span>Detected Affected Domains</span>
          <span className="text-xs font-normal text-slate-400 bg-slate-900 border border-slate-800 px-2.5 py-0.5 rounded-full">
            {domains.length} Selected
          </span>
        </h3>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {domains.map((domain) => {
          const relevancePercent = Math.round(domain.relevance * 100);
          return (
            <div
              key={domain.name}
              className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-indigo-500/40 transition space-y-2 shadow-lg"
            >
              <div className="flex items-center justify-between">
                <span className="text-base flex items-center space-x-2 font-semibold text-slate-200">
                  <span>{getDomainIcon(domain.name)}</span>
                  <span>{domain.display_name}</span>
                </span>
                <span
                  className={`text-xs font-mono font-bold px-2 py-1 rounded-md border ${
                    relevancePercent >= 80
                      ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30'
                      : relevancePercent >= 60
                      ? 'bg-sky-500/10 text-sky-400 border-sky-500/30'
                      : 'bg-slate-800 text-slate-300 border-slate-700'
                  }`}
                >
                  {relevancePercent}% Relevance
                </span>
              </div>

              {/* Progress relevance bar */}
              <div className="w-full bg-slate-950 rounded-full h-1.5 overflow-hidden border border-slate-800">
                <div
                  className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 h-1.5 rounded-full transition-all duration-500"
                  style={{ width: `${relevancePercent}%` }}
                />
              </div>

              <p className="text-xs text-slate-400 leading-relaxed pt-1">
                {domain.reason}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
