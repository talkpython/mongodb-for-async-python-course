import beanie
import motor.motor_asyncio

import models


async def init_connection(db_name: str):
    conn_str = f"mongodb://localhost:27017/{db_name}"
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)

    await beanie.init_beanie(database=client[db_name], document_models=models.all_models)

    print(f"Connected to {db_name}.")
