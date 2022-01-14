import asyncio
import logging
import time
from os.path import join

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.main_handler import register_all_handlers
from settings import local_log_path, log_file
from settings import formatter, date_format
from settings import tg_token


async def main():

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename=join(local_log_path, log_file),
        level=logging.INFO,
        format=formatter,
        datefmt=date_format
    )

    logger.info("Starting bot")

    bot = Bot(token=tg_token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_all_handlers(dp)

    while True:

        try:
            await dp.start_polling()

        except BaseException as e:
            logging.error(str(e))
            time.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
