from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Commission, Beyonder, Claim
from app.schemas import CommissionCreate, CommissionUpdate, CommissionResponse, ClaimResponse
from app.validation import validate_sequence_level_for_claim

router = APIRouter(prefix="/api/commissions", tags=["Commissions"])


@router.get("/", response_model=List[CommissionResponse])
def get_commissions(
    status: Optional[str] = None,
    hazard_rank: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Commission)
    if status:
        query = query.filter(Commission.status == status.upper())
    if hazard_rank is not None:
        query = query.filter(Commission.hazard_rank == hazard_rank)
    if search:
        query = query.filter(
            (Commission.title.ilike(f"%{search}%")) |
            (Commission.target.ilike(f"%{search}%")) |
            (Commission.location.ilike(f"%{search}%"))
        )
    
    return query.order_by(Commission.hazard_rank.desc(), Commission.id.desc()).all()


@router.get("/{commission_id}", response_model=CommissionResponse)
def get_commission(commission_id: int, db: Session = Depends(get_db)):
    commission = db.query(Commission).filter(Commission.id == commission_id).first()
    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    return commission


@router.post("/", response_model=CommissionResponse, status_code=status.HTTP_201_CREATED)
def create_commission(commission_in: CommissionCreate, db: Session = Depends(get_db)):
    commission = Commission(
        title=commission_in.title,
        hazard_rank=commission_in.hazard_rank,
        target=commission_in.target,
        location=commission_in.location,
        reward_gold=commission_in.reward_gold,
        status="OPEN"
    )
    db.add(commission)
    db.commit()
    db.refresh(commission)
    return commission


@router.put("/{commission_id}", response_model=CommissionResponse)
def update_commission(commission_id: int, commission_in: CommissionUpdate, db: Session = Depends(get_db)):
    commission = db.query(Commission).filter(Commission.id == commission_id).first()
    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    
    update_data = commission_in.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        if val is not None:
            if key == "status":
                setattr(commission, key, val.upper())
            else:
                setattr(commission, key, val)
            
    db.commit()
    db.refresh(commission)
    return commission


@router.delete("/{commission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commission(commission_id: int, db: Session = Depends(get_db)):
    commission = db.query(Commission).filter(Commission.id == commission_id).first()
    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    db.delete(commission)
    db.commit()
    return None


@router.post("/{commission_id}/claim")
def claim_commission(commission_id: int, payload: dict, db: Session = Depends(get_db)):
    """
    Direct endpoint for React frontend:
    POST /api/commissions/{id}/claim with { "beyonder_id": X }
    Runs validation logic, writes row to claims, updates commission status to CLAIMED.
    """
    beyonder_id = payload.get("beyonder_id")
    if not beyonder_id:
        raise HTTPException(status_code=400, detail="beyonder_id is required")
    
    commission = db.query(Commission).filter(Commission.id == commission_id).first()
    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    
    if commission.status != "OPEN":
        raise HTTPException(status_code=400, detail=f"Commission is currently {commission.status}, not OPEN for claiming")
    
    beyonder = db.query(Beyonder).filter(Beyonder.id == beyonder_id).first()
    if not beyonder:
        raise HTTPException(status_code=404, detail="Beyonder not found")
    
    # Validation engine rule check:
    validate_sequence_level_for_claim(beyonder.sequence_level, commission.hazard_rank)
    
    # Create claim record
    claim = Claim(
        commission_id=commission.id,
        beyonder_id=beyonder.id,
        status="ACTIVE"
    )
    commission.status = "CLAIMED"
    
    db.add(claim)
    db.commit()
    db.refresh(claim)
    
    return {
        "success": True,
        "claim_id": claim.id,
        "message": f"Mission '{commission.title}' claimed successfully by Beyonder {beyonder.codename}",
        "claim": {
            "id": claim.id,
            "commission_id": claim.commission_id,
            "beyonder_id": claim.beyonder_id,
            "claim_date": claim.claim_date,
            "status": claim.status,
            "debrief_notes": claim.debrief_notes
        }
    }
