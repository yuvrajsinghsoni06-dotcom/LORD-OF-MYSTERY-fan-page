import React, { useState } from 'react';
import { X, FileText, Activity, AlertTriangle, CheckCircle } from 'lucide-react';

export default function DebriefModal({
  isOpen,
  onClose,
  claim,
  onDebriefSubmit
}) {
  const [debriefNotes, setDebriefNotes] = useState(claim?.debrief_notes || '');
  const [sanityChange, setSanityChange] = useState(-5.0);
  const [status, setStatus] = useState('COMPLETED');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  if (!isOpen || !claim) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!debriefNotes.trim()) {
      setErrorMessage('Debrief notes are required to document the mission outcome.');
      return;
    }

    setLoading(true);
    setErrorMessage('');
    try {
      await onDebriefSubmit(claim.id, {
        debrief_notes: debriefNotes,
        sanity_change: Number(sanityChange),
        status: status
      });
      onClose();
    } catch (err) {
      setErrorMessage(err.response?.data?.detail || err.message || 'Failed to submit debrief.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="gothic-card gothic-card-gold w-full max-w-lg p-6 rounded-lg space-y-6">
        <div className="flex items-center justify-between border-b border-[#c5a059]/30 pb-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-[#d4af37]" />
            <h3 className="text-lg font-serif font-bold text-[#e6c656] gold-glow">
              Post-Mission Debrief & Sanity Logging
            </h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 font-serif text-sm">
          {/* Mission Info Summary */}
          <div className="p-3 rounded bg-[#0d0e12] border border-[#272a38] text-xs space-y-1">
            <p className="text-slate-300">
              <span className="text-slate-400">Commission Title:</span>{' '}
              <span className="font-bold text-[#e6c656]">{claim.commission_title || `Claim #${claim.id}`}</span>
            </p>
            <p className="text-slate-300">
              <span className="text-slate-400">Dispatched Operative:</span>{' '}
              <span className="font-bold text-purple-300">{claim.beyonder_codename || `Beyonder #${claim.beyonder_id}`}</span>
            </p>
          </div>

          {/* Outcome Status */}
          <div className="space-y-1.5">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
              Mission Outcome Status:
            </label>
            <div className="flex gap-4">
              <label className="flex items-center gap-2 text-slate-200 cursor-pointer text-xs">
                <input
                  type="radio"
                  name="status"
                  value="COMPLETED"
                  checked={status === 'COMPLETED'}
                  onChange={() => setStatus('COMPLETED')}
                  className="accent-[#d4af37]"
                />
                <span className="text-emerald-400 font-bold">COMPLETED (Success)</span>
              </label>
              <label className="flex items-center gap-2 text-slate-200 cursor-pointer text-xs">
                <input
                  type="radio"
                  name="status"
                  value="FAILED"
                  checked={status === 'FAILED'}
                  onChange={() => setStatus('FAILED')}
                  className="accent-[#d4af37]"
                />
                <span className="text-red-400 font-bold">FAILED (Aborted)</span>
              </label>
            </div>
          </div>

          {/* Debrief Notes */}
          <div className="space-y-1.5">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
              Debrief Field Notes:
            </label>
            <textarea
              rows="4"
              value={debriefNotes}
              onChange={(e) => setDebriefNotes(e.target.value)}
              placeholder="Record details of supernatural encounter, corrupted whispers, and relic containment status..."
              className="w-full p-3 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
            ></textarea>
          </div>

          {/* Sanity Adjustment */}
          <div className="space-y-1.5">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider flex items-center justify-between">
              <span>Sanity Percentage Impact (%):</span>
              <span className={sanityChange < 0 ? 'text-red-400 font-bold' : 'text-emerald-400 font-bold'}>
                {sanityChange > 0 ? `+${sanityChange}%` : `${sanityChange}%`}
              </span>
            </label>
            <input
              type="range"
              min="-30"
              max="20"
              step="1"
              value={sanityChange}
              onChange={(e) => setSanityChange(Number(e.target.value))}
              className="w-full accent-[#d4af37] bg-slate-800"
            />
            <p className="text-[11px] text-slate-400 italic">
              Negative values indicate mental corruption or strain during high-hazard missions. Positive values reflect therapeutic restoration.
            </p>
          </div>

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
              disabled={loading}
              className="px-5 py-2 rounded bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/80 text-[#e6c656] text-xs font-semibold transition"
            >
              {loading ? 'Updating Log...' : 'Submit Debrief Log'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
