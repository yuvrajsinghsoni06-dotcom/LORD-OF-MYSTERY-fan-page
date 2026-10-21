import React, { useState, useEffect } from 'react';
import { X, Shield, AlertTriangle, CheckCircle, Zap } from 'lucide-react';

export default function DispatchModal({
  isOpen,
  onClose,
  commissions,
  beyonders,
  preselectedCommission,
  onDispatchSuccess
}) {
  const [selectedCommissionId, setSelectedCommissionId] = useState('');
  const [selectedBeyonderId, setSelectedBeyonderId] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (preselectedCommission) {
      setSelectedCommissionId(preselectedCommission.id);
    } else if (commissions.filter(c => c.status === 'OPEN').length > 0) {
      setSelectedCommissionId(commissions.filter(c => c.status === 'OPEN')[0].id);
    }
  }, [preselectedCommission, commissions, isOpen]);

  if (!isOpen) return null;

  const currentCommission = commissions.find(c => c.id === Number(selectedCommissionId));
  const currentBeyonder = beyonders.find(b => b.id === Number(selectedBeyonderId));

  // Sequence Level Validation Logic
  // Beyonder sequence 0 is God (highest power), sequence 9 is Novice (lowest power).
  // Formula: beyonder.sequence_level <= commission.hazard_rank
  let isEligible = null;
  if (currentCommission && currentBeyonder) {
    isEligible = currentBeyonder.sequence_level <= currentCommission.hazard_rank;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    if (!selectedCommissionId || !selectedBeyonderId) {
      setErrorMessage('Please select both a commission and a Beyonder agent.');
      return;
    }

    if (isEligible === false) {
      setErrorMessage('Sequence rank insufficient for commission hazard level');
      return;
    }

    setLoading(true);
    try {
      await onDispatchSuccess(Number(selectedCommissionId), Number(selectedBeyonderId));
      onClose();
    } catch (err) {
      const serverError = err.response?.data?.detail || err.message || 'Dispatch failed';
      setErrorMessage(serverError);
    } finally {
      setLoading(false);
    }
  };

  const openCommissions = commissions.filter(c => c.status === 'OPEN');

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="gothic-card gothic-card-gold w-full max-w-lg p-6 rounded-lg space-y-6 animate-in fade-in zoom-in duration-200">
        <div className="flex items-center justify-between border-b border-[#c5a059]/30 pb-4">
          <div className="flex items-center gap-2">
            <Zap className="w-5 h-5 text-[#d4af37]" />
            <h3 className="text-lg font-serif font-bold text-[#e6c656] gold-glow">
              Dispatch & Claim Console
            </h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5 font-serif text-sm">
          {/* Select Commission */}
          <div className="space-y-1.5">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
              Select Available Commission:
            </label>
            <select
              value={selectedCommissionId}
              onChange={(e) => {
                setSelectedCommissionId(e.target.value);
                setErrorMessage('');
              }}
              className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 focus:outline-none focus:border-[#d4af37]"
            >
              <option value="">-- Choose Commission --</option>
              {openCommissions.map(c => (
                <option key={c.id} value={c.id}>
                  {c.title} (Hazard Rank {c.hazard_rank}) - Reward: £{c.reward_gold}
                </option>
              ))}
            </select>
          </div>

          {/* Select Beyonder */}
          <div className="space-y-1.5">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
              Select Beyonder Agent:
            </label>
            <select
              value={selectedBeyonderId}
              onChange={(e) => {
                setSelectedBeyonderId(e.target.value);
                setErrorMessage('');
              }}
              className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 focus:outline-none focus:border-[#d4af37]"
            >
              <option value="">-- Choose Operative --</option>
              {beyonders.map(b => (
                <option key={b.id} value={b.id}>
                  {b.codename} (Seq {b.sequence_level}{b.sequence_name ? ` - ${b.sequence_name}` : ''} • {b.affiliation}) • Sanity: {b.sanity_percentage}%
                </option>
              ))}
            </select>
          </div>

          {/* Live Validation Banner */}
          {currentCommission && currentBeyonder && (
            <div className={`p-4 rounded-lg border space-y-2 ${
              isEligible
                ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-200'
                : 'bg-red-950/50 border-red-500/60 text-red-200'
            }`}>
              <div className="flex items-center gap-2 font-bold text-xs">
                {isEligible ? (
                  <>
                    <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>ELIGIBLE OPERATIVE DISPATCH</span>
                  </>
                ) : (
                  <>
                    <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
                    <span>INELIGIBLE OPERATIVE DISPATCH</span>
                  </>
                )}
              </div>
              <p className="text-xs opacity-90">
                Operative <span className="font-semibold">{currentBeyonder.codename}</span> ({currentBeyonder.sequence_name ? `${currentBeyonder.sequence_name} (Seq ${currentBeyonder.sequence_level})` : `Sequence Level ${currentBeyonder.sequence_level}`} • {currentBeyonder.affiliation}) 
                vs Commission Hazard Rank {currentCommission.hazard_rank}.
              </p>
              {!isEligible && (
                <p className="text-xs font-bold text-red-300 pt-1 border-t border-red-800/40">
                  ⚠️ Sequence rank insufficient for commission hazard level
                </p>
              )}
            </div>
          )}

          {/* Error Message */}
          {errorMessage && (
            <div className="p-3 rounded bg-red-950/80 border border-red-500 text-red-200 text-xs font-bold flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Buttons */}
          <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || isEligible === false}
              className={`px-5 py-2 rounded text-xs font-semibold transition ${
                isEligible === false
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                  : 'bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/80 text-[#e6c656] shadow-md shadow-amber-950/50'
              }`}
            >
              {loading ? 'Dispatching...' : 'Confirm Mission Dispatch'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
