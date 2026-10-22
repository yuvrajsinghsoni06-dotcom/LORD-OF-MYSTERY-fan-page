from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Pathway(Base):
    __tablename__ = "pathways"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    sequence_0_title = Column(String, nullable=False)

    beyonders = relationship("Beyonder", back_populates="pathway", cascade="all, delete-orphan")
    potions = relationship("Potion", back_populates="pathway", cascade="all, delete-orphan")


class Beyonder(Base):
    __tablename__ = "beyonders"

    id = Column(Integer, primary_key=True, index=True)
    pathway_id = Column(Integer, ForeignKey("pathways.id", ondelete="CASCADE"), nullable=False)
    codename = Column(String, nullable=False, index=True)
    sequence_level = Column(Integer, nullable=False)  # 0 - 9
    sequence_name = Column(String, nullable=True)  # e.g., "Bizarro Sorcerer", "Nightmare"
    sanity_percentage = Column(Float, nullable=False, default=100.0)  # 0.0 - 100.0%
    affiliation = Column(String, nullable=False)
    characteristics = Column(Text, nullable=True)  # Abilities, sealed artifacts, traits, mythical creature forms
    avatar_url = Column(String, nullable=True)  # Visual character portrait URL or SVG avatar

    pathway = relationship("Pathway", back_populates="beyonders")
    claims = relationship("Claim", back_populates="beyonder", cascade="all, delete-orphan")
    squad_memberships = relationship("SquadMember", back_populates="beyonder", cascade="all, delete-orphan")


class Potion(Base):
    __tablename__ = "potions"

    id = Column(Integer, primary_key=True, index=True)
    pathway_id = Column(Integer, ForeignKey("pathways.id", ondelete="CASCADE"), nullable=False)
    sequence_level = Column(Integer, nullable=False)  # 0 - 9
    main_ingredients = Column(Text, nullable=False)
    supplementary_ingredients = Column(Text, nullable=False)
    abilities = Column(Text, nullable=False)

    pathway = relationship("Pathway", back_populates="potions")


class Commission(Base):
    __tablename__ = "commissions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    hazard_rank = Column(Integer, nullable=False)  # 0 - 9
    target = Column(String, nullable=False)
    location = Column(String, nullable=False)
    reward_gold = Column(Float, nullable=False, default=0.0)
    status = Column(String, nullable=False, default="OPEN")  # OPEN, CLAIMED, COMPLETED

    claims = relationship("Claim", back_populates="commission", cascade="all, delete-orphan")


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    commission_id = Column(Integer, ForeignKey("commissions.id", ondelete="CASCADE"), nullable=False)
    beyonder_id = Column(Integer, ForeignKey("beyonders.id", ondelete="CASCADE"), nullable=False)
    claim_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    status = Column(String, nullable=False, default="ACTIVE")  # ACTIVE, COMPLETED, FAILED
    debrief_notes = Column(Text, nullable=True)

    commission = relationship("Commission", back_populates="claims")
    beyonder = relationship("Beyonder", back_populates="claims")


class Squad(Base):
    __tablename__ = "squads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    motto = Column(String, nullable=True)
    formation_type = Column(String, nullable=False, default="BALANCED")  # BALANCED, ASSAULT, DEFENSIVE, INVESTIGATION, RITUAL
    status = Column(String, nullable=False, default="READY")  # READY, DEPLOYED

    members = relationship("SquadMember", back_populates="squad", cascade="all, delete-orphan")


class SquadMember(Base):
    __tablename__ = "squad_members"

    id = Column(Integer, primary_key=True, index=True)
    squad_id = Column(Integer, ForeignKey("squads.id", ondelete="CASCADE"), nullable=False)
    beyonder_id = Column(Integer, ForeignKey("beyonders.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False, default="Vanguard")  # Leader, Vanguard, Controller, Support, Diviner

    squad = relationship("Squad", back_populates="members")
    beyonder = relationship("Beyonder", back_populates="squad_memberships")

