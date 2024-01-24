import asyncio

from core.methods.database import Select, Database
from core.models.analytics import GeographySalary, GeographySalaryProfession, GeographyVacancyRate, GeographyVacancyRateProfession
from modules.graphics.scripts.config import vacancies_name
from modules.graphics.scripts.drawer import Drawer


async def main():
    await Database.connect()

    path_base = r'H:\DjangoProject\templates\geography'

    data = await (
        Select(GeographySalary.city, GeographySalary.salary)
        .order_by(GeographySalary.salary)
        .fetch()
    )

    Drawer.draw_horizontal_histogram(
        'Уровень зарплат по городам',
        {city.replace("-", '-\n').replace(" ", ' \n'): salary for city, salary in data},
        f'{path_base}\salary_by_city',
    )

    data = await (
        Select(GeographySalaryProfession.city, GeographySalaryProfession.salary)
        .order_by(GeographySalaryProfession.salary)
        .fetch()
    )

    Drawer.draw_horizontal_histogram(
        f'Уровень зарплат по городам для {vacancies_name}',
        {city.replace("-", '-\n').replace(" ", ' \n'): salary for city, salary in data},
        f'{path_base}\salary_by_city_profession',
    )

    data = await (
        Select(GeographyVacancyRate.city, GeographyVacancyRate.vacancy_rate)
        .order_by(GeographyVacancyRate.vacancy_rate)
        .fetch()
    )

    Drawer.draw_pie(
        'Доля вакансий по городам',
        {city: vacancy_rate for city, vacancy_rate in data} | {'Другие': 1 - sum([vacancy_rate for _, vacancy_rate in data])},
        f'{path_base}\\vacancy_rate_by_city',
    )

    data = await (
        Select(GeographyVacancyRateProfession.city, GeographyVacancyRateProfession.vacancy_rate)
        .order_by(GeographyVacancyRateProfession.vacancy_rate)
        .fetch()
    )

    Drawer.draw_pie(
        f'Доля вакансий по городам для {vacancies_name}',
        {city: vacancy_rate for city, vacancy_rate in data} | {'Другие': 1 - sum([vacancy_rate for _, vacancy_rate in data])},
        f'{path_base}\\vacancy_rate_city_profession',
    )

    await Database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
