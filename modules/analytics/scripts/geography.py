import asyncio

from sqlalchemy import func, column

from core.methods.database import Database, Select, Insert, Delete
from core.models.analytics import GeographySalary, GeographySalaryProfession, GeographyVacancyRateProfession, GeographyVacancyRate
from core.models.vacancies import Vacancies
from modules.analytics.scripts.config import profession_pattern


class GeographyAnalytics:

    @staticmethod
    async def dynamics_salary_by_city():
        all_vacancies = (
            Select(func.count())
            .where(Vacancies.salary < 10_000_000)
            .scalar_subquery()
        )

        return await (
            Select(Vacancies.area_name, (func.round(func.avg(Vacancies.salary))).label('salary_profession'))
            .where(Vacancies.salary < 10_000_000)
            .group_by(Vacancies.area_name)
            .having(func.count() >= 0.01 * all_vacancies)
            .order_by(column('salary_profession').desc())
            .limit(10)
            .fetch()
        )

    @staticmethod
    async def dynamics_vacancies_by_city():
        all_vacancies = (
            Select(func.count())
            .where(Vacancies.salary < 10_000_000)
            .scalar_subquery()
        )

        return await (
            Select(Vacancies.area_name, (func.round(func.count() / all_vacancies, 4)).label('vacancy_rate'))
            .where(Vacancies.salary < 10_000_000)
            .group_by(Vacancies.area_name)
            .having(func.count() >= 0.01 * all_vacancies)
            .order_by(column('vacancy_rate').desc())
            .limit(10)
            .fetch()
        )

    @staticmethod
    async def dynamics_salary_by_city_with_profession():
        all_vacancies = (
            Select(func.count())
            .where(Vacancies.salary < 10_000_000, Vacancies.name.regexp_match(profession_pattern, flags='i'))
            .scalar_subquery()
        )

        return await (
            Select(Vacancies.area_name, (func.round(func.avg(Vacancies.salary))).label('salary_profession'))
            .where(Vacancies.salary < 10_000_000, Vacancies.name.regexp_match(profession_pattern, flags='i'))
            .group_by(Vacancies.area_name)
            .having(func.count() >= 0.01 * all_vacancies)
            .order_by(column('salary_profession').desc())
            .limit(10)
            .fetch()
        )

    @staticmethod
    async def dynamics_vacancies_by_city_with_profession():
        all_vacancies = (
            Select(func.count())
            .where(Vacancies.salary < 10_000_000, Vacancies.name.regexp_match(profession_pattern, flags='i'))
            .scalar_subquery()
        )

        return await (
            Select(Vacancies.area_name, (func.round(func.count() / all_vacancies, 4)).label('vacancy_rate'))
            .where(Vacancies.salary < 10_000_000, Vacancies.name.regexp_match(profession_pattern, flags='i'))
            .group_by(Vacancies.area_name)
            .having(func.count() >= 0.01 * all_vacancies)
            .order_by(column('vacancy_rate').desc())
            .limit(10)
            .fetch()
        )

    @classmethod
    async def save_all(cls):
        await Delete(GeographySalary).execute()
        await Delete(GeographyVacancyRate).execute()
        await Delete(GeographySalaryProfession).execute()
        await Delete(GeographyVacancyRateProfession).execute()

        result = []

        for row in await cls.dynamics_salary_by_city():
            result.append({'city': row['area_name'], 'salary': row['salary_profession']})

        await Insert(GeographySalary).values(result).execute()

        result = []

        for row in await cls.dynamics_vacancies_by_city():
            result.append({'city': row['area_name'], 'vacancy_rate': row['vacancy_rate']})

        await Insert(GeographyVacancyRate).values(result).execute()

        result = []

        for row in await cls.dynamics_salary_by_city_with_profession():
            result.append({'city': row['area_name'], 'salary': row['salary_profession']})

        await Insert(GeographySalaryProfession).values(result).execute()

        result = []

        for row in await cls.dynamics_vacancies_by_city_with_profession():
            result.append({'city': row['area_name'], 'vacancy_rate': row['vacancy_rate']})

        await Insert(GeographyVacancyRateProfession).values(result).execute()


async def main():
    await Database.connect()
    await GeographyAnalytics.save_all()
    await Database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
