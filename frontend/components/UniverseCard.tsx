'use client';

import { ParallelUniverses } from '@/lib/api';

interface UniverseCardProps {
  universes: ParallelUniverses;
}

export default function UniverseCard({ universes }: UniverseCardProps) {
  const cards = [
    {
      id: 'optimistic',
      label: 'OPTIMISTIC',
      icon: '🟢',
      accentColor: 'emerald',
      borderStyle: 'border-emerald-500/40 hover:border-emerald-500/80',
      badgeStyle: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
      headerGradient: 'from-emerald-950/40 to-slate-900/90',
      titleColor: 'text-emerald-300',
      data: universes.optimistic,
    },
    {
      id: 'baseline',
      label: 'BASELINE',
      icon: '🔵',
      accentColor: 'sky',
      borderStyle: 'border-sky-500/40 hover:border-sky-500/80',
      badgeStyle: 'bg-sky-500/10 text-sky-400 border-sky-500/30',
      headerGradient: 'from-sky-950/40 to-slate-900/90',
      titleColor: 'text-sky-300',
      data: universes.baseline,
    },
    {
      id: 'adverse',
      label: 'ADVERSE',
      icon: '🔴',
      accentColor: 'rose',
      borderStyle: 'border-rose-500/40 hover:border-rose-500/80',
      badgeStyle: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
      headerGradient: 'from-rose-950/40 to-slate-900/90',
      titleColor: 'text-rose-300',
      data: universes.adverse,
    },
  ];

  return (
    <div className="space-y-6 pt-4">
      <div className="text-center space-y-1 max-w-2xl mx-auto">
        <h3 className="text-2xl font-black tracking-tight text-white flex items-center justify-center space-x-2">
          <span>Parallel Universe Futures</span>
        </h3>
        <p className="text-xs text-slate-400 leading-relaxed">
          The same hypothetical decision branches into distinct future trajectories depending on execution velocity, resource availability, and risk materialization.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {cards.map((card) => (
          <div
            key={card.id}
            className={`rounded-2xl bg-gradient-to-b ${card.headerGradient} border ${card.borderStyle} p-6 space-y-5 shadow-2xl transition duration-300 flex flex-col justify-between`}
          >
            <div className="space-y-4">
              {/* Universe Badge */}
              <div className="flex items-center justify-between">
                <span className="flex items-center space-x-2">
                  <span className="text-lg">{card.icon}</span>
                  <span className={`text-xs font-extrabold font-mono px-3 py-1 rounded-full border uppercase tracking-wider ${card.badgeStyle}`}>
                    {card.label} UNIVERSE
                  </span>
                </span>
              </div>

              {/* Title & Summary */}
              <div>
                <h4 className={`text-lg font-bold ${card.titleColor}`}>
                  {card.data.title}
                </h4>
                <p className="text-xs text-slate-300 mt-2 leading-relaxed bg-slate-950/70 p-3 rounded-xl border border-slate-800/80">
                  {card.data.summary}
                </p>
              </div>

              {/* Key Projected Outcomes */}
              {card.data.key_outcomes.length > 0 && (
                <div className="space-y-1.5">
                  <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider block">
                    Key Projected Outcomes
                  </span>
                  <ul className="space-y-1 text-xs text-slate-300">
                    {card.data.key_outcomes.map((outcome, idx) => (
                      <li key={idx} className="flex items-start space-x-2">
                        <span className="text-slate-400 font-bold">•</span>
                        <span>{outcome}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Primary Drivers */}
              {card.data.major_drivers.length > 0 && (
                <div className="space-y-1 text-xs pt-1">
                  <span className="font-semibold text-slate-400 block uppercase tracking-wider">
                    Primary Drivers:
                  </span>
                  <p className="text-slate-300 italic">{card.data.major_drivers.join(' • ')}</p>
                </div>
              )}
            </div>

            {/* Risk Factors Footer */}
            {card.data.risks.length > 0 && (
              <div className="pt-3 border-t border-slate-800/80 text-xs text-slate-400 space-y-1 mt-4">
                <span className="font-medium text-slate-400 block">Critical Sensitivity & Risks:</span>
                <p className="text-slate-300">{card.data.risks.join(' • ')}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
