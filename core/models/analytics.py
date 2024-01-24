from sqlalchemy import Integer, Float, Text
from sqlalchemy.orm import mapped_column as column, Mapped

from core.models.base import Base


class Demand(Base):
    __tablename__ = 'demand'

    year: Mapped[int] = column(Integer, primary_key=True, autoincrement=True)
    salary: Mapped[int] = column(Integer, nullable=False)
    vacancies_count: Mapped[int] = column(Integer, nullable=False)
    salary_profession: Mapped[int] = column(Integer, nullable=False)
    vacancies_count_profession: Mapped[int] = column(Integer, nullable=False)


class GeographySalary(Base):
    __tablename__ = 'geography_salary'

    city: Mapped[str] = column(Text, primary_key=True, autoincrement=True)
    salary: Mapped[int] = column(Integer, nullable=False)


class GeographySalaryProfession(Base):
    __tablename__ = 'geography_salary_profession'

    city: Mapped[str] = column(Text, primary_key=True, autoincrement=True)
    salary: Mapped[int] = column(Integer, nullable=False)


class GeographyVacancyRate(Base):
    __tablename__ = 'geography_vacancy_rate'

    city: Mapped[str] = column(Text, primary_key=True, autoincrement=True)
    vacancy_rate: Mapped[float] = column(Float, nullable=False)


class GeographyVacancyRateProfession(Base):
    __tablename__ = 'geography_vacancy_rate_profession'

    city: Mapped[str] = column(Text, primary_key=True, autoincrement=True)
    vacancy_rate: Mapped[float] = column(Float, nullable=False)


class KeySkillsTop(Base):
    __tablename__ = 'key_skills_top'

    year: Mapped[int] = column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[str] = column(Text, nullable=False)


class KeySkillsTopWithProfession(Base):
    __tablename__ = 'key_skills_top_with_profession'

    year: Mapped[int] = column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[str] = column(Text, nullable=False)
