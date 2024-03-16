import asyncio

from queries.core import SyncCore, AsyncCore
from database import sync_engine, async_engine


# if __name__ == "__main__":
#     SyncCore.create_tables()
#     SyncCore.insert_data()
#     print(SyncCore.select_workers())


async def async_main():
    await AsyncCore.create_tables()
    await AsyncCore.insert_data()
    print(await AsyncCore.select_workers())


if __name__ == "__main__":
    asyncio.run(async_main())
