import asyncio
from json import loads

from core.methods.database import Select, Database
from core.models.analytics import KeySkillsTop, KeySkillsTopWithProfession
from modules.graphics.scripts.config import vacancies_name
from modules.graphics.scripts.drawer import Drawer


async def main():
    await Database.connect()

    path_base = r'H:\DjangoProject\templates\skills'

    data = await (
        Select(KeySkillsTop.year, KeySkillsTop.data)
        .order_by(KeySkillsTop.year)
        .fetch()
    )

    for year, json_data in data:
        if not (data_ := loads(json_data)['data']):
            continue

        Drawer.draw_vertical_histogram(
            f'ТОП-20 навыков за {year} год',
            {row['name'].encode('utf-8').decode('unicode-escape'): row['count'] for row in data_},
            f'{path_base}\key_skills_{year}',
            tick_size=6
        )

    data = await (
        Select(KeySkillsTopWithProfession.year, KeySkillsTopWithProfession.data)
        .order_by(KeySkillsTopWithProfession.year)
        .fetch()
    )

    for year, json_data in data:
        if not (data_ := loads(json_data)['data']):
            continue

        Drawer.draw_vertical_histogram(
            f'ТОП-20 навыков за {year} год для {vacancies_name}',
            {row['name'].encode('utf-8').decode('unicode-escape'): row['count'] for row in data_},
            f'{path_base}\key_skills_profession_{year}',
            tick_size=6
        )

    await Database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
