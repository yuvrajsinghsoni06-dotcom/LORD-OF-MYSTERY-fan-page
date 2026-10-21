import React, { useState, useEffect } from 'react';
import { X, Shield, Plus, Edit2, Sparkles } from 'lucide-react';

export default function BeyonderFormModal({
  isOpen,
  onClose,
  pathways,
  editingBeyonder,
  onSubmit
}) {
  const [codename, setCodename] = useState('');
  const [pathwayId, setPathwayId] = useState('');
  const [sequenceLevel, setSequenceLevel] = useState(9);
  const [sequenceName, setSequenceName] = useState('');
  const [sanityPercentage, setSanityPercentage] = useState(100.0);
  const [affiliation, setAffiliation] = useState('Tarot Club');
  const [characteristics, setCharacteristics] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (editingBeyonder) {
      setCodename(editingBeyonder.codename);
      setPathwayId(editingBeyonder.pathway_id);
      setSequenceLevel(editingBeyonder.sequence_level);
      setSequenceName(editingBeyonder.sequence_name || '');
      setSanityPercentage(editingBeyonder.sanity_percentage);
      setAffiliation(editingBeyonder.affiliation);
      setCharacteristics(editingBeyonder.characteristics || '');
    } else {
      setCodename('');
      setPathwayId(pathways[0]?.id || '');
      setSequenceLevel(9);
      setSequenceName('');
      setSanityPercentage(100.0);
      setAffiliation('Tarot Club');
      setCharacteristics('');
    }
  }, [editingBeyonder, pathways, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!codename.trim() || !pathwayId) {
      setError('Please specify both a codename and a pathway.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      await onSubmit({
        codename,
        pathway_id: Number(pathwayId),
        sequence_level: Number(sequenceLevel),
        sequence_name: sequenceName.trim() || undefined,
        sanity_percentage: Number(sanityPercentage),
        affiliation,
        characteristics: characteristics.trim() || undefined
      });
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="gothic-card gothic-card-gold w-full max-w-lg p-6 rounded-lg space-y-5 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between border-b border-[#c5a059]/30 pb-4">
          <div className="flex items-center gap-2">
            <Shield className="w-5 h-5 text-[#d4af37]" />
            <h3 className="text-lg font-serif font-bold text-[#e6c656] gold-glow">
              {editingBeyonder ? 'Edit Beyonder Operative' : 'Induct New Beyonder Agent'}
            </h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 font-serif text-sm">
          <div className="space-y-1">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
              Agent Codename / True Name:
            </label>
            <input
              type="text"
              required
              value={codename}
              onChange={(e) => setCodename(e.target.value)}
              placeholder="e.g., The Magician, Dunn Smith, Leodero, Cattleya"
              className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                Divine Pathway:
              </label>
              <select
                value={pathwayId}
                onChange={(e) => setPathwayId(e.target.value)}
                className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
              >
                {pathways.map(p => (
                  <option key={p.id} value={p.id}>{p.name} (Seq 0: {p.sequence_0_title})</option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                Sequence Rank (0 - 9):
              </label>
              <select
                value={sequenceLevel}
                onChange={(e) => setSequenceLevel(e.target.value)}
                className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
              >
                {[0,1,2,3,4,5,6,7,8,9].map(seq => (
                  <option key={seq} value={seq}>Sequence {seq}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                Sequence Title / Name:
              </label>
              <input
                type="text"
                value={sequenceName}
                onChange={(e) => setSequenceName(e.target.value)}
                placeholder="e.g., Bizarro Sorcerer, Demon Hunter"
                className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
              />
            </div>

            <div className="space-y-1">
              <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
                Sanity Percentage (%):
              </label>
              <input
                type="number"
                min="0"
                max="100"
                step="0.5"
                value={sanityPercentage}
                onChange={(e) => setSanityPercentage(e.target.value)}
                className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider">
              Affiliation / Organization:
            </label>
            <input
              type="text"
              required
              value={affiliation}
              onChange={(e) => setAffiliation(e.target.value)}
              placeholder="e.g., Church of Evernight Goddess, Pirates (Five Seas), Tarot Club"
              className="w-full p-2.5 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-xs focus:outline-none focus:border-[#d4af37]"
            />
          </div>

          <div className="space-y-1">
            <label className="block text-slate-300 font-semibold text-xs uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-[#d4af37]" /> Characteristics, Abilities & Sealed Artifacts:
            </label>
            <textarea
              rows="3"
              value={characteristics}
              onChange={(e) => setCharacteristics(e.target.value)}
              placeholder="Record supernatural traits, spirit body thread range, sealed artifacts wielded, mythical creature traits..."
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
              className="px-4 py-2 rounded bg-slate-800 text-slate-300 text-xs font-semibold cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2 rounded bg-[#382613] hover:bg-[#4d3419] border border-[#d4af37]/80 text-[#e6c656] text-xs font-semibold cursor-pointer shadow"
            >
              {loading ? 'Saving...' : editingBeyonder ? 'Save Changes' : 'Induct Agent'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
