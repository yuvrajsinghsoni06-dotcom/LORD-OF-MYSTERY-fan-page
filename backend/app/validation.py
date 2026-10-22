from fastapi import HTTPException, status


def validate_sequence_level_for_claim(beyonder_sequence_level: int, commission_hazard_rank: int):
    """
    Checks if beyonder.sequence_level <= commission.hazard_rank when claiming a mission.
    In the Lord of the Mysteries system:
      - Sequence level ranges from 0 (God/highest power) to 9 (Initiate/lowest power).
      - Numerically, beyonder.sequence_level <= commission.hazard_rank means the beyonder has a sufficiently high rank (lower numerical sequence) to handle the hazard rank.
      - If sequence_level > hazard_rank (e.g., a Seq 8 trying to take a Hazard 3 mission), the operative is under-ranked for that hazard level.
    """
    if beyonder_sequence_level > commission_hazard_rank:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sequence rank insufficient for commission hazard level"
        )


def validate_squad_formation_members(member_ids: list[int]):
    """
    Validates that a squad formation strictly consists of 3 to 4 members only,
    with no duplicate members.
    """
    if not member_ids or len(member_ids) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Squad formation strictly requires a minimum of 3 operatives."
        )
    if len(member_ids) > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Squad formation is strictly limited to 3-4 members only."
        )
    if len(set(member_ids)) != len(member_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate operatives detected in squad formation."
        )


def calculate_squad_synergies(pathway_names: list[str]) -> list[str]:
    """
    Calculates canonical pathway combination synergies for Lord of the Mysteries squads.
    """
    synergies = []
    p_set = set((p.lower() if p else '') for p in pathway_names)

    # Lord of the Mysteries domain
    if "fool" in p_set and "door" in p_set:
        synergies.append("Celestial Spatial Marionette: Long-range puppet deployment through spatial gates")
    if "fool" in p_set and ("error" in p_set or "marauder" in p_set):
        synergies.append("Miracle Heist: Distorted historical void stealing & deceptive substitution")

    # God Almighty domain
    if "visionary" in p_set and "sun" in p_set:
        synergies.append("Solar Mind Sanctuary: Complete mental immunity to corruption and madness whispers")
    if "tyrant" in p_set and "sun" in p_set:
        synergies.append("Purifying Thunder Tempest: Blinding solar lightning smites with amplified exorcism power")
    if "visionary" in p_set and "tyrant" in p_set:
        synergies.append("Psychological Storm: Acoustic mental shockwaves disorienting enemy cognition")

    # Eternal Darkness domain
    if "darkness" in p_set and "death" in p_set:
        synergies.append("Silent Underworld: Concealed spectral necromancy and untraceable strikes")
    if "twilight giant" in p_set and "darkness" in p_set:
        synergies.append("Twilight Slumber Bastion: Impenetrable defensive dawn barrier with slumber pacification")

    # Calamity of Destruction domain
    if "red priest" in p_set and "demoness" in p_set:
        synergies.append("Yin-Yang Cataclysm: Blazing incendiary flame interwoven with freezing plague frost")

    # Demon of Knowledge domain
    if "paragon" in p_set and "hermit" in p_set:
        synergies.append("Arcane Automaton Array: Mechanized golems infused with ancient reality formulas")

    # Life & Origin domain
    if "moon" in p_set and "mother" in p_set:
        synergies.append("Primordial Bloom: High-speed biological regeneration and chimeric enhancement")

    # Order & Anarchy domain
    if "black emperor" in p_set and "justiciar" in p_set:
        synergies.append("Absolute Imperial Decree: Binding legal jurisdiction prohibiting enemy supernatural escape")

    # Default synergy
    if not synergies:
        synergies.append("Tactical Cohesion: Synchronized Victorian combat formation")

    return synergies
