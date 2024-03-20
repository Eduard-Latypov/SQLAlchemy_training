import asyncio
import os
import sys

from queries.core import SyncCore, AsyncCore
from queries.orm import SyncORM, AsyncORM
from database import sync_engine, async_engine
from config import settings

sys.path.insert(1, os.path.join(sys.path[0], ".."))


# if __name__ == "__main__":
#     SyncCore.create_tables()
#     SyncCore.insert_data()
#     SyncCore.update_worker(worker_id=2, new_username="Test_name")
#     print(SyncCore.select_workers())


async def async_main():
    await AsyncORM.create_tables()
    await AsyncORM.insert_data()
    await AsyncORM.insert_resumes()
    # await AsyncORM.update_workers(worker_id=10, new_username="Eddy")
    res = await AsyncORM.select_data(resumes=True)
    for item in res:
        print(
            f"{item.id}: {item.title} {item.compensation} {item.workload} {item.worker_id}"
        )
    # await AsyncORM.custom_select()
    await AsyncORM.selectin_workers_with_resumes()
    dto = await AsyncORM.worker_to_dto()
    print(dto)
    print(settings.async_url)


if __name__ == "__main__":
    asyncio.run(async_main())
