import React, { useState } from 'react';
import { Search, Plus, Filter, AlertTriangle, Shield, UserX, Edit2, ChevronDown, ChevronUp, Sparkles, Building2, Flame, Eye, X } from 'lucide-react';
import BeyonderAvatar from './BeyonderAvatar';

export default function BeyonderDirectory({
  beyonders,
  pathways,
  onOpenAddModal,
  onOpenEditModal,
  onDeleteBeyonder
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPathway, setSelectedPathway] = useState('');
  const [selectedAffiliation, setSelectedAffiliation] = useState('');
  const [expandedAgentId, setExpandedAgentId] = useState(null);
  const [inspectingAgent, setInspectingAgent] = useState(null);

  const filteredBeyonders = beyonders.filter(b => {
    const term = searchTerm.toLowerCase();
    const matchesSearch = b.codename.toLowerCase().includes(term) ||
                          b.affiliation.toLowerCase().includes(term) ||
                          (b.sequence_name && b.sequence_name.toLowerCase().includes(term)) ||
                          (b.characteristics && b.characteristics.toLowerCase().includes(term));
    const matchesPathway = selectedPathway === '' || b.pathway_id === Number(selectedPathway);
    const matchesAffiliation = selectedAffiliation === '' || b.affiliation === selectedAffiliation;
    return matchesSearch && matchesPathway && matchesAffiliation;
  });

  const affiliations = Array.from(new Set(beyonders.map(b => b.affiliation))).sort();

  const toggleExpand = (id) => {
    setExpandedAgentId(expandedAgentId === id ? null : id);
  };

  return (
    <div className="space-y-6">
      {/* Top Header & Search Bar */}
      <div className="gothic-card p-6 rounded-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-serif font-bold text-[#e6c656] flex items-center gap-2 gold-glow">
            <Shield className="w-6 h-6 text-[#d4af37]" /> Beyonder Operative & Divine Member Directory
          </h2>
          <p className="text-xs text-slate-400 font-serif mt-1">
            Enlisted registry of active Beyonders, high-sequence deities, church leaders, pirate admirals, visual tarot portraits, and supernatural characteristics.
          </p>
        </div>
        <button
          onClick={onOpenAddModal}
          className="px-4 py-2 rounded-md bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/60 text-[#e6c656] font-serif text-sm font-semibold flex items-center gap-2 transition shadow-lg shadow-amber-950/50 cursor-pointer"
        >
          <Plus className="w-4 h-4 text-[#d4af37]" /> Induct New Beyonder
        </button>
      </div>

      {/* Filters Bar */}
      <div className="gothic-card p-4 rounded-lg flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search member, sequence, trait, artifact..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-sm font-serif focus:outline-none focus:border-[#d4af37]"
          />
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          {/* Pathway Filter (All 22) */}
          <select
            value={selectedPathway}
            onChange={(e) => setSelectedPathway(e.target.value)}
            className="px-3 py-2 rounded bg-[#0d0e12] border border-[#272a38] text-slate-300 text-sm font-serif focus:outline-none focus:border-[#d4af37]"
          >
            <option value="">All Divine Pathways ({pathways.length})</option>
            {pathways.map(p => (
              <option key={p.id} value={p.id}>
                {p.name} ({p.sequence_0_title})
              </option>
            ))}
          </select>

          {/* Affiliation / Organization Filter */}
          <select
            value={selectedAffiliation}
            onChange={(e) => setSelectedAffiliation(e.target.value)}
            className="px-3 py-2 rounded bg-[#0d0e12] border border-[#272a38] text-slate-300 text-sm font-serif focus:outline-none focus:border-[#d4af37]"
          >
            <option value="">All Organizations ({affiliations.length})</option>
            {affiliations.map(aff => (
              <option key={aff} value={aff}>{aff}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Summary Counts Bar */}
      <div className="flex items-center justify-between px-2 text-xs font-serif text-slate-400">
        <span>Enlisted Operatives: <strong className="text-[#e6c656]">{filteredBeyonders.length}</strong></span>
        <span>Organizations Enrolled: <strong className="text-purple-300">{affiliations.length}</strong></span>
      </div>

      {/* Beyonder Table */}
      <div className="gothic-card p-6 rounded-lg overflow-x-auto">
        <table className="w-full text-left font-serif text-sm">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 uppercase text-xs">
              <th className="py-3 px-3">Portrait</th>
              <th className="py-3 px-4">Operative / Deity</th>
              <th className="py-3 px-4">Pathway</th>
              <th className="py-3 px-4">Sequence & Rank</th>
              <th className="py-3 px-4">Organization</th>
              <th className="py-3 px-4">Sanity / Corruption</th>
              <th className="py-3 px-4 text-center">Characteristics</th>
              <th className="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filteredBeyonders.map((agent) => {
              const sanity = agent.sanity_percentage;
              let sanityColor = 'bg-emerald-500';
              let textColor = 'text-emerald-400';

              if (sanity < 30) {
                sanityColor = 'bg-red-600 animate-pulse';
                textColor = 'text-red-400 font-bold';
              } else if (sanity < 70) {
                sanityColor = 'bg-amber-500';
                textColor = 'text-amber-400';
              }

              const isExpanded = expandedAgentId === agent.id;

              return (
                <React.Fragment key={agent.id}>
                  <tr className={`hover:bg-[#191c28]/60 transition ${isExpanded ? 'bg-[#151722]' : ''}`}>
                    {/* Character Picture / Avatar */}
                    <td className="py-3 px-3">
                      <BeyonderAvatar
                        avatarUrl={agent.avatar_url}
                        name={agent.codename}
                        sequenceLevel={agent.sequence_level}
                        pathway={agent.pathway_name || 'Fool'}
                        size="md"
                        onClick={() => setInspectingAgent(agent)}
                      />
                    </td>

                    <td className="py-3 px-4 font-semibold text-slate-100">
                      <div className="flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full ${agent.sequence_level <= 3 ? 'bg-[#d4af37] shadow-sm shadow-amber-400' : 'bg-slate-500'}`}></span>
                        <span
                          className={`cursor-pointer hover:underline ${agent.sequence_level === 0 ? 'text-[#e6c656] font-bold gold-glow' : 'text-slate-100'}`}
                          onClick={() => setInspectingAgent(agent)}
                        >
                          {agent.codename}
                        </span>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-[#e6c656] font-medium">
                      {agent.pathway_name || 'Unknown'}
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex flex-col gap-0.5">
                        <span className={`px-2 py-0.5 rounded text-xs font-semibold inline-block w-fit ${
                          agent.sequence_level <= 2
                            ? 'bg-purple-950/80 border border-purple-500/60 text-purple-200'
                            : agent.sequence_level <= 4
                            ? 'bg-amber-950/80 border border-amber-500/60 text-amber-200'
                            : 'bg-slate-900 border border-slate-700 text-slate-300'
                        }`}>
                          Seq {agent.sequence_level}
                        </span>
                        {agent.sequence_name && (
                          <span className="text-[11px] text-slate-300 italic">
                            {agent.sequence_name}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-1 rounded bg-[#0d0e12] border border-[#272a38] text-xs text-slate-300 flex items-center gap-1.5 w-fit">
                        <Building2 className="w-3 h-3 text-[#d4af37]" />
                        {agent.affiliation}
                      </span>
                    </td>
                    <td className="py-3 px-4 min-w-[180px]">
                      <div className="flex items-center gap-2">
                        <div className="w-full bg-[#0d0e12] rounded-full h-2.5 border border-[#272a38] overflow-hidden p-0.5">
                          <div
                            className={`h-full rounded-full transition-all duration-500 ${sanityColor}`}
                            style={{ width: `${Math.max(0, Math.min(100, sanity))}%` }}
                          ></div>
                        </div>
                        <span className={`text-xs w-10 text-right ${textColor}`}>
                          {sanity.toFixed(0)}%
                        </span>
                        {sanity < 30 && (
                          <AlertTriangle className="w-3.5 h-3.5 text-red-500 animate-bounce shrink-0" title="High Madness/Corruption Risk!" />
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <button
                        onClick={() => toggleExpand(agent.id)}
                        className={`px-2.5 py-1 rounded text-xs font-serif transition flex items-center gap-1 mx-auto cursor-pointer ${
                          isExpanded
                            ? 'bg-[#252038] text-[#e6c656] border border-[#d4af37]/50'
                            : 'bg-[#0d0e12] text-slate-400 hover:text-slate-200 border border-slate-800'
                        }`}
                      >
                        <Sparkles className="w-3 h-3 text-[#d4af37]" />
                        <span>Traits</span>
                        {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                      </button>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => onOpenEditModal(agent)}
                          className="p-1.5 rounded hover:bg-[#252836] text-slate-400 hover:text-[#d4af37] transition cursor-pointer"
                          title="Edit Operative"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => onDeleteBeyonder(agent.id)}
                          className="p-1.5 rounded hover:bg-red-950/60 text-slate-400 hover:text-red-400 transition cursor-pointer"
                          title="Decommission Operative"
                        >
                          <UserX className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>

                  {/* Expanded Characteristics Row */}
                  {isExpanded && (
                    <tr className="bg-[#11131b]">
                      <td colSpan="8" className="p-4 border-b border-[#c5a059]/20">
                        <div className="p-4 rounded-lg bg-[#0d0e12] border border-[#272a38] flex flex-col md:flex-row gap-5 items-start">
                          <BeyonderAvatar
                            avatarUrl={agent.avatar_url}
                            name={agent.codename}
                            sequenceLevel={agent.sequence_level}
                            pathway={agent.pathway_name || 'Fool'}
                            size="xl"
                            onClick={() => setInspectingAgent(agent)}
                          />
                          <div className="flex-1 space-y-2">
                            <div className="flex items-center justify-between">
                              <span className="text-xs uppercase font-serif tracking-wider text-[#d4af37] font-semibold flex items-center gap-1.5">
                                <Sparkles className="w-3.5 h-3.5" /> Canonical Characteristics, Sealed Artifacts & Traits:
                              </span>
                              <span className="text-xs text-purple-300 font-mono">
                                Sequence {agent.sequence_level}: {agent.sequence_name || 'Operative'}
                              </span>
                            </div>
                            <p className="text-xs text-slate-300 leading-relaxed font-serif italic bg-[#151722] p-3 rounded border border-slate-800/80">
                              {agent.characteristics || "No specialized characteristics recorded for this operative."}
                            </p>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}

            {filteredBeyonders.length === 0 && (
              <tr>
                <td colSpan="8" className="text-center py-10 text-slate-500 italic">
                  No Beyonder operatives match the specified filter criteria.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Tarot Card Preview Modal */}
      {inspectingAgent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4 animate-in fade-in">
          <div className="gothic-card gothic-card-gold max-w-sm w-full p-6 rounded-lg space-y-4 text-center relative">
            <button
              onClick={() => setInspectingAgent(null)}
              className="absolute top-3 right-3 text-slate-400 hover:text-slate-100 p-1"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="mx-auto w-48 h-56 rounded-lg overflow-hidden border-2 border-[#d4af37] shadow-xl shadow-amber-950/40 bg-black">
              {inspectingAgent.avatar_url ? (
                <img
                  src={inspectingAgent.avatar_url}
                  alt={inspectingAgent.codename}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center bg-[#181424] text-[#e6c656] text-xl font-serif">
                  🎴
                </div>
              )}
            </div>

            <div>
              <span className="text-[11px] uppercase tracking-widest text-purple-300 block">
                {inspectingAgent.pathway_name} Pathway • Sequence {inspectingAgent.sequence_level}
              </span>
              <h3 className="text-lg font-serif font-bold text-[#e6c656] gold-glow mt-0.5">
                {inspectingAgent.codename}
              </h3>
              <p className="text-xs text-amber-300 italic">
                {inspectingAgent.sequence_name || inspectingAgent.pathway_name}
              </p>
            </div>

            <div className="p-3 rounded bg-[#0d0e12] border border-[#272a38] text-left text-xs font-serif space-y-1.5">
              <div className="flex justify-between text-slate-400">
                <span>Affiliation:</span>
                <span className="text-slate-200 font-semibold">{inspectingAgent.affiliation}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Sanity Status:</span>
                <span className={inspectingAgent.sanity_percentage > 70 ? 'text-emerald-400' : 'text-amber-400'}>
                  {inspectingAgent.sanity_percentage}%
                </span>
              </div>
              <p className="text-[11px] text-slate-300 italic pt-1 border-t border-slate-800">
                "{inspectingAgent.characteristics}"
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
