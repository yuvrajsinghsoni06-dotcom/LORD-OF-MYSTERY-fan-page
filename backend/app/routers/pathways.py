from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pathway
from app.schemas import PathwayCreate, PathwayResponse

router = APIRouter(prefix="/api/pathways", tags=["Pathways"])


@router.get("/", response_model=List[PathwayResponse])
def get_pathways(db: Session = Depends(get_db)):
    return db.query(Pathway).order_by(Pathway.name).all()


@router.get("/{pathway_id}", response_model=PathwayResponse)
def get_pathway(pathway_id: int, db: Session = Depends(get_db)):
    pathway = db.query(Pathway).filter(Pathway.id == pathway_id).first()
    if not pathway:
        raise HTTPException(status_code=404, detail="Pathway not found")
    return pathway


@router.post("/", response_model=PathwayResponse, status_code=status.HTTP_201_CREATED)
def create_pathway(pathway_in: PathwayCreate, db: Session = Depends(get_db)):
    existing = db.query(Pathway).filter(Pathway.name == pathway_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Pathway with this name already exists")
    
    pathway = Pathway(name=pathway_in.name, sequence_0_title=pathway_in.sequence_0_title)
    db.add(pathway)
    db.commit()
    db.refresh(pathway)
    return pathway
