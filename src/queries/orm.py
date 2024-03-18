import random

from sqlalchemy import select, update, func, and_, cast, Integer

from src.database import sync_engine, async_engine, sync_session, async_session
from src.models import Model, Workers, Resumes, Workload

from faker import Faker

fake = Faker("en")


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

    @staticmethod
    def update_worker(worker_id: int = 1, new_username: str = "Test"):
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
        async with async_session(autoflush=True) as conn:
            worker1 = Workers(username="Jack", age=21)
            worker2 = Workers(username="John", age=45)
            worker3 = Workers(username="Johnson", age=34)
            conn.add_all([worker1, worker2, worker3])
            await conn.commit()

    @staticmethod
    async def select_data(workers=False, resumes=False):
        table = Workers if workers else Resumes if resumes else None
        if table is None:
            return
        async with async_session() as conn:
            query = select(table)
            result = await conn.execute(query)
            data = result.scalars().all()
            return data

    @staticmethod
    async def update_workers(worker_id: int = 1, new_username: str = "test_username"):
        async with async_session() as conn:
            stmt = update(Workers).values(username=new_username).filter_by(id=worker_id)
            await conn.execute(stmt)
            await conn.commit()

    # @staticmethod
    # async def update_worker(worker_id: int = 1, new_username: str = "test_username"):
    #     """Делает 2 запроса: 1 на получение, второй на обновление"""
    #     async with async_session() as conn:
    #         worker = await conn.get(Workers, worker_id)
    #         if worker:
    #             worker.username = new_username
    #         await conn.commit()

    @staticmethod
    async def insert_resumes():
        async with async_session() as conn:
            resumes = []
            for _ in range(20):
                title = random.choice(["Python", "Data_scientist"])
                compensation = random.randrange(100000, 300000, 10000)
                workload = random.choice(list(_ for _ in Workload))
                worker_id = random.randint(1, 3)
                resume = Resumes(
                    title=title,
                    compensation=compensation,
                    workload=workload,
                    worker_id=worker_id,
                )
                resumes.append(resume)
            conn.add_all(resumes)
            await conn.commit()

    @staticmethod
    async def custom_select():
        """
        Выбрать всех питонщиков, которые просят больше 100_000, разделить
        их по рабочей нагрузке, и вычислить среднюю зарплату по каждой рабочей нагрузке
        """
        async with async_session() as conn:
            query = (
                select(
                    Resumes.workload,
                    cast(func.avg(Resumes.compensation).label("avg"), Integer),
                )
                .filter(
                    and_(
                        Resumes.title.contains("Python"), Resumes.compensation > 100000
                    )
                )
                .group_by(Resumes.workload)
            )
            res = await conn.execute(query)
            print(res.all())
