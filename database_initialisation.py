from crud import crud_instance
import asyncio

"""данный файл создает таблицу users в базе данных"""

asyncio.run(crud_instance.create_table())
