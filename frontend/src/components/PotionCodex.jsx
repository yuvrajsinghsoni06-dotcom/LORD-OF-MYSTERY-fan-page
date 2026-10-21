import React, { useState } from 'react';
import { BookOpen, Search, Sparkles, Scroll, ShieldAlert, Award, Compass } from 'lucide-react';

export default function PotionCodex({ potions, pathways }) {
  const [selectedPathwayId, setSelectedPathwayId] = useState(pathways[0]?.id || 1);
  const [searchQuery, setSearchQuery] = useState('');
  const [pathwayFilter, setPathwayFilter] = useState('');

  const currentPathway = pathways.find(p => p.id === Number(selectedPathwayId)) || pathways[0];

  const filteredPathways = pathways.filter(p => {
    return p.name.toLowerCase().includes(pathwayFilter.toLowerCase()) ||
           p.sequence_0_title.toLowerCase().includes(pathwayFilter.toLowerCase());
  });

  const pathwayPotions = potions.filter(p => {
    const matchesPathway = p.pathway_id === Number(selectedPathwayId);
    const matchesSearch = searchQuery === '' || 
                          p.abilities.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          p.main_ingredients.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          p.supplementary_ingredients.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesPathway && matchesSearch;
  }).sort((a, b) => b.sequence_level - a.sequence_level); // Seq 9 -> Seq 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="gothic-card p-6 rounded-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-serif font-bold text-[#e6c656] flex items-center gap-2 gold-glow">
            <BookOpen className="w-6 h-6 text-[#d4af37]" /> The Sacred 22 Potion Pathways Codex
          </h2>
          <p className="text-xs text-slate-400 font-serif mt-1">
            Ancient blasphemy slate recipes, Sequence 9 to Sequence 0 formulas, main/supplementary ingredients, and divine abilities across all 22 pathways.
          </p>
        </div>
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search ingredients, abilities..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 text-sm font-serif focus:outline-none focus:border-[#d4af37]"
          />
        </div>
      </div>

      {/* Pathway Selector Grid (All 22 Pathways) */}
      <div className="gothic-card p-4 rounded-lg space-y-3">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 border-b border-slate-800 pb-2">
          <span className="text-xs font-serif font-bold text-[#d4af37] uppercase tracking-wider flex items-center gap-1.5">
            <Compass className="w-4 h-4" /> Select Pathway to the Divine ({pathways.length}/22 Available):
          </span>
          <div className="relative w-full sm:w-56">
            <input
              type="text"
              placeholder="Filter 22 pathways..."
              value={pathwayFilter}
              onChange={(e) => setPathwayFilter(e.target.value)}
              className="w-full px-2.5 py-1 text-xs rounded bg-[#0d0e12] border border-[#272a38] text-slate-200 focus:outline-none focus:border-[#d4af37]"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 max-h-56 overflow-y-auto pr-1">
          {filteredPathways.map(p => {
            const isSelected = p.id === Number(selectedPathwayId);
            return (
              <button
                key={p.id}
                onClick={() => setSelectedPathwayId(p.id)}
                className={`p-2 rounded text-left font-serif transition border text-xs cursor-pointer ${
                  isSelected
                    ? 'bg-[#252038] text-[#e6c656] border-[#d4af37] font-bold shadow-md shadow-amber-950/40'
                    : 'bg-[#0d0e12] text-slate-400 border-[#272a38] hover:text-slate-200 hover:bg-[#141620]'
                }`}
              >
                <div className="truncate font-semibold">{p.name}</div>
                <div className="text-[10px] text-purple-300 truncate opacity-80">{p.sequence_0_title}</div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Pathway Overview Card */}
      {currentPathway && (
        <div className="gothic-card gothic-card-gold p-6 rounded-lg space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-[#c5a059]/30 pb-4 gap-3">
            <div>
              <span className="text-xs uppercase font-serif tracking-widest text-[#d4af37]">
                DIVINE PATHWAY ARCHIVE
              </span>
              <h3 className="text-2xl font-serif font-bold text-[#e6c656] gold-glow">
                The {currentPathway.name} Pathway
              </h3>
            </div>
            <div className="sm:text-right">
              <span className="text-xs text-slate-400 font-serif block uppercase tracking-wider">Apex Sequence 0 Deity</span>
              <span className="text-lg font-serif font-bold text-purple-300">
                {currentPathway.sequence_0_title}
              </span>
            </div>
          </div>

          {/* Sequence Progression Ladder */}
          <div className="space-y-4">
            <h4 className="text-sm font-serif font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#d4af37]" /> Documented Sequence Recipes & Supernatural Bestowals
            </h4>

            {pathwayPotions.length > 0 ? (
              <div className="grid grid-cols-1 gap-4">
                {pathwayPotions.map(potion => (
                  <div
                    key={potion.id}
                    className="p-5 rounded-lg bg-[#0d0e12]/90 border border-[#272a38] hover:border-[#d4af37]/40 transition space-y-3 shadow-lg"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className={`px-3 py-1 rounded text-xs font-bold font-serif ${
                          potion.sequence_level <= 3
                            ? 'bg-purple-950/80 border border-purple-500/60 text-purple-200'
                            : 'bg-[#252038] border border-[#a855f7]/50 text-purple-300'
                        }`}>
                          Sequence {potion.sequence_level}
                        </span>
                        <h5 className="text-base font-serif font-bold text-[#e6c656]">
                          Sequence {potion.sequence_level} Potion Concoction
                        </h5>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-serif pt-2 border-t border-slate-800/60">
                      <div>
                        <span className="text-[#d4af37] font-semibold block mb-1">Main Extraordinary Ingredients:</span>
                        <p className="text-slate-300 bg-[#141620] p-2.5 rounded border border-slate-800">
                          {potion.main_ingredients}
                        </p>
                      </div>
                      <div>
                        <span className="text-amber-400 font-semibold block mb-1">Supplementary Alchemy Ingredients:</span>
                        <p className="text-slate-300 bg-[#141620] p-2.5 rounded border border-slate-800">
                          {potion.supplementary_ingredients}
                        </p>
                      </div>
                    </div>

                    <div className="text-xs font-serif pt-2">
                      <span className="text-purple-300 font-semibold block mb-1">Bestowed Supernatural Abilities:</span>
                      <p className="text-slate-200 bg-[#1a1729] p-2.5 rounded border border-purple-900/40 italic">
                        "{potion.abilities}"
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-10 text-slate-500 italic font-serif">
                No potion recipes currently documented for the {currentPathway.name} pathway matching criteria.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
