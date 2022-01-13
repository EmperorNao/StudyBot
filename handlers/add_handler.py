from os.path import join

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from handlers.tg_system import answer_and_finish, reply_and_finish
from arg_parser.dict_parser import parse_dict
from controlling.object_controlling import server

from settings import local_photo_path


class ProblemAdd(StatesGroup):
    waiting_for_problem = State()
    waiting_for_photo = State()


async def add_start(message: Message):

    await message.reply('Жду задачу')
    await ProblemAdd.next()


async def add_content(message: Message, state: FSMContext):

    try:
        data = parse_dict(message.text)
    except BaseException as e:
        await reply_and_finish(message, str(e), state)
        return

    if "name" not in data:
        await reply_and_finish(message, "У каждой задачи должно быть указано поле name", state)
        return

    await state.update_data(data=data)
    if "photo" in data:
        await message.reply("Ожидаю фото")
        await ProblemAdd.next()
        return

    server.save_object(data)
    await reply_and_finish(message, "Успешно добавил задачу", state)


async def add_photo(message: Message, state: FSMContext):

    if not len(message.photo):
        reply_and_finish(message, "Ожидалась фотография", state)
        return

    data = await state.get_data()
    await message.photo[-1].download(join(local_photo_path, data["name"] + ".jpg"))

    server.save_object(data)
    await reply_and_finish(message, "Успешно добавил задачу", state)


def register_add(dp: Dispatcher):
    dp.register_message_handler(add_start, commands="add", state="*")
    dp.register_message_handler(add_start, commands="new", state="*")
    dp.register_message_handler(add_content, state=ProblemAdd.waiting_for_problem)
    dp.register_message_handler(add_photo, content_types=['photo'], state=ProblemAdd.waiting_for_photo)
