import os
import re

AVATAR_DIR = os.path.join(os.path.dirname(__file__), "frontend", "public", "avatars")
os.makedirs(AVATAR_DIR, exist_ok=True)

# Pathway color schemes and occult iconography
PATHWAY_THEMES = {
    "Fool": {
        "bg_start": "#1b112c", "bg_end": "#0a0714",
        "accent": "#c084fc", "border": "#d4af37",
        "icon": "🎴", "symbol": "M50,25 C30,25 20,45 20,70 C20,95 40,110 50,110 C60,110 80,95 80,70 C80,45 70,25 50,25 Z",
        "feature": "tophat"
    },
    "Door": {
        "bg_start": "#0d1b2a", "bg_end": "#040810",
        "accent": "#60a5fa", "border": "#93c5fd",
        "icon": "🚪", "symbol": "M30,30 L70,30 L70,100 L30,100 Z",
        "feature": "door"
    },
    "Error": {
        "bg_start": "#1f1712", "bg_end": "#0d0906",
        "accent": "#f59e0b", "border": "#d97706",
        "icon": "⏳", "symbol": "M50,30 L65,55 L35,55 Z M50,90 L65,65 L35,65 Z",
        "feature": "monocle"
    },
    "Visionary": {
        "bg_start": "#191c2b", "bg_end": "#0c0d16",
        "accent": "#38bdf8", "border": "#7dd3fc",
        "icon": "👁️", "symbol": "M20,60 Q50,20 80,60 Q50,100 20,60 Z",
        "feature": "eye"
    },
    "Hanged Man": {
        "bg_start": "#261014", "bg_end": "#0e0406",
        "accent": "#ef4444", "border": "#991b1b",
        "icon": "🩸", "symbol": "M50,20 L50,85 M35,40 L65,40 M40,60 L60,60",
        "feature": "cross"
    },
    "Tyrant": {
        "bg_start": "#0c1d2e", "bg_end": "#030b14",
        "accent": "#38bdf8", "border": "#0284c7",
        "icon": "⚡", "symbol": "M55,20 L30,60 L50,60 L45,95 L70,50 L50,50 Z",
        "feature": "lightning"
    },
    "Sun": {
        "bg_start": "#2a1c06", "bg_end": "#0f0902",
        "accent": "#fbbf24", "border": "#f59e0b",
        "icon": "☀️", "symbol": "M50,30 A20,20 0 1,0 50,70 A20,20 0 1,0 50,30 Z",
        "feature": "sun"
    },
    "Darkness": {
        "bg_start": "#13131e", "bg_end": "#06060c",
        "accent": "#e11d48", "border": "#9f1239",
        "icon": "🌙", "symbol": "M60,25 C45,25 35,40 35,60 C35,80 45,95 60,95 C45,90 40,75 40,60 C40,45 45,30 60,25 Z",
        "feature": "moon"
    },
    "Death": {
        "bg_start": "#111817", "bg_end": "#050a09",
        "accent": "#2dd4bf", "border": "#0f766e",
        "icon": "💀", "symbol": "M35,35 C35,25 65,25 65,35 C65,55 60,65 50,65 C40,65 35,55 35,35 Z",
        "feature": "skull"
    },
    "Twilight Giant": {
        "bg_start": "#28170c", "bg_end": "#0d0603",
        "accent": "#fb923c", "border": "#ea580c",
        "icon": "🗡️", "symbol": "M50,15 L55,25 L55,75 L50,85 L45,75 L45,25 Z",
        "feature": "sword"
    },
    "Red Priest": {
        "bg_start": "#2c100d", "bg_end": "#100403",
        "accent": "#f97316", "border": "#c2410c",
        "icon": "🔥", "symbol": "M50,20 Q65,45 55,65 Q65,65 60,85 Q45,95 35,75 Q35,55 50,20 Z",
        "feature": "flame"
    },
    "Demoness": {
        "bg_start": "#1e0f24", "bg_end": "#0c0410",
        "accent": "#c084fc", "border": "#a855f7",
        "icon": "🕸️", "symbol": "M30,30 L70,70 M70,30 L30,70 M50,20 L50,80 M20,50 L80,50",
        "feature": "mirror"
    },
    "Paragon": {
        "bg_start": "#1c1917", "bg_end": "#0c0a09",
        "accent": "#fbbf24", "border": "#ca8a04",
        "icon": "⚙️", "symbol": "M50,30 A20,20 0 1,0 50,70 A20,20 0 1,0 50,30 Z",
        "feature": "gear"
    },
    "Hermit": {
        "bg_start": "#1a162b", "bg_end": "#080612",
        "accent": "#a78bfa", "border": "#7c3aed",
        "icon": "📜", "symbol": "M30,25 L70,25 L70,85 L30,85 Z",
        "feature": "scroll"
    },
    "Wheel of Fortune": {
        "bg_start": "#1c2018", "bg_end": "#080b06",
        "accent": "#a3e635", "border": "#65a30d",
        "icon": "🎲", "symbol": "M50,20 A30,30 0 1,0 50,80 A30,30 0 1,0 50,20 Z",
        "feature": "ouroboros"
    },
    "Moon": {
        "bg_start": "#230e16", "bg_end": "#0c0407",
        "accent": "#fb7185", "border": "#e11d48",
        "icon": "🩸", "symbol": "M60,30 C45,30 35,45 35,65 C35,85 45,95 60,95 C48,90 44,75 44,65 C44,45 48,35 60,30 Z",
        "feature": "vampire"
    },
    "Mother": {
        "bg_start": "#122014", "bg_end": "#050d06",
        "accent": "#4ade80", "border": "#16a34a",
        "icon": "🌱", "symbol": "M50,80 Q50,40 30,35 Q50,45 50,80 Q50,45 70,35 Q50,40 50,80 Z",
        "feature": "plant"
    },
    "Black Emperor": {
        "bg_start": "#181412", "bg_end": "#080605",
        "accent": "#eab308", "border": "#ca8a04",
        "icon": "👑", "symbol": "M25,65 L35,35 L50,55 L65,35 L75,65 Z",
        "feature": "crown"
    },
    "Justiciar": {
        "bg_start": "#161b24", "bg_end": "#070a0f",
        "accent": "#94a3b8", "border": "#64748b",
        "icon": "⚖️", "symbol": "M50,20 L50,80 M25,40 L75,40 M25,40 L15,65 L35,65 Z M75,40 L65,65 L85,65 Z",
        "feature": "scales"
    },
    "Chained": {
        "bg_start": "#1c1416", "bg_end": "#090506",
        "accent": "#f43f5e", "border": "#be123c",
        "icon": "⛓️", "symbol": "M30,35 L70,35 L70,45 L30,45 Z M30,55 L70,55 L70,65 L30,65 Z",
        "feature": "chains"
    },
    "Abyss": {
        "bg_start": "#240a0a", "bg_end": "#0e0202",
        "accent": "#ef4444", "border": "#b91c1c",
        "icon": "😈", "symbol": "M30,25 L40,45 L60,45 L70,25 L65,65 L35,65 Z",
        "feature": "horns"
    },
    "White Tower": {
        "bg_start": "#1b1f28", "bg_end": "#080a0f",
        "accent": "#cbd5e1", "border": "#94a3b8",
        "icon": "🏰", "symbol": "M35,25 L65,25 L60,85 L40,85 Z",
        "feature": "tower"
    }
}


def sanitize_filename(name: str) -> str:
    slug = re.sub(r'[^a-zA-Z0-9]', '_', name.lower()).strip('_')
    slug = re.sub(r'_+', '_', slug)
    return slug


def create_avatar_svg(name: str, pathway: str, seq_level: int, seq_name: str, affiliation: str) -> str:
    theme = PATHWAY_THEMES.get(pathway, PATHWAY_THEMES["Fool"])
    initials = "".join([part[0] for part in name.split() if part and part[0].isalpha()])[:2].upper()
    if not initials:
        initials = "BY"

    bg_start = theme["bg_start"]
    bg_end = theme["bg_end"]
    accent = theme["accent"]
    border_color = theme["border"]
    icon = theme["icon"]
    feature = theme["feature"]

    # Rank tier styling
    if seq_level <= 0:
        tier_title = "TRUE DEITY"
        ring_color = "#ffd700"
        ring_glow = "rgba(255, 215, 0, 0.6)"
    elif seq_level <= 2:
        tier_title = "ANGEL"
        ring_color = "#e6c656"
        ring_glow = "rgba(230, 198, 86, 0.4)"
    elif seq_level <= 4:
        tier_title = "SAINT / HIGH"
        ring_color = "#d4af37"
        ring_glow = "rgba(212, 175, 55, 0.3)"
    elif seq_level <= 7:
        tier_title = "MID SEQUENCE"
        ring_color = "#a855f7"
        ring_glow = "rgba(168, 85, 247, 0.2)"
    else:
        tier_title = "LOW SEQUENCE"
        ring_color = "#64748b"
        ring_glow = "rgba(100, 116, 139, 0.15)"

    short_name = name.split("(")[0].strip()
    if len(short_name) > 18:
        short_name = short_name[:17] + "…"

    seq_disp = f"Seq {seq_level}"
    if seq_name:
        seq_sub = seq_name[:15]
    else:
        seq_sub = pathway

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 240" width="200" height="240">
  <defs>
    <radialGradient id="bg_grad" cx="50%" cy="40%" r="65%">
      <stop offset="0%" stop-color="{bg_start}" />
      <stop offset="100%" stop-color="{bg_end}" />
    </radialGradient>
    <linearGradient id="gold_grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{ring_color}" />
      <stop offset="50%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="{ring_color}" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Tarot Card Outer Body -->
  <rect x="4" y="4" width="192" height="232" rx="10" fill="url(#bg_grad)" stroke="{ring_color}" stroke-width="2.5" />
  <rect x="8" y="8" width="184" height="224" rx="7" fill="none" stroke="{border_color}" stroke-width="0.8" stroke-dasharray="4,2" opacity="0.6" />

  <!-- Top Tarot Header -->
  <rect x="15" y="14" width="170" height="20" rx="3" fill="#07090e" stroke="{ring_color}" stroke-width="0.8" opacity="0.8" />
  <text x="100" y="28" fill="{ring_color}" font-family="Georgia, serif" font-size="9" font-weight="bold" text-anchor="middle" letter-spacing="1.5">
    {tier_title} • {pathway.upper()}
  </text>

  <!-- Central Mystical Halo & Portrait Circle -->
  <circle cx="100" cy="85" r="48" fill="#080a10" stroke="{ring_color}" stroke-width="2" filter="url(#glow)" />
  <circle cx="100" cy="85" r="44" fill="none" stroke="{accent}" stroke-width="1" stroke-dasharray="6,3" opacity="0.8" />

  <!-- Victorian Silhouette Bust / Symbol -->
  <g transform="translate(60, 45) scale(0.8)">
    <!-- Shoulders & Coat -->
    <path d="M10,85 C15,65 30,55 50,55 C70,55 85,65 90,85 Z" fill="#141824" stroke="{accent}" stroke-width="1.2" />
    <path d="M50,55 L40,85 M50,55 L60,85" stroke="{ring_color}" stroke-width="0.8" opacity="0.5" />
    
    <!-- Head / Mask / Sigil -->
    <circle cx="50" cy="38" r="16" fill="#1e2235" stroke="{accent}" stroke-width="1.5" />

    <!-- Occult Feature (Top Hat / Eye / Monocle / Horns / Hood) -->
    <!-- Feature-specific emblem inside head -->
    <circle cx="50" cy="38" r="12" fill="{bg_start}" />
  </g>

  <!-- Large Center Tarot Icon -->
  <text x="100" y="93" font-size="28" text-anchor="middle" filter="url(#glow)">{icon}</text>

  <!-- Sequence Level Emblem Pill -->
  <rect x="65" y="125" width="70" height="18" rx="9" fill="#06080e" stroke="{ring_color}" stroke-width="1.2" />
  <text x="100" y="137" fill="{ring_color}" font-family="Georgia, serif" font-size="10" font-weight="bold" text-anchor="middle">
    {seq_disp}
  </text>

  <!-- Member Name Banner -->
  <rect x="12" y="152" width="176" height="42" rx="4" fill="#080a12" stroke="{border_color}" stroke-width="1" opacity="0.9" />
  <text x="100" y="169" fill="#f8fafc" font-family="Georgia, serif" font-size="11" font-weight="bold" text-anchor="middle">
    {short_name}
  </text>
  <text x="100" y="184" fill="{accent}" font-family="Georgia, serif" font-size="9.5" text-anchor="middle" font-style="italic">
    {seq_sub}
  </text>

  <!-- Bottom Affiliation Footer -->
  <rect x="12" y="198" width="176" height="22" rx="3" fill="#06070a" stroke="{ring_color}" stroke-width="0.8" opacity="0.7" />
  <text x="100" y="213" fill="#94a3b8" font-family="Georgia, serif" font-size="8.5" text-anchor="middle">
    {affiliation[:26]}
  </text>
</svg>"""
    return svg


# Extract characters from seed.py or database directly
if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
    from app.database import SessionLocal
    from app.models import Beyonder

    db = SessionLocal()
    beyonders = db.query(Beyonder).all()
    print(f"Generating stylized Victorian-Gothic tarot portraits for {len(beyonders)} characters...")

    count = 0
    for b in beyonders:
        slug = sanitize_filename(b.codename)
        p_name = b.pathway.name if b.pathway else "Fool"
        svg_content = create_avatar_svg(
            name=b.codename,
            pathway=p_name,
            seq_level=b.sequence_level,
            seq_name=b.sequence_name or p_name,
            affiliation=b.affiliation
        )
        file_path = os.path.join(AVATAR_DIR, f"{slug}.svg")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        
        # Update database with relative path
        b.avatar_url = f"/avatars/{slug}.svg"
        count += 1

    db.commit()
    db.close()
    print(f"Successfully generated {count} portraits in {AVATAR_DIR} and updated Beyonders avatar_url!")
