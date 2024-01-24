from json import loads

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.methods.database import Select, Database
from core.models.analytics import Demand, GeographySalary, GeographyVacancyRate, GeographySalaryProfession, \
    GeographyVacancyRateProfession, KeySkillsTop, KeySkillsTopWithProfession
from modules.analytics.scripts.vacancies import Vacancies


@require_http_methods(["GET"])
def index(request):
    return render(request, 'html/index.html')


@require_http_methods(["GET"])
async def geography(request):
    await Database.connect()

    data1 = await (
        Select(GeographySalary.city, GeographySalary.salary)
        .order_by(GeographySalary.salary.desc())
        .fetch(model=tuple)
    )

    data2 = await (
        Select(GeographyVacancyRate.city, GeographyVacancyRate.vacancy_rate)
        .order_by(GeographyVacancyRate.vacancy_rate.desc())
        .fetch(model=tuple)
    )

    data3 = await (
        Select(GeographySalaryProfession.city, GeographySalaryProfession.salary)
        .order_by(GeographySalaryProfession.salary.desc())
        .fetch(model=tuple)
    )

    data4 = await (
        Select(GeographyVacancyRateProfession.city, GeographyVacancyRateProfession.vacancy_rate)
        .order_by(GeographyVacancyRateProfession.vacancy_rate.desc())
        .fetch(model=tuple)
    )

    await Database.disconnect()

    return render(request, 'html/geography.html', {'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4})


@require_http_methods(["GET"])
async def demand(request):
    await Database.connect()

    result = await (
        Select(Demand.year, Demand.salary, Demand.vacancies_count, Demand.salary_profession, Demand.vacancies_count_profession)
        .order_by(Demand.year)
        .fetch(model=tuple)
    )
    await Database.disconnect()

    return render(request, 'html/demand.html', {'data': result})


@require_http_methods(["GET"])
async def skills(request):
    await Database.connect()

    data = await (
        Select(KeySkillsTop.year, KeySkillsTop.data)
        .order_by(KeySkillsTop.year)
        .fetch()
    )

    cap1 = []

    for year, json_data in data:
        if loads(json_data)['data']:
            cap1.append(year)

    data1 = [['' for _ in range(len(cap1))] for _ in range(20)]

    index_y = 0
    for year, json_data in data:
        if not (data_ := loads(json_data)['data']):
            continue

        for index, row in enumerate(data_):
            data1[index][index_y] = f"{row['name'].encode('utf-8').decode('unicode-escape')}: {row['count']}"

        index_y +=1

    data = await (
        Select(KeySkillsTopWithProfession.year, KeySkillsTopWithProfession.data)
        .order_by(KeySkillsTopWithProfession.year)
        .fetch()
    )

    cap2 = []

    for year, json_data in data:
        if loads(json_data)['data']:
            cap2.append(year)

    data2 = [['' for _ in range(len(cap2))] for _ in range(20)]

    index_y = 0
    for year, json_data in data:
        if not (data_ := loads(json_data)['data']):
            continue

        for index, row in enumerate(data_):
            data2[index][index_y] = f"{row['name'].encode('utf-8').decode('unicode-escape')}: {row['count']}"

        index_y += 1

    await Database.disconnect()

    return render(request, 'html/skills.html', {'data1': data1, 'data2': data2, 'cap1': cap1, 'cap2': cap2})


@require_http_methods(["GET"])
async def vacancies(request):
    return render(request, 'html/vacancies.html', {'data': await Vacancies.get()})
