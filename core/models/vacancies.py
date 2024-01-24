from sqlalchemy import Text, BigInteger, SmallInteger
from sqlalchemy.orm import mapped_column as column, Mapped

from core.models.base import Base


class Vacancies(Base):
    __tablename__ = 'vacancies'

    id: Mapped[int] = column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = column(Text)
    key_skills: Mapped[str] = column(Text)
    salary: Mapped[int] = column(BigInteger)
    area_name: Mapped[str] = column(Text, nullable=False)
    year: Mapped[int] = column(SmallInteger, nullable=False)
