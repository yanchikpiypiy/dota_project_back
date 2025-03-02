from pydantic import BaseModel

class HeroesDTO(BaseModel):
    id: int
    name: str
    roles: dict
    short_desc: str
    long_desc: str
    primary_attribute: str
    attack_type: str
    baseHealth: str
    baseMana: str
    manaGain: float
    healthGain: float
    baseArmor: str
    base_str: str
    base_agi: str
    base_int: str
    str_gain: float
    agi_gain: float
    int_gain: float
    complexity: int
    baseDmg: str
    attackTime: str
    attackRange: str
    projectileSpeed: str
    magicResist: str
    moveSpeed: str
    turnRate: str
    vision: str
    # abilities: Mapped[list["HeroAbilityOrm"]] = relationship("HeroAbilityOrm", back_populates="hero", cascade="all, delete-orphan")


class HeroAbilitiesDTO(BaseModel):
    id: int 
    name: str 
    description: str 
    cooldown: str
    mana_cost: str 
    general_details: dict
    specific_details: dict

class HeroRelDTO(HeroesDTO):
    abilities: list["HeroAbilitiesDTO"]


class HeroAbilitiesRelDTO(HeroAbilitiesDTO):
    hero: "HeroesDTO"