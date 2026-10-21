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
