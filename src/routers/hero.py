from fastapi import APIRouter
from queries.orm import SyncORM
from schemas import HeroesDTO, HeroRelDTO
router = APIRouter()

@router.get("/heroes", tags=["Heroes"], response_model=list[HeroesDTO])
def get_heroes():
    heroes = SyncORM.convert_heroes_to_dto()
    return heroes


@router.get("/heroesChad/{hero_name}", tags=["Heroes"], response_model=list[HeroRelDTO])
def get_heroes(hero_name: str):
    heroes = SyncORM.convert_heroes_with_abilities_to_dto(hero_name)
    return heroes