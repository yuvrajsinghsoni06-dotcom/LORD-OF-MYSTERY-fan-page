from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Beyonder, Pathway
from app.schemas import BeyonderCreate, BeyonderUpdate, BeyonderResponse

router = APIRouter(prefix="/api/beyonders", tags=["Beyonders"])


def format_beyonder_response(beyonder: Beyonder) -> dict:
    return {
        "id": beyonder.id,
        "pathway_id": beyonder.pathway_id,
        "codename": beyonder.codename,
        "sequence_level": beyonder.sequence_level,
        "sequence_name": beyonder.sequence_name,
        "sanity_percentage": beyonder.sanity_percentage,
        "affiliation": beyonder.affiliation,
        "characteristics": beyonder.characteristics,
        "avatar_url": beyonder.avatar_url,
        "pathway_name": beyonder.pathway.name if beyonder.pathway else None,
    }


@router.get("/", response_model=List[BeyonderResponse])
def get_beyonders(
    search: Optional[str] = None,
    pathway_id: Optional[int] = None,
    affiliation: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Beyonder)
    if pathway_id:
        query = query.filter(Beyonder.pathway_id == pathway_id)
    if affiliation:
        query = query.filter(Beyonder.affiliation.ilike(f"%{affiliation}%"))
    if search:
        query = query.filter(
            (Beyonder.codename.ilike(f"%{search}%")) | 
            (Beyonder.affiliation.ilike(f"%{search}%")) |
            (Beyonder.sequence_name.ilike(f"%{search}%")) |
            (Beyonder.characteristics.ilike(f"%{search}%"))
        )
    
    beyonders = query.order_by(Beyonder.sequence_level.asc(), Beyonder.codename.asc()).all()
    return [format_beyonder_response(b) for b in beyonders]


@router.get("/{beyonder_id}", response_model=BeyonderResponse)
def get_beyonder(beyonder_id: int, db: Session = Depends(get_db)):
    beyonder = db.query(Beyonder).filter(Beyonder.id == beyonder_id).first()
    if not beyonder:
        raise HTTPException(status_code=404, detail="Beyonder not found")
    return format_beyonder_response(beyonder)


@router.post("/", response_model=BeyonderResponse, status_code=status.HTTP_201_CREATED)
def create_beyonder(beyonder_in: BeyonderCreate, db: Session = Depends(get_db)):
    pathway = db.query(Pathway).filter(Pathway.id == beyonder_in.pathway_id).first()
    if not pathway:
        raise HTTPException(status_code=404, detail="Pathway not found")
    
    beyonder = Beyonder(
        pathway_id=beyonder_in.pathway_id,
        codename=beyonder_in.codename,
        sequence_level=beyonder_in.sequence_level,
        sequence_name=beyonder_in.sequence_name,
        sanity_percentage=beyonder_in.sanity_percentage,
        affiliation=beyonder_in.affiliation,
        characteristics=beyonder_in.characteristics,
        avatar_url=beyonder_in.avatar_url
    )
    db.add(beyonder)
    db.commit()
    db.refresh(beyonder)
    return format_beyonder_response(beyonder)


@router.put("/{beyonder_id}", response_model=BeyonderResponse)
def update_beyonder(beyonder_id: int, beyonder_in: BeyonderUpdate, db: Session = Depends(get_db)):
    beyonder = db.query(Beyonder).filter(Beyonder.id == beyonder_id).first()
    if not beyonder:
        raise HTTPException(status_code=404, detail="Beyonder not found")
    
    update_data = beyonder_in.model_dump(exclude_unset=True)
    if "pathway_id" in update_data and update_data["pathway_id"] is not None:
        pathway = db.query(Pathway).filter(Pathway.id == update_data["pathway_id"]).first()
        if not pathway:
            raise HTTPException(status_code=404, detail="Pathway not found")
    
    for key, val in update_data.items():
        if val is not None:
            setattr(beyonder, key, val)
            
    db.commit()
    db.refresh(beyonder)
    return format_beyonder_response(beyonder)


@router.delete("/{beyonder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_beyonder(beyonder_id: int, db: Session = Depends(get_db)):
    beyonder = db.query(Beyonder).filter(Beyonder.id == beyonder_id).first()
    if not beyonder:
        raise HTTPException(status_code=404, detail="Beyonder not found")
    db.delete(beyonder)
    db.commit()
    return None
