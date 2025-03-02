from sqlalchemy.orm import aliased,selectinload
from sqlalchemy import select
from database import session_factory, engine, Base
from models import User, HeroesOrm, HeroRoles, HeroAbilityOrm
from schemas import HeroesDTO, HeroRelDTO
import json
class SyncORM():
    @staticmethod
    def create_tables():
        engine.echo = False
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        engine.echo = True

    @staticmethod
    def insert_heroes():
        with session_factory() as session:
            # print("Starting session...")

            # Open the hero and ability data files
            with open("improved_dota_hero_stats.json", "r") as file:
                hero_data_list = json.load(file)
            with open("dota2_official_abilities.json", "r") as file:
                ability_data_list = json.load(file)

            heroes_dict = {}

            # Insert heroes into the database
            for hero_data in hero_data_list:
                hero_fields = {}
                for key, value in hero_data.items():
                    if hasattr(HeroesOrm, key):  # Check if the field exists in the model
                        # Handle numeric fields
                        if key in ['baseHealth', 'baseMana', 'base_str', 'base_agi', 'base_int', 'str_gain', 'agi_gain', 'int_gain', 'attackTime']:
                            hero_fields[key] = float(value) if '.' in str(value) else int(value)
                        else:
                            hero_fields[key] = value

                # Create hero instance and add to session
                hero = HeroesOrm(**hero_fields)
                session.add(hero)

                # Keep track of the hero by name for later linking abilities
                heroes_dict[hero_data["name"]] = hero

            # Commit heroes to the database
            session.flush()
        

            # Insert abilities into the database and associate them with the correct hero
            for hero_abilities in ability_data_list:
                hero_name = hero_abilities.get("hero_name")
                if not hero_name:
                    continue  # Skip abilities without a valid hero association

                # Find the hero object by name
                hero = heroes_dict.get(hero_name)
                if not hero:
                    continue  # Skip abilities with no matching hero

                # Process each ability for the hero
                for ability_data in hero_abilities.get("abilities", []):
                    ability_fields = {}
                    for key, value in ability_data.items():
                        if hasattr(HeroAbilityOrm, key):  # Check if the field exists in the model
                            ability_fields[key] = value

                    # Create ability instance and associate with hero
                    ability = HeroAbilityOrm(**ability_fields)
                    hero.abilities.append(ability)

            

            # Commit all changes (heroes and abilities) to the database
            session.commit()

    @staticmethod
    def get_heroes_by_attributes(attribute:str):
        with session_factory() as session:
            query = (
                select(HeroesOrm).filter(HeroesOrm.primary_attribute == attribute)
            )

            result = session.execute(query).scalars().all()
            # for hero in result:
            #     print(hero)

    @staticmethod
    def get_heroes_with_abbilities():
        with session_factory() as session:
            query = select(HeroesOrm).options(selectinload(HeroesOrm.abilities))

            res = session.execute(query)
            result = res.scalars().all()
            print(result)

    @staticmethod
    def convert_heroes_to_dto():
        with session_factory() as session:
            query = select(HeroesOrm)
            result = session.execute(query).scalars().all()

            result_dto = [HeroesDTO.model_validate(row, from_attributes=True) for row in result]

            return result_dto
        
    
    @staticmethod
    def convert_heroes_with_abilities_to_dto(hero_name: str):
        with session_factory() as session:
            query = (
                select(HeroesOrm).options(selectinload(HeroesOrm.abilities)).filter(HeroesOrm.name == hero_name)
            )

            result = session.execute(query).first()

             # Process each hero and their abilities
            for hero in result:
                for ability in hero.abilities:
                    if ability.cooldown is None:
                        ability.cooldown = ""  # Replace None with an empty string or a default value
                    if ability.mana_cost is None:
                        ability.mana_cost = ""  # Replace None with an empty string or a default value
                    if ability.description is None:
                        ability.description = ""
            result_dto = [HeroRelDTO.model_validate(row, from_attributes=True) for row in result]

            return result_dto