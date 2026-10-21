import React, { useState } from 'react';
import { Scroll, Plus, Search, Filter, AlertOctagon, CheckCircle2, Clock, Trash2 } from 'lucide-react';

export default function CommissionBoard({
  commissions,
  onOpenAddModal,
  onOpenDispatchModal,
  onDeleteCommission
}) {
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [hazardFilter, setHazardFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredCommissions = commissions.filter(c => {
    const matchesStatus = statusFilter === 'ALL' || c.status === statusFilter;
    const matchesHazard = hazardFilter === '' || c.hazard_rank === Number(hazardFilter);
    const matchesSearch = searchQuery === '' ||
                          c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          c.target.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          c.location.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesHazard && matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="gothic-card p-6 rounded-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-serif font-bold text-[#e6c656] flex items-center gap-2 gold-glow">
            <Scroll className="w-6 h-6 text-[#d4af37]" /> Victorian Commission Board
          </h2>
          <p className="text-xs text-slate-400 font-serif mt-1">
            Live task registry for supernatural investigations, purifications, and relic escorts across Loen Kingdom.
          </p>
        </div>
        <button
          onClick={onOpenAddModal}
          className="px-4 py-2 rounded-md bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/60 text-[#e6c656] font-serif text-sm font-semibold flex items-center gap-2 transition shadow-lg shadow-amber-950/50"
        >
          <Plus className="w-4 h-4 text-[#d4af37]" /> Issue New Commission
        </button>
      </div>

      {/* Filter & Search Bar */}
      <div className="gothic-card p-4 rounded-lg flex flex-col md:flex-row gap-4 items-center justify-between">
        {/* Status Tabs */}
        <div className="flex items-center gap-1 bg-[#0d0e12] p-1 rounded border border-[#272a38]">
          {['ALL', 'OPEN', 'CLAIMED', 'COMPLETED'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1.5 rounded text-xs font-serif transition ${
                statusFilter === st
                  ? 'bg-[#252038] text-[#e6c656] font-bold border border-[#d4af37]/40'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {st}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          {/* Hazard Rank Selector */}
          <select
            value={hazardFilter}
            onChange={(e) => setHazardFilter(e.target.value)}
            className="px-3 py-2 rounded bg-[#0d0e12] border border-[#272a38] text-slate-300 text-sm font-serif focus:outline-none focus:border-[#d4af37]"
          >
            <option value="">All Hazard Ranks</option>
            {[0,1,2,3,4,5,6,7,8,9].map(r => (
              <option key={r} value={r}>Hazard Rank {r}</option>
            ))}
          </select>

          {/* Search Input */}
          <div className="relative w-full md:w-60">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search title or location..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-sm font-serif focus:outline-none focus:border-[#d4af37]"
            />
          </div>
        </div>
      </div>

      {/* Commissions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCommissions.map((comm) => {
          let statusBadgeClass = 'bg-emerald-950/60 border-emerald-500/50 text-emerald-300';
          let StatusIcon = CheckCircle2;

          if (comm.status === 'OPEN') {
            statusBadgeClass = 'bg-amber-950/60 border-amber-500/50 text-amber-300';
            StatusIcon = Clock;
          } else if (comm.status === 'CLAIMED') {
            statusBadgeClass = 'bg-purple-950/60 border-purple-500/50 text-purple-300';
            StatusIcon = AlertOctagon;
          }

          return (
            <div
              key={comm.id}
              className={`gothic-card p-5 rounded-lg flex flex-col justify-between space-y-4 ${
                comm.hazard_rank >= 5 ? 'gothic-card-crimson' : ''
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <span className={`px-2.5 py-0.5 rounded text-xs border font-bold flex items-center gap-1 ${statusBadgeClass}`}>
                    <StatusIcon className="w-3 h-3" />
                    {comm.status}
                  </span>
                  <span className={`px-2.5 py-0.5 rounded text-xs border font-bold ${
                    comm.hazard_rank <= 3 ? 'bg-purple-950/60 border-purple-500/50 text-purple-300' :
                    comm.hazard_rank <= 6 ? 'bg-amber-950/60 border-amber-500/50 text-amber-300' :
                    'bg-red-950/60 border-red-500/50 text-red-300 animate-pulse'
                  }`}>
                    Hazard Rank {comm.hazard_rank}
                  </span>
                </div>

                <div>
                  <h3 className="text-base font-serif font-bold text-[#e6c656] leading-tight">
                    {comm.title}
                  </h3>
                  <p className="text-xs text-slate-400 font-serif mt-1">
                    Location: <span className="text-slate-300">{comm.location}</span>
                  </p>
                </div>

                <div className="p-3 rounded bg-[#0d0e12]/80 border border-slate-800 text-xs font-serif space-y-1">
                  <p className="text-slate-300">
                    <span className="text-slate-400">Target / Threat:</span> {comm.target}
                  </p>
                  <p className="text-amber-300 font-semibold">
                    <span>Reward:</span> {comm.reward_gold} Gold Pounds (£)
                  </p>
                </div>
              </div>

              {/* Bottom Actions */}
              <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
                <button
                  onClick={() => onDeleteCommission(comm.id)}
                  className="text-xs text-slate-500 hover:text-red-400 flex items-center gap-1 transition"
                >
                  <Trash2 className="w-3.5 h-3.5" /> Remove
                </button>

                {comm.status === 'OPEN' && (
                  <button
                    onClick={() => onOpenDispatchModal(comm)}
                    className="px-3 py-1.5 rounded bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/60 text-[#e6c656] text-xs font-serif font-semibold transition shadow"
                  >
                    Dispatch Agent
                  </button>
                )}
              </div>
            </div>
          );
        })}

        {filteredCommissions.length === 0 && (
          <div className="col-span-full gothic-card p-10 text-center text-slate-500 italic font-serif">
            No commissions found matching the filter criteria.
          </div>
        )}
      </div>
    </div>
  );
}
