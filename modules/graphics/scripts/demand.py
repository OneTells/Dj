import asyncio

from core.methods.database import Select, Database
from core.models.analytics import Demand
from modules.graphics.scripts.config import vacancies_name
from modules.graphics.scripts.drawer import Drawer


async def main():
    await Database.connect()

    path_base = r'H:\DjangoProject\templates\demand'

    data = await (
        Select(Demand.year, Demand.salary)
        .order_by(Demand.year)
        .fetch()
    )

    Drawer.draw_vertical_histogram(
        'Динамика уровня зарплат по годам',
        {year: salary for year, salary in data},
        f'{path_base}\salary_by_year',
    )

    data = await (
        Select(Demand.year, Demand.vacancies_count)
        .order_by(Demand.year)
        .fetch()
    )

    Drawer.draw_vertical_histogram(
        'Динамика количества вакансий по годам',
        {year: count for year, count in data},
        f'{path_base}\count_by_year',
    )

    data = await (
        Select(Demand.year, Demand.salary_profession)
        .order_by(Demand.year)
        .fetch()
    )

    Drawer.draw_vertical_histogram(
        f'Динамика уровня зарплат по годам для {vacancies_name}',
        {year: salary for year, salary in data},
        f'{path_base}\salary_by_year_profession',
    )

    data = await (
        Select(Demand.year, Demand.vacancies_count_profession)
        .order_by(Demand.year)
        .fetch()
    )

    Drawer.draw_vertical_histogram(
        f'Динамика количества вакансий по годам для {vacancies_name}',
        {year: count for year, count in data},
        f'{path_base}\count_by_year_profession',
    )

    await Database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
