import asyncio
from datetime import datetime
from math import isnan

import pandas as pd

from core.methods.database import Database, Insert, Delete
from core.models.vacancies import Vacancies


async def main():
    await Database.connect()

    await Delete(Vacancies).execute()

    for dataframe in pd.read_csv(r'H:\DjangoProject\modules\analytics\data\vacancies_with_formatting_salary.csv', chunksize=10_000):
        result = []

        for _, row in dataframe.iterrows():
            result.append(
                {
                    'name': row['name'], 'area_name': row['area_name'],
                    'year': datetime.fromtimestamp(row['published_at']).year,
                    'key_skills': None if not isinstance(row['key_skills'], str) else row['key_skills'],
                    'salary': None if isnan(row['salary']) else row['salary']
                }
            )

        await Insert(Vacancies).values(result).execute()

    await Database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
