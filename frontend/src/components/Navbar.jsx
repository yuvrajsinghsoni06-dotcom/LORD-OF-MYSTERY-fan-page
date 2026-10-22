import React from 'react';
import { Shield, BookOpen, Scroll, Activity, AlertTriangle, Eye, Users } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, squadCount = 0 }) {
  const tabs = [
    { id: 'dashboard', label: 'Command Center', icon: Eye },
    { id: 'beyonders', label: 'Beyonder Directory', icon: Shield },
    { id: 'squads', label: 'Squad Formation', icon: Users, badge: squadCount },
    { id: 'potions', label: 'Potion Codex', icon: BookOpen },
    { id: 'commissions', label: 'Commission Board', icon: Scroll },
    { id: 'claims', label: 'Dispatch & Debriefs', icon: Activity },
  ];

  return (
    <header className="sticky top-0 z-40 bg-[#0c0e14]/90 border-b border-[#c5a059]/30 backdrop-blur-md px-6 py-4 shadow-2xl">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Logo & Title */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
          <div className="w-10 h-10 rounded-full bg-[#1e1b2e] border-2 border-[#d4af37] flex items-center justify-center shadow-lg shadow-purple-900/30">
            <span className="text-[#d4af37] text-xl font-serif">🎴</span>
          </div>
          <div>
            <h1 className="text-xl font-serif font-bold text-[#e6c656] tracking-wider gothic-heading gold-glow">
              TAROT CLUB COMMAND CENTER
            </h1>
            <p className="text-xs text-slate-400 font-serif tracking-widest uppercase">
              Lord of the Mysteries • Administrative Registry
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex flex-wrap items-center gap-1 bg-[#12141c]/80 p-1.5 rounded-lg border border-[#c5a059]/20">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-md font-serif text-sm transition-all duration-200 ${
                  isActive
                    ? 'bg-[#252038] text-[#e6c656] border border-[#d4af37]/60 shadow-md shadow-amber-950/40 font-semibold'
                    : 'text-slate-300 hover:text-[#d4af37] hover:bg-[#191c28]'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-[#d4af37]' : 'text-slate-400'}`} />
                <span>{tab.label}</span>
                {tab.badge !== undefined && tab.badge > 0 && (
                  <span className="ml-1 px-1.5 py-0.2 rounded-full text-[10px] bg-purple-950/80 border border-purple-500/50 text-purple-200 font-mono">
                    {tab.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
