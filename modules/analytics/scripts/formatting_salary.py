from csv import DictWriter
from datetime import datetime
from math import isnan
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import pandas as pd
import requests
from pandas import Series


class ExchangeStorage:
    __URL = "https://www.cbr.ru/scripts/XML_daily.asp"

    __storage: dict[tuple[int, int], dict[str, float]] = {}

    @classmethod
    def __get_exchange_from_api(cls, month: int, year: int) -> list[Element]:
        response = requests.get(
            cls.__URL, params={'date_req': f'01/{month if month > 9 else "0" + str(month)}/{year}'}
        )

        return ElementTree.fromstring(response.content).findall('Valute')

    @classmethod
    def get(cls, month: int, year: int, currency: str) -> float | None:
        if (exchange := cls.__storage.get((month, year), None)) is not None:
            return exchange.get(currency, None)

        print(month, year)

        result: dict[str, float] = {}

        for element in cls.__get_exchange_from_api(month, year):
            result |= {element.find('CharCode').text: round(float(element.find('VunitRate').text.replace(',', '.')), 5)}

        cls.__storage.update({(month, year): result})

        return result.get(currency, None)


class Converter:

    @staticmethod
    def __formatting_vacancy(row: Series) -> Series:
        salaries = []
        salary = ''

        if not isnan(row['salary_to']):
            salaries.append(row['salary_to'])

        if not isnan(row['salary_from']):
            salaries.append(row['salary_from'])

        date = datetime.strptime(row['published_at'], r"%Y-%m-%dT%H:%M:%S%z")

        if salaries:
            exchange_rate = ExchangeStorage.get(
                date.month, date.year, row['salary_currency']
            ) if row['salary_currency'] != 'RUR' else 1

            if exchange_rate is not None:
                salary = int(sum(salaries) * exchange_rate / len(salaries))

        return Series(
            dict(
                name=' '.join(row['name'].split()), salary=salary, area_name=' '.join(row['area_name'].split()),
                key_skills='' if not isinstance(row['key_skills'], str) else row['key_skills'], published_at=int(date.timestamp())
            )
        )

    @classmethod
    def run(cls):
        with open(r'H:\DjangoProject\modules\analytics\data\vacancies_with_formatting_salary.csv', 'w', newline='', encoding="utf-8") as file:
            writer = DictWriter(file, fieldnames=['name', 'key_skills', 'salary', 'area_name', 'published_at'])
            writer.writeheader()

            for dataframe in pd.read_csv(r'H:\DjangoProject\modules\analytics\data\vacancies.csv', chunksize=100_000):
                writer.writerows(dataframe.apply(cls.__formatting_vacancy, axis=1).to_dict('records'))


if __name__ == '__main__':
    Converter.run()
