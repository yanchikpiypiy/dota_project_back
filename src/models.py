from sqlalchemy import  Table, Column, Integer, String, Boolean, MetaData, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256
import enum
import sqlalchemy.types as types
from sqlalchemy.dialects.postgresql import JSON
class HeroRoles(enum.Enum):
    carry = "Carry"
    escape = "Escape"
    nuker = "Nuker"
    disabler = "Disabler"
    durable = "Durable"
    initiator = "Initiator"
    support = "Support"
    pusher = "Pusher"
    jungler = "Jungler"

class HeroesOrm(Base):
    __tablename__ = "heroes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str_256]
    roles: Mapped[dict] = mapped_column(JSON, nullable=True)
    short_desc: Mapped[str]
    long_desc: Mapped[str]

    primary_attribute: Mapped[str_256]
    attack_type: Mapped[str_256]
    baseHealth: Mapped[str_256]
    baseMana: Mapped[str_256]
    manaGain: Mapped[float]
    healthGain: Mapped[float]
    baseArmor: Mapped[str]
    base_str: Mapped[str_256]
    base_agi: Mapped[str_256]
    base_int: Mapped[str_256]
    str_gain: Mapped[float]
    agi_gain: Mapped[float]
    int_gain: Mapped[float]
    complexity: Mapped[int]
    baseDmg: Mapped[str]
    attackTime: Mapped[str]
    attackRange: Mapped[str]
    projectileSpeed: Mapped[str]
    magicResist: Mapped[str]
    moveSpeed: Mapped[str]
    turnRate: Mapped[str]
    vision: Mapped[str]
    abilities: Mapped[list["HeroAbilityOrm"]] = relationship("HeroAbilityOrm", back_populates="hero", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize abilities as an empty list
        if not hasattr(self, 'abilities'):
            self.abilities = []
class HeroAbilityOrm(Base):
    __tablename__ = "heroAbilities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hero_id: Mapped[int] = mapped_column(ForeignKey("heroes.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    cooldown: Mapped[str] = mapped_column(String, nullable=True)
    mana_cost: Mapped[str] = mapped_column(String, nullable=True)
    general_details: Mapped[dict] = mapped_column(JSON, nullable=True)
    specific_details: Mapped[dict] = mapped_column(JSON, nullable=True)
    hero: Mapped["HeroesOrm"] = relationship("HeroesOrm", back_populates="abilities")
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str_256] = mapped_column(unique=True)
    username: Mapped[str_256]
    hashed_password: Mapped[str_256]
    role: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

