import pytest
from fastapi import HTTPException
from app.validation import validate_sequence_level_for_claim


def test_sequence_level_validation_pass():
    # Sequence 4 Beyonder trying to take Hazard Rank 5 mission (4 <= 5: Allowed)
    validate_sequence_level_for_claim(4, 5)

    # Sequence 0 God trying to take Hazard Rank 0 mission (0 <= 0: Allowed)
    validate_sequence_level_for_claim(0, 0)


def test_sequence_level_validation_fail():
    # Sequence 8 Novice trying to take Hazard Rank 3 mission (8 > 3: Rejected)
    with pytest.raises(HTTPException) as exc_info:
        validate_sequence_level_for_claim(8, 3)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Sequence rank insufficient for commission hazard level"
