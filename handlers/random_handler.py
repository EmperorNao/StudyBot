from os.path import join
import random

from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from handlers.tg_system import answer_and_finish, reply_and_finish
from arg_parser.dict_parser import parse_dict
from controlling.object_controlling import server
from handlers.tg_system import show_problem

from settings import local_photo_path


class ProblemRandom(StatesGroup):
    waiting_for_info = State()


async def random_start(message: Message):

    await message.reply('Жду теги задачи для выбора случайной')
    await ProblemRandom.next()


async def random_content(message: Message, state: FSMContext):

    try:
        data = parse_dict(message.text)
    except BaseException as e:
        await reply_and_finish(message, str(e), state)
        return

    if "tags" not in data:
        await reply_and_finish(message, "Для выбора случайной задачи обязательно указывать теги", state)
        return

    collection = server.get_by_query(data)
    if not len(collection):
        await answer_and_finish(message, "По данным тегам не было найдено ни одной задачи", state)
        return

    random.seed()
    index = random.randint(0, len(collection) - 1)
    await message.reply("Случайная задача:")
    await show_problem(message, collection.iloc[index])

    await state.finish()


def register_random(dp: Dispatcher):
    dp.register_message_handler(random_start, commands="random", state="*")
    dp.register_message_handler(random_content, state=ProblemRandom.waiting_for_info)
