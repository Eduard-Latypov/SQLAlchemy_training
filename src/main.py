import asyncio

from queries.core import sync_create_tables, async_create_tables
from database import sync_engine, async_engine


if __name__ == "__main__":
    sync_create_tables(sync_engine)


# async def async_main():
#     await async_create_tables(async_engine)
#
#
# if __name__ == "__main__":
#     asyncio.run(async_main())
