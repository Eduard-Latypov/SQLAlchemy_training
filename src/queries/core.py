import asyncio

from sqlalchemy import insert, select, update

from src.models import workers_table, metadata, Base, Workers, Resumes
from src.database import sync_engine, async_engine, sync_session, async_session


# Synchronous
class SyncCore:

    @staticmethod
    def create_tables():
        sync_engine.echo = True
        metadata.drop_all(sync_engine)
        metadata.create_all(sync_engine)

    @staticmethod
    def insert_data():
        with sync_engine.connect() as conn:
            smtm = insert(workers_table).values(
                [
                    {"username": "Pavel", "age": 27},
                    {"username": "Ivan", "age": 28},
                    {"username": "Misha", "age": 29},
                    {"username": "Oleg", "age": 21},
                ]
            )
            conn.execute(smtm)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table)  # SELECT * FROM workers
            result = conn.execute(query)
            workers = result.all()
            return workers

    @staticmethod
    def update_worker(worker_id: int = 1, new_username: str = "Alhimiya"):
        with sync_engine.connect() as conn:
            smtm = (
                update(workers_table)
                .values(username=new_username)
                .filter_by(id=worker_id)
            )
            conn.execute(smtm)
            conn.commit()


# Asynchronous
class AsyncCore:

    @staticmethod
    async def create_tables():
        async_engine.echo = True
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)

    @staticmethod
    async def insert_data():
        async with async_engine.connect() as conn:
            smtm = insert(workers_table).values(
                [
                    {"username": "Pavel", "age": 27},
                    {"username": "Ivan", "age": 28},
                    {"username": "Misha", "age": 29},
                    {"username": "Oleg", "age": 21},
                ]
            )
            await conn.execute(smtm)
            await conn.commit()

    @staticmethod
    async def select_workers():
        async with async_engine.connect() as conn:
            query = select(workers_table)
            result = await conn.execute(query)
            workers = result.all()
            return workers

    @staticmethod
    async def update_worker(worker_id: int = 1, new_username: str = "test_username"):
        async with async_session() as conn:
            query = (
                update(Workers).values(username=new_username).filter_by(id=worker_id)
            )
            await conn.execute(query)
            await conn.commit()
