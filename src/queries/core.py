import asyncio

from src.models import Model


# Synchronous
def sync_create_tables(engine):
    engine.echo = True
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)


# Asynchronous
async def async_create_tables(async_engine):
    async_engine.echo = True
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
