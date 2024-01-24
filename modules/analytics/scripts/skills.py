import asyncio
from collections import Counter
from json import dumps

from sqlalchemy import null


from core.methods.database import Database, Select, Insert, Delete
from core.models.analytics import KeySkillsTopWithProfession, KeySkillsTop
from core.models.vacancies import Vacancies
from modules.analytics.scripts.config import profession_pattern


class SkillsAnalytics:

    @staticmethod
    async def top_20_by_year():
        years: list[int] = await (
            Select(Vacancies.year.distinct())
            .order_by(Vacancies.year)
            .fetch(model=lambda x: x[0])
        )

        result = {}

        for year in years:
            key_skills: list[str] = await (
                Select(Vacancies.key_skills)
                .where(
                    Vacancies.salary < 10_000_000, Vacancies.year.__eq__(year),
                    Vacancies.key_skills.is_not(null())
                ).fetch(model=lambda x: x[0])
            )

            counter = Counter()

            for key_skill in key_skills:
                counter.update(Counter(key_skill.split('\n')))

            result.update({int(year): [{'name': name, 'count': count} for name, count in counter.most_common(20)]})

        return result

    @staticmethod
    async def top_20_by_year_with_profession() -> dict[int, list[dict[str, str | int]]]:
        years: list[int] = await (
            Select(Vacancies.year.distinct())
            .order_by(Vacancies.year)
            .fetch(model=lambda x: x[0])
        )

        result = {}

        for year in years:
            key_skills: list[str] = await (
                Select(Vacancies.key_skills)
                .where(
                    Vacancies.salary < 10_000_000, Vacancies.year.__eq__(year),
                    Vacancies.key_skills.is_not(null()), Vacancies.name.regexp_match(profession_pattern, flags='i')
                ).fetch(model=lambda x: x[0])
            )

            counter = Counter()

            for key_skill in key_skills:
                counter.update(Counter(key_skill.split('\n')))

            result.update({int(year): [{'name': name, 'count': count} for name, count in counter.most_common(20)]})

        return result

    @classmethod
    async def save_all(cls):
        await Delete(KeySkillsTop).execute()
        await Delete(KeySkillsTopWithProfession).execute()

        result = []

        for year, data in (await cls.top_20_by_year()).items():
            result.append({'year': year, 'data': dumps({'data': data})})

        await Insert(KeySkillsTop).values(result).execute()

        result = []

        for year, data in (await cls.top_20_by_year_with_profession()).items():
            result.append({'year': year, 'data': dumps({'data': data})})

        await Insert(KeySkillsTopWithProfession).values(result).execute()


async def main():
    await Database.connect()
    await SkillsAnalytics.save_all()
    await Database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
