from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Claim, Commission, Beyonder, Squad
from app.schemas import ClaimCreate, ClaimDebrief, ClaimResponse, DashboardMetrics
from app.validation import validate_sequence_level_for_claim

router = APIRouter(prefix="/api/claims", tags=["Claims & Dispatch"])


def format_claim_response(claim: Claim) -> dict:
    return {
        "id": claim.id,
        "commission_id": claim.commission_id,
        "beyonder_id": claim.beyonder_id,
        "claim_date": claim.claim_date,
        "status": claim.status,
        "debrief_notes": claim.debrief_notes,
        "commission_title": claim.commission.title if claim.commission else None,
        "beyonder_codename": claim.beyonder.codename if claim.beyonder else None,
    }


@router.get("/", response_model=List[ClaimResponse])
def get_claims(
    status: Optional[str] = None,
    beyonder_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Claim)
    if status:
        query = query.filter(Claim.status == status.upper())
    if beyonder_id:
        query = query.filter(Claim.beyonder_id == beyonder_id)
        
    claims = query.order_by(Claim.id.desc()).all()
    return [format_claim_response(c) for c in claims]


@router.get("/metrics", response_model=DashboardMetrics)
def get_dashboard_metrics(db: Session = Depends(get_db)):
    beyonders = db.query(Beyonder).all()
    commissions = db.query(Commission).all()
    
    total_beyonders = len(beyonders)
    active_agents = len([b for b in beyonders if b.sanity_percentage > 30.0])
    corrupted_count = len([b for b in beyonders if b.sanity_percentage <= 30.0])
    
    total_sanity = sum([b.sanity_percentage for b in beyonders]) if total_beyonders > 0 else 100.0
    avg_sanity = round(total_sanity / total_beyonders, 1) if total_beyonders > 0 else 100.0
    
    total_commissions = len(commissions)
    high_risk_commissions = len([c for c in commissions if c.hazard_rank >= 5 and c.status == "OPEN"])
    open_commissions = len([c for c in commissions if c.status == "OPEN"])
    completed_commissions = len([c for c in commissions if c.status == "COMPLETED"])
    total_squads = db.query(Squad).count()
    
    return DashboardMetrics(
        total_beyonders=total_beyonders,
        active_agents=active_agents,
        high_risk_commissions=high_risk_commissions,
        average_sanity=avg_sanity,
        total_commissions=total_commissions,
        open_commissions=open_commissions,
        completed_commissions=completed_commissions,
        corrupted_beyonders_count=corrupted_count,
        total_squads=total_squads
    )


@router.get("/{claim_id}", response_model=ClaimResponse)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return format_claim_response(claim)


@router.post("/", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
def dispatch_claim(claim_in: ClaimCreate, db: Session = Depends(get_db)):
    """
    Dispatch endpoint /api/claims/ containing sequence rank validation checks.
    """
    commission = db.query(Commission).filter(Commission.id == claim_in.commission_id).first()
    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
        
    if commission.status != "OPEN":
        raise HTTPException(status_code=400, detail=f"Commission is currently {commission.status}, not OPEN for dispatch")
        
    beyonder = db.query(Beyonder).filter(Beyonder.id == claim_in.beyonder_id).first()
    if not beyonder:
        raise HTTPException(status_code=404, detail="Beyonder not found")
        
    # Sequence rank validation check
    validate_sequence_level_for_claim(beyonder.sequence_level, commission.hazard_rank)
    
    claim = Claim(
        commission_id=commission.id,
        beyonder_id=beyonder.id,
        status="ACTIVE"
    )
    commission.status = "CLAIMED"
    
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return format_claim_response(claim)


@router.post("/{claim_id}/debrief", response_model=ClaimResponse)
def post_debrief(claim_id: int, debrief_in: ClaimDebrief, db: Session = Depends(get_db)):
    """
    Sanity & Corruption State Updater:
    Updates agent sanity upon logging post-mission debriefs.
    """
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
        
    claim.debrief_notes = debrief_in.debrief_notes
    claim.status = debrief_in.status if debrief_in.status else "COMPLETED"
    
    # Update commission status
    if claim.commission:
        claim.commission.status = "COMPLETED" if claim.status == "COMPLETED" else "OPEN"
        
    # Update beyonder sanity
    if claim.beyonder:
        if debrief_in.new_sanity_percentage is not None:
            new_sanity = debrief_in.new_sanity_percentage
        elif debrief_in.sanity_change is not None:
            new_sanity = claim.beyonder.sanity_percentage + debrief_in.sanity_change
        else:
            new_sanity = claim.beyonder.sanity_percentage
            
        # Bound sanity between 0.0% and 100.0%
        claim.beyonder.sanity_percentage = max(0.0, min(100.0, new_sanity))
        
    db.commit()
    db.refresh(claim)
    return format_claim_response(claim)
