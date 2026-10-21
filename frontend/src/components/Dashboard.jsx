import React from 'react';
import { Shield, AlertOctagon, Activity, Scroll, Award, AlertTriangle, ArrowRight, Zap } from 'lucide-react';

export default function Dashboard({ metrics, commissions, beyonders, onOpenDispatch, setActiveTab }) {
  const highRiskCommissions = commissions.filter(c => c.hazard_rank >= 5 && c.status === 'OPEN');
  const corruptedBeyonders = beyonders.filter(b => b.sanity_percentage < 40.0);

  return (
    <div className="space-[#12141c] space-y-8">
      {/* Header Banner */}
      <div className="gothic-card gothic-card-gold p-6 rounded-lg bg-gradient-to-r from-[#171326] via-[#12141c] to-[#1c121e]">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <span className="text-xs uppercase font-serif tracking-widest text-[#d4af37] px-2.5 py-1 rounded border border-[#d4af37]/30 bg-[#d4af37]/10">
              The Fool's Sanctuary
            </span>
            <h2 className="text-2xl font-serif font-bold text-[#e6c656] mt-2 gold-glow">
              Tarot Command Center Overview
            </h2>
            <p className="text-sm text-slate-300 font-serif max-w-2xl mt-1">
              Real-time monitoring of Beyonder agent sanity levels, potion pathway codices, and active Victorian commissions.
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => setActiveTab('commissions')}
              className="px-4 py-2 rounded-md bg-[#2d1b36] hover:bg-[#3d2449] border border-[#a855f7]/40 text-purple-200 font-serif text-sm flex items-center gap-2 transition"
            >
              <Scroll className="w-4 h-4 text-purple-400" />
              View Commissions
            </button>
            <button
              onClick={() => onOpenDispatch(null)}
              className="px-4 py-2 rounded-md bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/60 text-[#e6c656] font-serif text-sm font-semibold flex items-center gap-2 transition shadow-lg shadow-amber-950/50"
            >
              <Zap className="w-4 h-4 text-[#d4af37]" />
              Dispatch Operative
            </button>
          </div>
        </div>
      </div>

      {/* Corruption Warning Alert Banner if corrupted agents exist */}
      {corruptedBeyonders.length > 0 && (
        <div className="p-4 rounded-lg bg-red-950/40 border border-red-800/60 text-red-200 flex items-center justify-between shadow-lg shadow-red-950/30">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-6 h-6 text-red-400 animate-pulse shrink-0" />
            <div>
              <p className="font-serif font-bold text-red-300">
                CRITICAL SANITY ALERT: {corruptedBeyonders.length} Operative(s) Nearing Mental Breakdown!
              </p>
              <p className="text-xs text-red-300/80 font-serif">
                Agents with sanity below 40% risk imminent madness or monster transformation. Rest tab or debrief immediately.
              </p>
            </div>
          </div>
          <button
            onClick={() => setActiveTab('beyonders')}
            className="px-3 py-1.5 rounded bg-red-900/60 hover:bg-red-800 border border-red-500 text-xs font-serif text-red-100 flex items-center gap-1 transition shrink-0"
          >
            Inspect Roster <ArrowRight className="w-3 h-3" />
          </button>
        </div>
      )}

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Card 1: Active Agents */}
        <div className="gothic-card p-5 rounded-lg flex items-center justify-between">
          <div>
            <p className="text-xs font-serif text-slate-400 uppercase tracking-wider">Active Operatives</p>
            <h3 className="text-3xl font-serif font-bold text-amber-200 mt-1">
              {metrics.active_agents || beyonders.filter(b => b.sanity_percentage >= 30).length}
            </h3>
            <p className="text-xs text-slate-400 mt-1">Total Registered: {metrics.total_beyonders || beyonders.length}</p>
          </div>
          <div className="p-3.5 rounded-full bg-amber-950/40 border border-amber-500/30 text-amber-400">
            <Shield className="w-7 h-7" />
          </div>
        </div>

        {/* Card 2: High Risk Open Missions */}
        <div className="gothic-card p-5 rounded-lg flex items-center justify-between">
          <div>
            <p className="text-xs font-serif text-slate-400 uppercase tracking-wider">High-Risk Missions</p>
            <h3 className="text-3xl font-serif font-bold text-red-400 mt-1">
              {metrics.high_risk_commissions || highRiskCommissions.length}
            </h3>
            <p className="text-xs text-slate-400 mt-1">Hazard Level Rank 5 - 9</p>
          </div>
          <div className="p-3.5 rounded-full bg-red-950/40 border border-red-500/30 text-red-400">
            <AlertOctagon className="w-7 h-7" />
          </div>
        </div>

        {/* Card 3: Average Sanity / Corruption */}
        <div className="gothic-card p-5 rounded-lg flex items-center justify-between">
          <div>
            <p className="text-xs font-serif text-slate-400 uppercase tracking-wider">Avg Mental Sanity</p>
            <h3 className={`text-3xl font-serif font-bold mt-1 ${
              (metrics.average_sanity || 100) > 75 ? 'text-emerald-400' :
              (metrics.average_sanity || 100) > 40 ? 'text-amber-400' : 'text-red-400'
            }`}>
              {metrics.average_sanity || 100}%
            </h3>
            <p className="text-xs text-slate-400 mt-1">Corrupted: {metrics.corrupted_beyonders_count || 0}</p>
          </div>
          <div className="p-3.5 rounded-full bg-purple-950/40 border border-purple-500/30 text-purple-400">
            <Activity className="w-7 h-7" />
          </div>
        </div>

        {/* Card 4: Total Commissions */}
        <div className="gothic-card p-5 rounded-lg flex items-center justify-between">
          <div>
            <p className="text-xs font-serif text-slate-400 uppercase tracking-wider">Total Commissions</p>
            <h3 className="text-3xl font-serif font-bold text-purple-300 mt-1">
              {metrics.total_commissions || commissions.length}
            </h3>
            <p className="text-xs text-slate-400 mt-1">Completed: {metrics.completed_commissions || 0}</p>
          </div>
          <div className="p-3.5 rounded-full bg-blue-950/40 border border-blue-500/30 text-blue-400">
            <Award className="w-7 h-7" />
          </div>
        </div>
      </div>

      {/* High Hazard Open Missions Section */}
      <div className="gothic-card p-6 rounded-lg space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-serif font-bold text-[#e6c656] flex items-center gap-2">
              <Scroll className="w-5 h-5 text-[#d4af37]" /> High-Priority Available Commissions
            </h3>
            <p className="text-xs text-slate-400 font-serif">Open missions requiring eligible Beyonder assignment.</p>
          </div>
          <button
            onClick={() => setActiveTab('commissions')}
            className="text-xs font-serif text-[#d4af37] hover:underline flex items-center gap-1"
          >
            View All ({commissions.filter(c => c.status === 'OPEN').length}) <ArrowRight className="w-3 h-3" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm font-serif border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase text-xs">
                <th className="py-3 px-4">Title</th>
                <th className="py-3 px-4">Hazard Rank</th>
                <th className="py-3 px-4">Target</th>
                <th className="py-3 px-4">Location</th>
                <th className="py-3 px-4">Reward</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {commissions.filter(c => c.status === 'OPEN').slice(0, 5).map((comm) => (
                <tr key={comm.id} className="hover:bg-[#191c28]/60 transition">
                  <td className="py-3 px-4 font-semibold text-slate-200">{comm.title}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-0.5 rounded text-xs border font-bold ${
                      comm.hazard_rank <= 3 ? 'bg-purple-950/60 border-purple-500/50 text-purple-300' :
                      comm.hazard_rank <= 6 ? 'bg-amber-950/60 border-amber-500/50 text-amber-300' :
                      'bg-red-950/60 border-red-500/50 text-red-300 animate-pulse'
                    }`}>
                      Hazard Rank {comm.hazard_rank}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-300">{comm.target}</td>
                  <td className="py-3 px-4 text-slate-400 text-xs">{comm.location}</td>
                  <td className="py-3 px-4 text-[#e6c656] font-semibold">{comm.reward_gold} £</td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => onOpenDispatch(comm)}
                      className="px-3 py-1 rounded bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/60 text-[#e6c656] text-xs font-semibold transition"
                    >
                      Dispatch Agent
                    </button>
                  </td>
                </tr>
              ))}
              {commissions.filter(c => c.status === 'OPEN').length === 0 && (
                <tr>
                  <td colSpan="6" className="text-center py-6 text-slate-500 italic">
                    No open commissions at this time.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
