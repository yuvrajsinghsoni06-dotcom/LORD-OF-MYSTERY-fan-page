import React, { useState } from 'react';
import { X, Scroll, Plus } from 'lucide-react';

export default function CommissionFormModal({
  isOpen,
  onClose,
  onSubmit
}) {
  const [title, setTitle] = useState('');
  const [hazardRank, setHazardRank] = useState(5);
  const [target, setTarget] = useState('');
  const [location, setLocation] = useState('');
  const [rewardGold, setRewardGold] = useState(100.0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !target.trim() || !location.trim()) {
      setError('Title, Target, and Location are required.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      await onSubmit({
        title,
        hazard_rank: Number(hazardRank),
        target,
        location,
        reward_gold: Number(rewardGold)
      });
      setTitle('');
      setTarget('');
      setLocation('');
      setRewardGold(100.0);
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to issue commission');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="gothic-card gothic-card-gold w-full max-w-md p-6 rounded-lg space-y-5">
        <div className="flex items-center justify-between border-b border-[#c5a059]/30 pb-4">
          <div className="flex items-center gap-2">
            <Scroll className="w-5 h-5 text-[#d4af37]" />
            <h3 className="text-lg font-serif font-bold text-[#e6c656] gold-glow">
              Issue New Commission
            </h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 font-serif text-sm">
          <div className="space-y-1">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
              Commission Title:
            </label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g., Exorcise Wraith in Empress Borough"
              className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                Hazard Rank (0 - 9):
              </label>
              <select
                value={hazardRank}
                onChange={(e) => setHazardRank(e.target.value)}
                className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
              >
                {[0,1,2,3,4,5,6,7,8,9].map(h => (
                  <option key={h} value={h}>Hazard Rank {h}</option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                Reward Gold (£):
              </label>
              <input
                type="number"
                min="0"
                step="10"
                value={rewardGold}
                onChange={(e) => setRewardGold(e.target.value)}
                className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
              Target / Entity Threat:
            </label>
            <input
              type="text"
              required
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              placeholder="e.g., Ancient Spectre, Amon Avatar, Secret Order Cultist"
              className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
            />
          </div>

          <div className="space-y-1">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
              Location:
            </label>
            <input
              type="text"
              required
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g., Backlund Bridge District, Tingen City"
              className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
            />
          </div>

          {error && (
            <p className="text-xs font-bold text-red-400 bg-red-950/80 p-2.5 rounded border border-red-500">
              {error}
            </p>
          )}

          <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded bg-slate-800 text-slate-300 text-xs font-semibold"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2 rounded bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/80 text-[#e6c656] text-xs font-semibold"
            >
              {loading ? 'Posting...' : 'Issue Commission'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
