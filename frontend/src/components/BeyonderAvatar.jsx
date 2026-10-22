import React, { useState } from 'react';

export default function BeyonderAvatar({
  avatarUrl,
  name = 'Unknown',
  sequenceLevel = 9,
  pathway = 'Fool',
  size = 'md',
  showBadge = true,
  className = '',
  onClick
}) {
  const [hasError, setHasError] = useState(false);

  // Size styling classes
  const sizeClasses = {
    xs: 'w-8 h-8 text-[10px]',
    sm: 'w-10 h-10 text-xs',
    md: 'w-13 h-13 text-sm',
    lg: 'w-18 h-18 text-base',
    xl: 'w-24 h-28 text-lg'
  }[size] || 'w-13 h-13 text-sm';

  // Ring & border styling based on Sequence Level
  let ringColor = 'border-slate-600 shadow-slate-900/40';
  let badgeColor = 'bg-slate-800 text-slate-300 border-slate-600';

  if (sequenceLevel <= 0) {
    ringColor = 'border-[#ffd700] shadow-amber-500/30 shadow-lg';
    badgeColor = 'bg-[#ffd700] text-black font-extrabold border-amber-300';
  } else if (sequenceLevel <= 2) {
    ringColor = 'border-[#e6c656] shadow-amber-500/20 shadow-md';
    badgeColor = 'bg-[#e6c656] text-black font-bold border-amber-300';
  } else if (sequenceLevel <= 4) {
    ringColor = 'border-[#d4af37] shadow-amber-900/40 shadow-md';
    badgeColor = 'bg-[#382613] text-[#e6c656] border-[#d4af37]';
  } else if (sequenceLevel <= 7) {
    ringColor = 'border-[#a855f7] shadow-purple-950/40 shadow-sm';
    badgeColor = 'bg-[#252038] text-purple-300 border-purple-500';
  }

  const initials = name
    .split('(')[0]
    .trim()
    .split(' ')
    .filter(Boolean)
    .map(p => p[0])
    .slice(0, 2)
    .join('')
    .toUpperCase() || 'BY';

  return (
    <div
      onClick={onClick}
      className={`relative inline-block rounded-lg overflow-visible group ${onClick ? 'cursor-pointer' : ''} ${className}`}
      title={`${name} (Sequence ${sequenceLevel} • ${pathway})`}
    >
      <div
        className={`${sizeClasses} rounded-lg border-2 ${ringColor} bg-[#0a0d14] overflow-hidden flex items-center justify-center transition-transform duration-200 group-hover:scale-105`}
      >
        {avatarUrl && !hasError ? (
          <img
            src={avatarUrl}
            alt={name}
            onError={() => setHasError(true)}
            className="w-full h-full object-cover object-center"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-[#161224] to-[#090b10] p-1 text-center">
            <span className="font-serif font-bold text-[#e6c656] tracking-tighter">
              {initials}
            </span>
          </div>
        )}
      </div>

      {showBadge && (
        <span
          className={`absolute -bottom-1 -right-1.5 px-1 py-0.2 rounded text-[9px] font-mono leading-none border shadow-md ${badgeColor}`}
        >
          S{sequenceLevel}
        </span>
      )}
    </div>
  );
}
