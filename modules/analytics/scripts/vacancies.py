import asyncio
import re
from asyncio import sleep
from datetime import datetime
from json import loads
from pprint import pprint

from aiohttp import ClientSession, ClientOSError, ClientConnectorError, ContentTypeError

from core.methods.logger import logger
from modules.analytics.scripts.config import profession_search_pattern


class API:
    __session: ClientSession | None = None

    @classmethod
    async def get(cls, url: str, params: dict = None) -> bytes:
        if not cls.__session:
            cls.__session = ClientSession()

        try:
            async with cls.__session.get(url, headers={}, cookies={}, params=params) as response:
                return await response.read()
        except (ClientOSError, TimeoutError, asyncio.TimeoutError, ClientConnectorError, ContentTypeError):
            logger.error(f'Ошибка получения картинки | {url}')
            raise ValueError()

    @classmethod
    async def close(cls):
        await cls.__session.close()
        cls.__session = None


class Vacancies:

    @staticmethod
    def get_salary(salary_from: int | None, salary_to: int | None, currency: str):
        salary = []

        if salary_from is not None:
            salary.append(salary_from)

        if salary_to is not None:
            salary.append(salary_to)

        return f"{int(sum(salary) / len(salary))} {currency}"

    @classmethod
    async def get(cls) -> list[list[str]]:
        response = await API.get(
            "https://api.hh.ru/vacancies", params={"text": profession_search_pattern, "period": "1", "per_page": 10}
        )

        if (elements := loads(response).get("items", None)) is None:
            return []

        vacancies = []

        for vacancy in elements:
            vacancy_data = loads(await API.get(f"https://api.hh.ru/vacancies/{vacancy['id']}"))

            vacancies.append(
                [
                    vacancy["name"],
                    (re.sub(re.compile('<.*?>'), '', vacancy_data["description"])).replace('&quot;', ''),
                    ", ".join(skill.get("name") for skill in vacancy_data.get("key_skills", [])) or 'Неуказанны',
                    vacancy["employer"]["name"],
                    cls.get_salary(vacancy["salary"]["from"], vacancy["salary"]["to"], vacancy["salary"]["currency"])
                    if vacancy["salary"] is not None else 'Неизвестно',
                    vacancy["area"]["name"],
                    datetime.strptime(vacancy["published_at"], r"%Y-%m-%dT%H:%M:%S%z").strftime(r"%H:%M %d.%m.%Y"),
                    f'https://hh.ru/vacancy/{vacancy["id"]}'
                ]
            )
        await API.close()
        await sleep(0.1)
        return sorted(vacancies, key=lambda x: x[-2])


async def main():
    pprint(res := await Vacancies.get())
    print(len(res))

    await API.close()
    await sleep(0.1)


if __name__ == '__main__':
    asyncio.run(main())
