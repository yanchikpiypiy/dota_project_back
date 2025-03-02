from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, String
from config import settings
from typing import Annotated

engine = create_engine(
    url=settings.DATABASE_URL_psycpg,
    echo=True,
    pool_size=10
)

session_factory = sessionmaker(engine)

str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 12
    repr_cols = tuple()
    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"