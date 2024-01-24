from datetime import datetime
from inspect import isclass
from typing import Any, Callable, overload, TypeVar

from asyncpg import Pool, create_pool, Record
from pydantic import BaseModel
from sqlalchemy import Update as _Update, Select as _Select, Insert as _Insert, Delete as _Delete
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import CompileError
from sqlalchemy.sql._typing import _ColumnsClauseArgument

from core.config import DatabaseInfo
from core.methods.logger import logger

T = TypeVar('T', bound=BaseModel)
T1 = TypeVar('T1')

Query = _Select | _Update | _Insert | _Delete
Model = type[T] | Callable[[Any], T1] | None


class Select(_Select):

    @overload
    async def fetch(self, *, model: Callable[[Any], T1]) -> list[T1]:
        ...

    @overload
    async def fetch(self, *, model: type[T]) -> list[T]:
        ...

    @overload
    async def fetch(self, *, model: None = None) -> list[Record]:
        ...

    async def fetch(self, *, model: Model = None) -> list[Record | T1 | T]:
        return await Database.fetch(self, model=model)

    @overload
    async def fetch_one(self, *, model: type[T]) -> T | None:
        ...

    @overload
    async def fetch_one(self, *, model: Callable[[Any], T1]) -> T1 | None:
        ...

    @overload
    async def fetch_one(self, *, model: None = None) -> Record | None:
        ...

    async def fetch_one(self, *, model: Model = None) -> Record | T1 | T | None:
        return await Database.fetch_one(self, model=model)


class Update(_Update):

    async def execute(self) -> None:
        await Database.execute(self)


class Insert(_Insert):

    async def execute(self) -> None:
        await Database.execute(self)

    @overload
    async def returning(self, *cols: _ColumnsClauseArgument[Any], model: Callable[[Any], T1]) -> T1 | None:
        ...

    @overload
    async def returning(self, *cols: _ColumnsClauseArgument[Any], model: type[T]) -> T | None:
        ...

    @overload
    async def returning(self, *cols: _ColumnsClauseArgument[Any], model: None = None) -> Record | None:
        ...

    async def returning(self, *cols: _ColumnsClauseArgument[Any], model: Model = None) -> Record | T1 | T | None:
        return await Database.fetch_one(super().returning(*cols), model=model)


class Delete(_Delete):

    async def execute(self) -> None:
        await Database.execute(self)


class Database:
    __pool: Pool = None

    @classmethod
    async def connect(cls):
        cls.__pool = await create_pool(
            DatabaseInfo.DSN,
            max_inactive_connection_lifetime=3,
            min_size=1, max_size=1
        )

        logger.info('База данных подключена')

    @classmethod
    async def disconnect(cls):
        await cls.__pool.close()
        logger.info('База данных отключена')

    @classmethod
    async def fetch(cls, query: Query, *, model: Model = None) -> list[Record | T1 | T]:
        result = await cls.__pool.fetch(cls.query(query))

        if model is None:
            return result

        if isclass(model) and issubclass(model, BaseModel):
            return list(map(lambda record: model.model_validate(dict(record)), result))

        return list(map(model, result))

    @classmethod
    async def fetch_one(cls, query: Query, *, model: Model = None) -> Record | T1 | T | None:
        return response[0] if (response := await cls.fetch(query, model=model)) else None

    @classmethod
    async def execute(cls, query: Query) -> None:
        await cls.__pool.execute(cls.query(query))

    @staticmethod
    def __text_processing(value: Any) -> Any:
        if isinstance(value, (str, datetime)):
            if isinstance(value, str):
                value = value.replace("'", "''")

            return f"'{value}'"

        return value

    @classmethod
    def __query_incomplete_processing(cls, query: Select) -> str:
        query_compiled = query.compile(dialect=postgresql.dialect(), compile_kwargs={"render_postcompile": True})
        logger.debug(
            response := str(query_compiled) % {key: cls.__text_processing(value) for key, value in query_compiled.params.items()}
        )

        return response

    @classmethod
    def query(cls, query: Query) -> str:
        try:
            response = str(query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        except CompileError:
            logger.error('Ошибка компиляции в бд')
            logger.error(f'{str(query)}')
            logger.exception()

            response = cls.__query_incomplete_processing(query)

        logger.debug(response)
        return response
