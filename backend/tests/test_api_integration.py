import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
import app.database as db_module

# Setup shared in-memory test database using StaticPool
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
db_module.engine = test_engine


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def test_full_mission_workflow():
    with TestClient(app) as client:
        # 1. Create a Pathway
        p_resp = client.post("/api/pathways/", json={"name": "Fool", "sequence_0_title": "The Fool"})
        assert p_resp.status_code == 201
        pathway_id = p_resp.json()["id"]

        # 2. Create Beyonder Operative A (Sequence 4 - Bizarro Sorcerer)
        b1_resp = client.post("/api/beyonders/", json={
            "pathway_id": pathway_id,
            "codename": "Bizarro Operative",
            "sequence_level": 4,
            "sanity_percentage": 90.0,
            "affiliation": "Tarot Club"
        })
        assert b1_resp.status_code == 201
        b1_id = b1_resp.json()["id"]

        # 3. Create Beyonder Operative B (Sequence 8 - Clown, weaker rank)
        b2_resp = client.post("/api/beyonders/", json={
            "pathway_id": pathway_id,
            "codename": "Novice Clown",
            "sequence_level": 8,
            "sanity_percentage": 85.0,
            "affiliation": "Tarot Club"
        })
        assert b2_resp.status_code == 201
        b2_id = b2_resp.json()["id"]

        # 4. Create High-Hazard Commission (Hazard Rank 3)
        c_resp = client.post("/api/commissions/", json={
            "title": "Banish Demonic Entity",
            "hazard_rank": 3,
            "target": "Ancient Spirit",
            "location": "Backlund District",
            "reward_gold": 500.0
        })
        assert c_resp.status_code == 201
        comm_id = c_resp.json()["id"]

        # 5. Invalid Claim Attempt: Operative B (Seq 8) tries to claim Hazard Rank 3 mission
        # Expect 400 Bad Request ("Sequence rank insufficient for commission hazard level")
        invalid_claim = client.post(f"/api/commissions/{comm_id}/claim", json={"beyonder_id": b2_id})
        assert invalid_claim.status_code == 400
        assert invalid_claim.json()["detail"] == "Sequence rank insufficient for commission hazard level"

        # 6. Valid Claim Attempt: Operative A (Seq 4) claims Hazard Rank 5 mission (4 <= 5 -> Valid!)
        c2_resp = client.post("/api/commissions/", json={
            "title": "Purify Sewer Spirit",
            "hazard_rank": 5,
            "target": "Slime Wraith",
            "location": "East Borough",
            "reward_gold": 100.0
        })
        c2_id = c2_resp.json()["id"]

        valid_claim = client.post(f"/api/commissions/{c2_id}/claim", json={"beyonder_id": b1_id})
        assert valid_claim.status_code == 200
        claim_id = valid_claim.json()["claim_id"]

        # Verify commission status is now CLAIMED
        comm_check = client.get(f"/api/commissions/{c2_id}")
        assert comm_check.json()["status"] == "CLAIMED"

        # 7. Post Mission Debrief and Update Sanity
        debrief_resp = client.post(f"/api/claims/{claim_id}/debrief", json={
            "debrief_notes": "Entity banished successfully, but incurred mild mental strain.",
            "sanity_change": -5.0,
            "status": "COMPLETED"
        })
        assert debrief_resp.status_code == 200

        # Verify Beyonder sanity updated (90.0 - 5.0 = 85.0)
        beyonder_check = client.get(f"/api/beyonders/{b1_id}")
        assert beyonder_check.json()["sanity_percentage"] == 85.0
