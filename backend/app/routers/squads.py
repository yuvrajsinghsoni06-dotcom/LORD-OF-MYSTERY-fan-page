from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Squad, SquadMember, Beyonder, Commission, Claim
from app.schemas import SquadCreate, SquadUpdate, SquadResponse, SquadMemberResponse
from app.validation import validate_squad_formation_members, calculate_squad_synergies

router = APIRouter(prefix="/api/squads", tags=["Squad Formation"])


def format_squad_response(squad: Squad) -> dict:
    members_data = []
    seq_levels = []
    sanities = []
    pathways = []

    for sm in squad.members:
        b = sm.beyonder
        if b:
            seq_levels.append(b.sequence_level)
            sanities.append(b.sanity_percentage)
            p_name = b.pathway.name if b.pathway else None
            pathways.append(p_name)
            members_data.append({
                "id": sm.id,
                "beyonder_id": sm.beyonder_id,
                "role": sm.role,
                "codename": b.codename,
                "sequence_level": b.sequence_level,
                "sequence_name": b.sequence_name,
                "pathway_name": p_name,
                "affiliation": b.affiliation,
                "sanity_percentage": b.sanity_percentage,
                "avatar_url": b.avatar_url
            })

    member_count = len(members_data)
    avg_seq = round(sum(seq_levels) / member_count, 1) if member_count > 0 else 9.0
    avg_sanity = round(sum(sanities) / member_count, 1) if member_count > 0 else 100.0
    # In LOTM, lower sequence rank number is more powerful. Best hazard clearance = minimum sequence number
    hazard_clearance = min(seq_levels) if seq_levels else 9
    synergies = calculate_squad_synergies(pathways)

    return {
        "id": squad.id,
        "name": squad.name,
        "motto": squad.motto,
        "formation_type": squad.formation_type,
        "status": squad.status,
        "member_count": member_count,
        "average_sequence": avg_seq,
        "average_sanity": avg_sanity,
        "hazard_clearance": hazard_clearance,
        "synergies": synergies,
        "members": members_data
    }


@router.get("/", response_model=List[SquadResponse])
def get_squads(db: Session = Depends(get_db)):
    squads = db.query(Squad).all()
    return [format_squad_response(s) for s in squads]


@router.get("/{squad_id}", response_model=SquadResponse)
def get_squad(squad_id: int, db: Session = Depends(get_db)):
    squad = db.query(Squad).filter(Squad.id == squad_id).first()
    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")
    return format_squad_response(squad)


@router.post("/", response_model=SquadResponse, status_code=status.HTTP_201_CREATED)
def create_squad(payload: SquadCreate, db: Session = Depends(get_db)):
    # Enforce strict 3-4 members rule
    validate_squad_formation_members(payload.member_ids)

    # Check for duplicate name
    existing = db.query(Squad).filter(Squad.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="A squad with this name already exists")

    # Verify all beyonders exist
    beyonders = db.query(Beyonder).filter(Beyonder.id.in_(payload.member_ids)).all()
    if len(beyonders) != len(payload.member_ids):
        raise HTTPException(status_code=404, detail="One or more specified Beyonders do not exist")

    squad = Squad(
        name=payload.name,
        motto=payload.motto,
        formation_type=payload.formation_type or "BALANCED",
        status="READY"
    )
    db.add(squad)
    db.flush()

    roles_dict = payload.member_roles or {}
    default_roles = ["Squad Leader", "Vanguard", "Controller", "Support"]

    for idx, b_id in enumerate(payload.member_ids):
        assigned_role = roles_dict.get(str(b_id)) or roles_dict.get(b_id) or (default_roles[idx] if idx < len(default_roles) else "Specialist")
        sm = SquadMember(
            squad_id=squad.id,
            beyonder_id=b_id,
            role=assigned_role
        )
        db.add(sm)

    db.commit()
    db.refresh(squad)
    return format_squad_response(squad)


@router.put("/{squad_id}", response_model=SquadResponse)
def update_squad(squad_id: int, payload: SquadUpdate, db: Session = Depends(get_db)):
    squad = db.query(Squad).filter(Squad.id == squad_id).first()
    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")

    if payload.name is not None and payload.name != squad.name:
        existing = db.query(Squad).filter(Squad.name == payload.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="A squad with this name already exists")
        squad.name = payload.name

    if payload.motto is not None:
        squad.motto = payload.motto
    if payload.formation_type is not None:
        squad.formation_type = payload.formation_type
    if payload.status is not None:
        squad.status = payload.status

    if payload.member_ids is not None:
        # Enforce strict 3-4 members rule
        validate_squad_formation_members(payload.member_ids)

        beyonders = db.query(Beyonder).filter(Beyonder.id.in_(payload.member_ids)).all()
        if len(beyonders) != len(payload.member_ids):
            raise HTTPException(status_code=404, detail="One or more specified Beyonders do not exist")

        # Replace members
        db.query(SquadMember).filter(SquadMember.squad_id == squad.id).delete()
        roles_dict = payload.member_roles or {}
        default_roles = ["Squad Leader", "Vanguard", "Controller", "Support"]

        for idx, b_id in enumerate(payload.member_ids):
            assigned_role = roles_dict.get(str(b_id)) or roles_dict.get(b_id) or (default_roles[idx] if idx < len(default_roles) else "Specialist")
            sm = SquadMember(
                squad_id=squad.id,
                beyonder_id=b_id,
                role=assigned_role
            )
            db.add(sm)

    db.commit()
    db.refresh(squad)
    return format_squad_response(squad)


@router.delete("/{squad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_squad(squad_id: int, db: Session = Depends(get_db)):
    squad = db.query(Squad).filter(Squad.id == squad_id).first()
    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")
    db.delete(squad)
    db.commit()
    return None


@router.post("/{squad_id}/dispatch")
def dispatch_squad_on_commission(squad_id: int, payload: dict, db: Session = Depends(get_db)):
    """
    Dispatches a 3-4 member squad on a mission.
    Validates squad hazard clearance against the commission hazard rank.
    """
    commission_id = payload.get("commission_id")
    if not commission_id:
        raise HTTPException(status_code=400, detail="commission_id is required")

    squad = db.query(Squad).filter(Squad.id == squad_id).first()
    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")

    commission = db.query(Commission).filter(Commission.id == commission_id).first()
    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")

    if commission.status != "OPEN":
        raise HTTPException(status_code=400, detail=f"Commission is {commission.status}, not OPEN for dispatch")

    # Check squad member count (3-4 only)
    if len(squad.members) < 3 or len(squad.members) > 4:
        raise HTTPException(status_code=400, detail="Squad must have between 3 and 4 members to deploy.")

    # Calculate squad highest clearance (lowest sequence number)
    member_seqs = [sm.beyonder.sequence_level for sm in squad.members if sm.beyonder]
    highest_rank = min(member_seqs) if member_seqs else 9

    if highest_rank > commission.hazard_rank:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Squad highest sequence rank ({highest_rank}) is insufficient for commission hazard rank ({commission.hazard_rank})"
        )

    # Lead operative claims the mission for the squad
    lead_member = squad.members[0].beyonder
    claim = Claim(
        commission_id=commission.id,
        beyonder_id=lead_member.id,
        status="ACTIVE",
        debrief_notes=f"Dispatched full squad '{squad.name}' ({len(squad.members)} operatives)."
    )
    commission.status = "CLAIMED"
    squad.status = "DEPLOYED"

    db.add(claim)
    db.commit()
    db.refresh(claim)

    return {
        "success": True,
        "message": f"Squad '{squad.name}' ({len(squad.members)} operatives) deployed to '{commission.title}'!",
        "claim_id": claim.id,
        "squad_name": squad.name,
        "commission_title": commission.title
    }
