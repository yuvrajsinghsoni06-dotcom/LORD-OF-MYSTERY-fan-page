import pytest
from fastapi import HTTPException
from app.validation import validate_squad_formation_members, calculate_squad_synergies


def test_squad_member_count_validation():
    # Valid: 3 members
    validate_squad_formation_members([1, 2, 3])

    # Valid: 4 members
    validate_squad_formation_members([1, 2, 3, 4])

    # Invalid: < 3 members (2 members)
    with pytest.raises(HTTPException) as exc_info:
        validate_squad_formation_members([1, 2])
    assert exc_info.value.status_code == 400
    assert "minimum of 3 operatives" in exc_info.value.detail

    # Invalid: > 4 members (5 members)
    with pytest.raises(HTTPException) as exc_info:
        validate_squad_formation_members([1, 2, 3, 4, 5])
    assert exc_info.value.status_code == 400
    assert "strictly limited to 3-4 members only" in exc_info.value.detail

    # Invalid: duplicate members
    with pytest.raises(HTTPException) as exc_info:
        validate_squad_formation_members([1, 2, 2])
    assert exc_info.value.status_code == 400
    assert "Duplicate operatives detected" in exc_info.value.detail


def test_squad_api_flow(client):
    # 1. Create a Pathway
    p_resp = client.post("/api/pathways/", json={"name": "TestDarkness", "sequence_0_title": "Darkness"})
    assert p_resp.status_code == 201
    pathway_id = p_resp.json()["id"]

    # 2. Create 5 Beyonders
    b_ids = []
    for i in range(5):
        b_resp = client.post("/api/beyonders/", json={
            "pathway_id": pathway_id,
            "codename": f"Nighthawk Operative {i+1}",
            "sequence_level": 7 - i,  # Seq 7, 6, 5, 4, 3
            "sanity_percentage": 85.0,
            "affiliation": "Church of Evernight Goddess"
        })
        assert b_resp.status_code == 201
        b_ids.append(b_resp.json()["id"])

    # 3. Attempt creating squad with 2 members (Should fail: < 3)
    inv_resp = client.post("/api/squads/", json={
        "name": "Under-manned Squad",
        "member_ids": [b_ids[0], b_ids[1]]
    })
    assert inv_resp.status_code in [400, 422]

    # 4. Attempt creating squad with 5 members (Should fail: > 4)
    inv_resp2 = client.post("/api/squads/", json={
        "name": "Over-manned Squad",
        "member_ids": b_ids[:5]
    })
    assert inv_resp2.status_code in [400, 422]

    # 5. Successfully create squad with 3 members
    squad3_resp = client.post("/api/squads/", json={
        "name": "Tingen Trio",
        "motto": "We are guardians.",
        "formation_type": "BALANCED",
        "member_ids": [b_ids[0], b_ids[1], b_ids[2]]
    })
    assert squad3_resp.status_code == 201
    assert squad3_resp.json()["member_count"] == 3

    # 6. Successfully create squad with 4 members
    squad4_resp = client.post("/api/squads/", json={
        "name": "Backlund Vanguard",
        "motto": "Night conceals.",
        "formation_type": "ASSAULT",
        "member_ids": [b_ids[0], b_ids[1], b_ids[2], b_ids[3]]
    })
    assert squad4_resp.status_code == 201
    assert squad4_resp.json()["member_count"] == 4
    squad_id = squad4_resp.json()["id"]

    # 7. Create a Commission (Hazard Rank 4)
    comm_resp = client.post("/api/commissions/", json={
        "title": "Purify Sewer Spirit",
        "hazard_rank": 4,
        "target": "Ancient Spirit",
        "location": "East Borough",
        "reward_gold": 200.0
    })
    assert comm_resp.status_code == 201
    comm_id = comm_resp.json()["id"]

    # 8. Dispatch squad on commission
    disp_resp = client.post(f"/api/squads/{squad_id}/dispatch", json={"commission_id": comm_id})
    assert disp_resp.status_code == 200
    assert disp_resp.json()["success"] is True

    # Check squad is now DEPLOYED
    sq_check = client.get(f"/api/squads/{squad_id}")
    assert sq_check.json()["status"] == "DEPLOYED"
