import React from 'react';
import { Activity, FileText, CheckCircle2, Clock, Zap } from 'lucide-react';

export default function ClaimsList({ claims, onOpenDebriefModal, onOpenDispatchModal }) {
  return (
    <div className="space-y-6 font-serif">
      <div className="gothic-card p-6 rounded-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-serif font-bold text-[#e6c656] flex items-center gap-2 gold-glow">
            <Activity className="w-6 h-6 text-[#d4af37]" /> Active Dispatches & Mission Claims Log
          </h2>
          <p className="text-xs text-slate-400 font-serif mt-1">
            Track live agent assignments, field debrief logs, and post-mission sanity updates.
          </p>
        </div>
        <button
          onClick={() => onOpenDispatchModal(null)}
          className="px-4 py-2 rounded-md bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/60 text-[#e6c656] font-serif text-sm font-semibold flex items-center gap-2 transition shadow-lg shadow-amber-950/50"
        >
          <Zap className="w-4 h-4 text-[#d4af37]" /> Dispatch New Mission
        </button>
      </div>

      <div className="gothic-card p-6 rounded-lg overflow-x-auto">
        <table className="w-full text-left text-sm font-serif">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 uppercase text-xs">
              <th className="py-3 px-4">Claim ID</th>
              <th className="py-3 px-4">Commission</th>
              <th className="py-3 px-4">Dispatched Operative</th>
              <th className="py-3 px-4">Dispatch Date</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4">Debrief Notes</th>
              <th className="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {claims.map((claim) => (
              <tr key={claim.id} className="hover:bg-[#191c28]/60 transition">
                <td className="py-3 px-4 font-mono text-xs text-slate-400">#{claim.id}</td>
                <td className="py-3 px-4 font-semibold text-slate-200">
                  {claim.commission_title || `Commission #${claim.commission_id}`}
                </td>
                <td className="py-3 px-4 text-purple-300 font-semibold">
                  {claim.beyonder_codename || `Beyonder #${claim.beyonder_id}`}
                </td>
                <td className="py-3 px-4 text-slate-400 text-xs">
                  {new Date(claim.claim_date).toLocaleString()}
                </td>
                <td className="py-3 px-4">
                  <span className={`px-2.5 py-0.5 rounded text-xs border font-bold ${
                    claim.status === 'ACTIVE'
                      ? 'bg-amber-950/60 border-amber-500/50 text-amber-300 animate-pulse'
                      : claim.status === 'COMPLETED'
                      ? 'bg-emerald-950/60 border-emerald-500/50 text-emerald-300'
                      : 'bg-red-950/60 border-red-500/50 text-red-300'
                  }`}>
                    {claim.status}
                  </span>
                </td>
                <td className="py-3 px-4 text-xs text-slate-300 max-w-xs truncate italic">
                  {claim.debrief_notes || <span className="text-slate-500">Pending debrief...</span>}
                </td>
                <td className="py-3 px-4 text-right">
                  {claim.status === 'ACTIVE' ? (
                    <button
                      onClick={() => onOpenDebriefModal(claim)}
                      className="px-3 py-1 rounded bg-[#252038] hover:bg-[#342d4d] border border-purple-500/50 text-purple-200 text-xs font-semibold flex items-center gap-1 ml-auto transition"
                    >
                      <FileText className="w-3.5 h-3.5 text-purple-400" /> Log Debrief
                    </button>
                  ) : (
                    <button
                      onClick={() => onOpenDebriefModal(claim)}
                      className="px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold ml-auto transition"
                    >
                      Edit Debrief
                    </button>
                  )}
                </td>
              </tr>
            ))}
            {claims.length === 0 && (
              <tr>
                <td colSpan="7" className="text-center py-8 text-slate-500 italic">
                  No mission claims logged. Dispatch an operative to start an active mission claim.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
