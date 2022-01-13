from os.path import join

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from handlers.tg_system import answer_and_finish, reply_and_finish, show_problem
from arg_parser.dict_parser import parse_dict
from controlling.object_controlling import server

from settings import local_photo_path


class ProblemSearch(StatesGroup):
    waiting_for_info = State()


async def search_start(message: Message):

    await message.reply('Жду запрос для поиска')
    await ProblemSearch.next()


async def search_content(message: Message, state: FSMContext):

    try:
        data = parse_dict(message.text)
    except BaseException as e:
        await reply_and_finish(message, str(e), state)
        return

    if "name" not in data and "id" not in data and "tags" not in data:
        await reply_and_finish(message, "В запросе должно быть указано хотя бы одно из полей: id, name, tags", state)
        return

    await message.reply("Отображаю найденные задачи")
    collection = server.get_by_query(data)
    for index, row in collection.iterrows():
        await show_problem(message, row)
    if not len(collection):
        await answer_and_finish(message, "По данному запросы не было найдено ни одной задачи", state)

    await state.finish()


def register_search(dp: Dispatcher):
    dp.register_message_handler(search_start, commands="search", state="*")
    dp.register_message_handler(search_start, commands="show", state="*")
    dp.register_message_handler(search_content, state=ProblemSearch.waiting_for_info)
