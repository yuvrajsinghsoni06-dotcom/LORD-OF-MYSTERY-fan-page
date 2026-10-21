from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Potion, Pathway
from app.schemas import PotionCreate, PotionResponse

router = APIRouter(prefix="/api/potions", tags=["Potions"])


def format_potion_response(potion: Potion) -> dict:
    return {
        "id": potion.id,
        "pathway_id": potion.pathway_id,
        "sequence_level": potion.sequence_level,
        "main_ingredients": potion.main_ingredients,
        "supplementary_ingredients": potion.supplementary_ingredients,
        "abilities": potion.abilities,
        "pathway_name": potion.pathway.name if potion.pathway else None,
    }


@router.get("/", response_model=List[PotionResponse])
def get_potions(
    pathway_id: Optional[int] = None,
    sequence_level: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Potion)
    if pathway_id:
        query = query.filter(Potion.pathway_id == pathway_id)
    if sequence_level is not None:
        query = query.filter(Potion.sequence_level == sequence_level)
    if search:
        query = query.filter(
            (Potion.abilities.ilike(f"%{search}%")) |
            (Potion.main_ingredients.ilike(f"%{search}%")) |
            (Potion.supplementary_ingredients.ilike(f"%{search}%"))
        )
    
    potions = query.order_by(Potion.sequence_level.desc()).all()
    return [format_potion_response(p) for p in potions]


@router.get("/{potion_id}", response_model=PotionResponse)
def get_potion(potion_id: int, db: Session = Depends(get_db)):
    potion = db.query(Potion).filter(Potion.id == potion_id).first()
    if not potion:
        raise HTTPException(status_code=404, detail="Potion recipe not found")
    return format_potion_response(potion)


@router.post("/", response_model=PotionResponse, status_code=status.HTTP_201_CREATED)
def create_potion(potion_in: PotionCreate, db: Session = Depends(get_db)):
    pathway = db.query(Pathway).filter(Pathway.id == potion_in.pathway_id).first()
    if not pathway:
        raise HTTPException(status_code=404, detail="Pathway not found")
    
    potion = Potion(
        pathway_id=potion_in.pathway_id,
        sequence_level=potion_in.sequence_level,
        main_ingredients=potion_in.main_ingredients,
        supplementary_ingredients=potion_in.supplementary_ingredients,
        abilities=potion_in.abilities
    )
    db.add(potion)
    db.commit()
    db.refresh(potion)
    return format_potion_response(potion)
