import React, { useState } from 'react';
import { Users, Shield, Plus, AlertTriangle, CheckCircle, Zap, Trash2, Edit3, Sparkles, Building2, Compass, Award, Clock } from 'lucide-react';
import BeyonderAvatar from './BeyonderAvatar';

export default function SquadFormation({
  squads,
  beyonders,
  commissions,
  onCreateSquad,
  onUpdateSquad,
  onDeleteSquad,
  onDispatchSquad
}) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingSquad, setEditingSquad] = useState(null);
  const [squadName, setSquadName] = useState('');
  const [motto, setMotto] = useState('');
  const [formationType, setFormationType] = useState('BALANCED');
  const [selectedMemberIds, setSelectedMemberIds] = useState([]);
  const [memberRoles, setMemberRoles] = useState({});
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Dispatch squad state
  const [dispatchingSquad, setDispatchingSquad] = useState(null);
  const [selectedCommissionId, setSelectedCommissionId] = useState('');

  const defaultRoles = ['Squad Leader', 'Vanguard', 'Controller', 'Support'];

  const openCreateModal = () => {
    setEditingSquad(null);
    setSquadName('');
    setMotto('');
    setFormationType('BALANCED');
    setSelectedMemberIds([]);
    setMemberRoles({});
    setErrorMessage('');
    setIsModalOpen(true);
  };

  const openEditModal = (squad) => {
    setEditingSquad(squad);
    setSquadName(squad.name);
    setMotto(squad.motto || '');
    setFormationType(squad.formation_type || 'BALANCED');
    const ids = squad.members.map(m => m.beyonder_id);
    setSelectedMemberIds(ids);
    const roles = {};
    squad.members.forEach(m => {
      roles[m.beyonder_id] = m.role;
    });
    setMemberRoles(roles);
    setErrorMessage('');
    setIsModalOpen(true);
  };

  const toggleMemberSelection = (beyonderId) => {
    if (selectedMemberIds.includes(beyonderId)) {
      setSelectedMemberIds(selectedMemberIds.filter(id => id !== beyonderId));
      const newRoles = { ...memberRoles };
      delete newRoles[beyonderId];
      setMemberRoles(newRoles);
      setErrorMessage('');
    } else {
      if (selectedMemberIds.length >= 4) {
        setErrorMessage('Squad formation is strictly limited to a maximum of 4 members.');
        return;
      }
      const newSelected = [...selectedMemberIds, beyonderId];
      setSelectedMemberIds(newSelected);
      const roleIndex = newSelected.length - 1;
      const assignedRole = defaultRoles[roleIndex] || 'Specialist';
      setMemberRoles({ ...memberRoles, [beyonderId]: assignedRole });
      setErrorMessage('');
    }
  };

  const handleRoleChange = (beyonderId, newRole) => {
    setMemberRoles({ ...memberRoles, [beyonderId]: newRole });
  };

  const handleSaveSquad = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    if (!squadName.trim()) {
      setErrorMessage('Squad name is required.');
      return;
    }

    // STRICT VALIDATION: Squad must be between 3 and 4 members only!
    if (selectedMemberIds.length < 3) {
      setErrorMessage('Squad formation strictly requires a minimum of 3 operatives.');
      return;
    }
    if (selectedMemberIds.length > 4) {
      setErrorMessage('Squad formation is strictly limited to 3-4 members only.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        name: squadName.trim(),
        motto: motto.trim() || undefined,
        formation_type: formationType,
        member_ids: selectedMemberIds,
        member_roles: memberRoles
      };

      if (editingSquad) {
        await onUpdateSquad(editingSquad.id, payload);
      } else {
        await onCreateSquad(payload);
      }
      setIsModalOpen(false);
    } catch (err) {
      setErrorMessage(err.response?.data?.detail || err.message || 'Failed to save squad');
    } finally {
      setLoading(false);
    }
  };

  const handleDispatchSubmit = async (e) => {
    e.preventDefault();
    if (!dispatchingSquad || !selectedCommissionId) return;

    setLoading(true);
    try {
      await onDispatchSquad(dispatchingSquad.id, Number(selectedCommissionId));
      setDispatchingSquad(null);
      setSelectedCommissionId('');
    } catch (err) {
      alert(err.response?.data?.detail || err.message || 'Dispatch failed');
    } finally {
      setLoading(false);
    }
  };

  const openCommissions = commissions.filter(c => c.status === 'OPEN');

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="gothic-card p-6 rounded-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs uppercase font-serif tracking-widest text-[#d4af37] px-2.5 py-0.5 rounded border border-[#d4af37]/30 bg-[#d4af37]/10">
              Tactical Unit Registry
            </span>
            <span className="text-xs uppercase font-serif tracking-wider text-purple-300 px-2.5 py-0.5 rounded border border-purple-500/30 bg-purple-950/40">
              Capacity: 3–4 Operatives
            </span>
          </div>
          <h2 className="text-xl font-serif font-bold text-[#e6c656] mt-2 gold-glow flex items-center gap-2">
            <Users className="w-6 h-6 text-[#d4af37]" /> Beyonder Squad Formation & Strike Units
          </h2>
          <p className="text-xs text-slate-400 font-serif mt-1">
            Assemble specialized combat and investigation squads. Each tactical unit is strictly limited to <strong>3 to 4 members</strong> to preserve mental stability and prevent corruption resonance.
          </p>
        </div>

        <button
          onClick={openCreateModal}
          className="px-4 py-2 rounded-md bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/60 text-[#e6c656] font-serif text-sm font-semibold flex items-center gap-2 transition shadow-lg shadow-amber-950/50 cursor-pointer shrink-0"
        >
          <Plus className="w-4 h-4 text-[#d4af37]" /> Form New Squad (3-4 Members)
        </button>
      </div>

      {/* Squad Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {squads.map(squad => (
          <div
            key={squad.id}
            className="gothic-card p-6 rounded-lg space-y-5 border border-[#c5a059]/30 relative overflow-hidden"
          >
            {/* Squad Header */}
            <div className="flex items-start justify-between gap-3 border-b border-slate-800 pb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[11px] font-bold border border-purple-500/40 bg-purple-950/60 text-purple-200">
                    {squad.formation_type}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-[11px] font-bold border ${
                    squad.status === 'READY'
                      ? 'border-emerald-500/40 bg-emerald-950/60 text-emerald-300'
                      : 'border-amber-500/40 bg-amber-950/60 text-amber-300 animate-pulse'
                  }`}>
                    {squad.status}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">
                    {squad.member_count}/4 Members
                  </span>
                </div>
                <h3 className="text-lg font-serif font-bold text-[#e6c656] mt-1 gold-glow">
                  {squad.name}
                </h3>
                {squad.motto && (
                  <p className="text-xs text-slate-400 font-serif italic mt-0.5">
                    "{squad.motto}"
                  </p>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-1.5 shrink-0">
                <button
                  onClick={() => openEditModal(squad)}
                  className="p-1.5 rounded hover:bg-[#252836] text-slate-400 hover:text-[#d4af37] transition"
                  title="Edit Squad"
                >
                  <Edit3 className="w-4 h-4" />
                </button>
                <button
                  onClick={() => onDeleteSquad(squad.id)}
                  className="p-1.5 rounded hover:bg-red-950/60 text-slate-400 hover:text-red-400 transition"
                  title="Disband Squad"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Squad Tactical Stats Bar */}
            <div className="grid grid-cols-3 gap-2 p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-center text-xs font-serif">
              <div>
                <span className="text-slate-400 text-[10px] uppercase block">Avg Sequence</span>
                <span className="font-bold text-purple-300 text-sm">Seq {squad.average_sequence}</span>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] uppercase block">Hazard Clearance</span>
                <span className="font-bold text-[#d4af37] text-sm">Rank {squad.hazard_clearance}</span>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] uppercase block">Avg Sanity</span>
                <span className={`font-bold text-sm ${squad.average_sanity > 70 ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {squad.average_sanity}%
                </span>
              </div>
            </div>

            {/* Squad Members (3-4 Slots) */}
            <div className="space-y-2">
              <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold block">
                Assigned Squad Operatives ({squad.member_count}/4):
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {squad.members.map(member => (
                  <div
                    key={member.id}
                    className="p-2 rounded bg-[#0d0e12]/80 border border-[#272a38] flex items-center gap-3"
                  >
                    <BeyonderAvatar
                      avatarUrl={member.avatar_url}
                      name={member.codename}
                      sequenceLevel={member.sequence_level}
                      pathway={member.pathway_name}
                      size="sm"
                    />
                    <div className="overflow-hidden min-w-0 flex-1">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-serif font-bold text-slate-200 truncate block">
                          {member.codename}
                        </span>
                      </div>
                      <div className="flex items-center gap-1.5 text-[10px] text-slate-400">
                        <span className="text-[#d4af37] font-semibold">{member.role}</span>
                        <span>•</span>
                        <span className="truncate">{member.sequence_name || `Seq ${member.sequence_level}`}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Synergies */}
            {squad.synergies && squad.synergies.length > 0 && (
              <div className="p-2.5 rounded bg-[#13101c] border border-purple-900/40 text-xs font-serif space-y-1">
                <span className="text-[10px] uppercase font-bold text-purple-300 flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-[#d4af37]" /> Pathway Synergies:
                </span>
                {squad.synergies.map((syn, idx) => (
                  <p key={idx} className="text-slate-300 text-[11px] italic pl-2 border-l border-purple-500/40">
                    "{syn}"
                  </p>
                ))}
              </div>
            )}

            {/* Bottom Actions */}
            <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
              <span className="text-xs text-slate-400 font-serif">
                Eligible for Hazard Rank ≤ {squad.hazard_clearance} missions
              </span>
              {squad.status === 'READY' ? (
                <button
                  onClick={() => setDispatchingSquad(squad)}
                  className="px-3.5 py-1.5 rounded bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/60 text-[#e6c656] text-xs font-serif font-semibold transition flex items-center gap-1.5 cursor-pointer shadow"
                >
                  <Zap className="w-3.5 h-3.5 text-[#d4af37]" /> Dispatch Squad
                </button>
              ) : (
                <span className="px-3 py-1 rounded bg-slate-800 text-slate-400 text-xs font-serif">
                  Unit Currently Deployed
                </span>
              )}
            </div>
          </div>
        ))}

        {squads.length === 0 && (
          <div className="col-span-full gothic-card p-12 text-center text-slate-500 font-serif italic">
            No squads currently formed. Click "Form New Squad" to assemble an elite 3 to 4 member strike team.
          </div>
        )}
      </div>

      {/* Squad Formation Modal (Strict 3-4 Limit) */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 overflow-y-auto">
          <div className="gothic-card gothic-card-gold max-w-2xl w-full p-6 rounded-lg space-y-5 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-[#c5a059]/30 pb-3">
              <div>
                <h3 className="text-lg font-serif font-bold text-[#e6c656] gold-glow flex items-center gap-2">
                  <Users className="w-5 h-5 text-[#d4af37]" />
                  {editingSquad ? 'Reconfigure Squad Formation' : 'Assemble Strike Squad'}
                </h3>
                <p className="text-xs text-slate-400 font-serif">
                  Strict Rule: Operatives must number between <strong>3 and 4 members only</strong>.
                </p>
              </div>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-200">
                ✕
              </button>
            </div>

            <form onSubmit={handleSaveSquad} className="space-y-4 font-serif text-sm">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                    Squad Name:
                  </label>
                  <input
                    type="text"
                    required
                    value={squadName}
                    onChange={(e) => setSquadName(e.target.value)}
                    placeholder="e.g., Tingen Nighthawks Strike Team"
                    className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
                  />
                </div>

                <div className="space-y-1">
                  <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                    Formation Stance:
                  </label>
                  <select
                    value={formationType}
                    onChange={(e) => setFormationType(e.target.value)}
                    className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
                  >
                    <option value="BALANCED">Balanced Formation</option>
                    <option value="ASSAULT">Assault / High-Damage</option>
                    <option value="DEFENSIVE">Defensive / Bastion</option>
                    <option value="INVESTIGATION">Mystical Investigation</option>
                    <option value="RITUAL">Ritualistic Exorcism</option>
                  </select>
                </div>
              </div>

              <div className="space-y-1">
                <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                  Squad Motto / Oath:
                </label>
                <input
                  type="text"
                  value={motto}
                  onChange={(e) => setMotto(e.target.value)}
                  placeholder="e.g., We are guardians, but also miserable wretches."
                  className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
                />
              </div>

              {/* Member Selection Status Banner */}
              <div className={`p-3 rounded border text-xs font-semibold flex items-center justify-between ${
                selectedMemberIds.length >= 3 && selectedMemberIds.length <= 4
                  ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300'
                  : 'bg-amber-950/40 border-amber-500/50 text-amber-300'
              }`}>
                <span>Selected Operatives: <strong>{selectedMemberIds.length} / 4</strong></span>
                <span>
                  {selectedMemberIds.length < 3 && `⚠️ Need ${3 - selectedMemberIds.length} more member(s) to reach minimum 3.`}
                  {selectedMemberIds.length === 3 && `✓ Valid Squad (3/4). You can deploy now or add 1 more.`}
                  {selectedMemberIds.length === 4 && `✓ Full Squad (4/4). Maximum capacity reached.`}
                </span>
              </div>

              {/* Roster Selection Section */}
              <div className="space-y-2">
                <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                  Select 3 to 4 Operatives from Roster:
                </label>
                <div className="max-h-60 overflow-y-auto grid grid-cols-1 sm:grid-cols-2 gap-2 p-2 rounded bg-[#090b10] border border-[#272a38]">
                  {beyonders.map(agent => {
                    const isSelected = selectedMemberIds.includes(agent.id);
                    return (
                      <div
                        key={agent.id}
                        onClick={() => toggleMemberSelection(agent.id)}
                        className={`p-2 rounded border transition cursor-pointer flex items-center gap-3 ${
                          isSelected
                            ? 'bg-[#252038] border-[#d4af37] shadow-sm'
                            : selectedMemberIds.length >= 4
                            ? 'bg-[#0d0e12]/50 border-slate-800 opacity-60'
                            : 'bg-[#0d0e12] border-slate-800 hover:border-slate-600'
                        }`}
                      >
                        <BeyonderAvatar
                          avatarUrl={agent.avatar_url}
                          name={agent.codename}
                          sequenceLevel={agent.sequence_level}
                          pathway={agent.pathway_name}
                          size="sm"
                        />
                        <div className="overflow-hidden min-w-0 flex-1">
                          <span className={`text-xs font-semibold truncate block ${isSelected ? 'text-[#e6c656]' : 'text-slate-200'}`}>
                            {agent.codename}
                          </span>
                          <span className="text-[10px] text-slate-400 block truncate">
                            Seq {agent.sequence_level} • {agent.pathway_name} • {agent.affiliation}
                          </span>
                        </div>
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => {}}
                          className="accent-[#d4af37]"
                        />
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Role Assignment for Selected Members */}
              {selectedMemberIds.length > 0 && (
                <div className="space-y-2 pt-2 border-t border-slate-800">
                  <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                    Assign Roles to Selected Operatives:
                  </label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {selectedMemberIds.map((id, index) => {
                      const agent = beyonders.find(b => b.id === id);
                      if (!agent) return null;
                      return (
                        <div key={id} className="p-2 rounded bg-[#0d0e12] border border-[#272a38] flex items-center justify-between gap-2">
                          <span className="text-xs text-slate-200 truncate font-semibold">
                            {agent.codename}
                          </span>
                          <select
                            value={memberRoles[id] || defaultRoles[index] || 'Vanguard'}
                            onChange={(e) => handleRoleChange(id, e.target.value)}
                            className="p-1 rounded bg-[#181a24] border border-[#272a38] text-[11px] text-[#e6c656] focus:outline-none focus:border-[#d4af37]"
                          >
                            <option value="Squad Leader">Squad Leader</option>
                            <option value="Vanguard">Vanguard</option>
                            <option value="Controller">Controller</option>
                            <option value="Support">Support</option>
                            <option value="Specialist">Specialist</option>
                            <option value="Diviner">Diviner</option>
                          </select>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {errorMessage && (
                <div className="p-3 rounded bg-red-950/80 border border-red-500 text-red-200 text-xs font-bold flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
                  <span>{errorMessage}</span>
                </div>
              )}

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 rounded bg-slate-800 text-slate-300 text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading || selectedMemberIds.length < 3 || selectedMemberIds.length > 4}
                  className={`px-5 py-2 rounded text-xs font-semibold transition ${
                    selectedMemberIds.length < 3 || selectedMemberIds.length > 4
                      ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                      : 'bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/80 text-[#e6c656] cursor-pointer shadow'
                  }`}
                >
                  {loading ? 'Saving Formation...' : editingSquad ? 'Save Squad Changes' : 'Confirm Squad Formation (3-4)'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Dispatch Squad Modal */}
      {dispatchingSquad && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="gothic-card gothic-card-gold max-w-md w-full p-6 rounded-lg space-y-5">
            <div className="flex items-center justify-between border-b border-[#c5a059]/30 pb-3">
              <h3 className="text-lg font-serif font-bold text-[#e6c656] gold-glow flex items-center gap-2">
                <Zap className="w-5 h-5 text-[#d4af37]" /> Deploy Full Squad
              </h3>
              <button onClick={() => setDispatchingSquad(null)} className="text-slate-400 hover:text-slate-200">
                ✕
              </button>
            </div>

            <form onSubmit={handleDispatchSubmit} className="space-y-4 font-serif text-sm">
              <div className="p-3 rounded bg-[#0d0e12] border border-[#272a38] text-xs space-y-1">
                <p className="text-slate-300">
                  Deploying Squad: <strong className="text-[#e6c656]">{dispatchingSquad.name}</strong> ({dispatchingSquad.member_count} Operatives)
                </p>
                <p className="text-slate-400">
                  Squad Clearance: <strong className="text-purple-300">Hazard Rank ≤ {dispatchingSquad.hazard_clearance}</strong>
                </p>
              </div>

              <div className="space-y-1">
                <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                  Select Open Commission:
                </label>
                <select
                  required
                  value={selectedCommissionId}
                  onChange={(e) => setSelectedCommissionId(e.target.value)}
                  className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
                >
                  <option value="">-- Choose Commission --</option>
                  {openCommissions.map(c => (
                    <option key={c.id} value={c.id}>
                      {c.title} (Hazard Rank {c.hazard_rank}) - Reward: £{c.reward_gold}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setDispatchingSquad(null)}
                  className="px-4 py-2 rounded bg-slate-800 text-slate-300 text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading || !selectedCommissionId}
                  className="px-5 py-2 rounded bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/80 text-[#e6c656] text-xs font-semibold cursor-pointer shadow"
                >
                  {loading ? 'Deploying...' : 'Deploy Squad on Mission'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
