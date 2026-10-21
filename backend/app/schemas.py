from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


# Pathway Schemas
class PathwayBase(BaseModel):
    name: str
    sequence_0_title: str


class PathwayCreate(PathwayBase):
    pass


class PathwayResponse(PathwayBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Beyonder Schemas
class BeyonderBase(BaseModel):
    pathway_id: int
    codename: str
    sequence_level: int = Field(..., ge=0, le=9)
    sequence_name: Optional[str] = None
    sanity_percentage: float = Field(100.0, ge=0.0, le=100.0)
    affiliation: str
    characteristics: Optional[str] = None


class BeyonderCreate(BeyonderBase):
    pass


class BeyonderUpdate(BaseModel):
    codename: Optional[str] = None
    sequence_level: Optional[int] = Field(None, ge=0, le=9)
    sequence_name: Optional[str] = None
    sanity_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    affiliation: Optional[str] = None
    characteristics: Optional[str] = None
    pathway_id: Optional[int] = None


class BeyonderResponse(BeyonderBase):
    id: int
    pathway_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Potion Schemas
class PotionBase(BaseModel):
    pathway_id: int
    sequence_level: int = Field(..., ge=0, le=9)
    main_ingredients: str
    supplementary_ingredients: str
    abilities: str


class PotionCreate(PotionBase):
    pass


class PotionResponse(PotionBase):
    id: int
    pathway_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Commission Schemas
class CommissionBase(BaseModel):
    title: str
    hazard_rank: int = Field(..., ge=0, le=9)
    target: str
    location: str
    reward_gold: float = Field(0.0, ge=0.0)


class CommissionCreate(CommissionBase):
    pass


class CommissionUpdate(BaseModel):
    title: Optional[str] = None
    hazard_rank: Optional[int] = Field(None, ge=0, le=9)
    target: Optional[str] = None
    location: Optional[str] = None
    reward_gold: Optional[float] = Field(None, ge=0.0)
    status: Optional[str] = None


class CommissionResponse(CommissionBase):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)


# Claim Schemas
class ClaimCreate(BaseModel):
    commission_id: int
    beyonder_id: int


class ClaimDebrief(BaseModel):
    debrief_notes: str
    sanity_change: Optional[float] = 0.0  # Positive to restore, negative for corruption/loss
    new_sanity_percentage: Optional[float] = None
    status: Optional[str] = "COMPLETED"  # COMPLETED or FAILED


class ClaimResponse(BaseModel):
    id: int
    commission_id: int
    beyonder_id: int
    claim_date: datetime
    status: str
    debrief_notes: Optional[str] = None
    commission_title: Optional[str] = None
    beyonder_codename: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Dashboard summary metrics
class DashboardMetrics(BaseModel):
    total_beyonders: int
    active_agents: int
    high_risk_commissions: int
    average_sanity: float
    total_commissions: int
    open_commissions: int
    completed_commissions: int
    corrupted_beyonders_count: int
