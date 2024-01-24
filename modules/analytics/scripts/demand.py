import asyncio

from sqlalchemy.sql.functions import count, func


from core.methods.database import Select, Database, Insert, Delete
from core.models.analytics import Demand
from core.models.vacancies import Vacancies
from modules.analytics.scripts.config import profession_pattern


class DemandAnalytics:

    @staticmethod
    async def dynamics_by_year():
        return await (
            Select(
                Vacancies.year,
                (func.round(func.avg(Vacancies.salary))).label('salary'),
                count().label('vacancies_count')
            )
            .where(Vacancies.salary < 10_000_000)
            .group_by(Vacancies.year)
            .order_by(Vacancies.year)
            .fetch()
        )

    @staticmethod
    async def dynamics_by_year_with_profession():
        return await (
            Select(
                Vacancies.year,
                (func.round(func.avg(Vacancies.salary))).label('salary_profession'),
                count().label('vacancies_count_profession')
            )
            .where(Vacancies.salary < 10_000_000, Vacancies.name.regexp_match(profession_pattern, flags='i'))
            .group_by(Vacancies.year)
            .order_by(Vacancies.year)
            .fetch()
        )

    @classmethod
    async def save_all(cls):
        await Delete(Demand).execute()

        years: list[int] = await (
            Select(Vacancies.year.distinct())
            .order_by(Vacancies.year)
            .fetch(model=lambda x: x[0])
        )

        storage = {
            year: {'year': int(year), 'salary': 0, 'vacancies_count': 0, 'salary_profession': 0, 'vacancies_count_profession': 0}
            for year in years
        }

        for row in await cls.dynamics_by_year():
            storage[row['year']]['salary'] = int(row['salary'])
            storage[row['year']]['vacancies_count'] = row['vacancies_count']

        for row in await cls.dynamics_by_year_with_profession():
            storage[row['year']]['salary_profession'] = int(row['salary_profession'])
            storage[row['year']]['vacancies_count_profession'] = row['vacancies_count_profession']

        await Insert(Demand).values([row for row in storage.values()]).execute()


async def main():
    await Database.connect()
    await DemandAnalytics.save_all()
    await Database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
