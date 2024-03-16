from src.database import sync_engine, sync_session, async_engine
from src.models import Model, Workers


class SyncORM:

    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Model.metadata.drop_all(sync_engine)
        Model.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_data():
        with sync_session() as conn:
            worker1 = Workers(username="Jack", age=21)
            worker2 = Workers(username="John", age=45)
            worker3 = Workers(username="Johnson", age=34)
            conn.add_all([worker1, worker2, worker3])
            conn.commit()

    @staticmethod
    def select_workers():
        pass


class AsyncORM:

    @staticmethod
    async def create_tables():
        async_engine.echo = False
        async with async_engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)
            await conn.run_sync(Model.metadata.create_all)
        async_engine.echo = True

    @staticmethod
    async def insert_data():
        async with sync_session() as conn:
            worker1 = Workers(username="Jack", age=21)
            worker2 = Workers(username="John", age=45)
            worker3 = Workers(username="Johnson", age=34)
            conn.add_all([worker1, worker2, worker3])
            await conn.commit()

    @staticmethod
    async def select_workers():
        pass
