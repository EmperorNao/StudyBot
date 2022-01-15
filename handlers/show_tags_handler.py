from os.path import join

from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from handlers.tg_system import answer_and_finish, reply_and_finish
from arg_parser.dict_parser import parse_dict
from controlling.object_controlling import server
from handlers.tg_system import show_problem

from settings import local_photo_path


async def show_tags(message: Message):

    tags = server.get_all_tags()
    if not tags:
        await message.reply("Не было найдени ни одного тега")

    else:

        await message.reply("Теги: " + ", ".join(list(tags)))

    return


def register_show_tags(dp: Dispatcher):
    dp.register_message_handler(show_tags, commands="tags")
    dp.register_message_handler(show_tags, commands="showtags")
    dp.register_message_handler(show_tags, commands="alltags")
