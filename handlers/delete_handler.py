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


class ProblemDelete(StatesGroup):
    waiting_for_info = State()
    waiting_for_checking = State()


async def delete_start(message: Message):

    await message.reply('Жду id задачи для удаления')
    await ProblemDelete.next()


async def delete_content(message: Message, state: FSMContext):

    try:
        data = parse_dict(message.text)
    except BaseException as e:
        await reply_and_finish(message, str(e), state)
        return

    if "id" not in data or not data["id"].isnumeric():
        await reply_and_finish(message, "Для удаления задачи обязательно указывать один id", state)
        return

    collection = server.get_by_query(data)
    if not len(collection):
        await answer_and_finish(message, "По данному запросы не было найдено ни одной задачи", state)
        return
    if len(collection) != 1:
        await answer_and_finish(message, "Было найдено больше чем одна задача, ошибка!", state)
        return

    await message.reply("Найденая задача:")
    for index, row in collection.iterrows():
        await show_problem(message, row)

    await state.update_data(data=data)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.answer("Вы действительно хотите удалить данную задачу?", reply_markup=keyboard)
    await ProblemDelete.next()


async def delete_check(message: Message, state: FSMContext):

    keyboard = ReplyKeyboardRemove()

    data = await state.get_data()
    if message.text == "Нет":
        await reply_and_finish(message, "Не удаляю задачу", state, keyboard)

    elif message.text == "Да":
        await message.reply("Удаляю задачу", reply_markup=keyboard)

        server.delete_object(data["id"])
        await reply_and_finish(message, "Успешно удалил задачу", state, keyboard)

    else:
        await reply_and_finish(message, "Не понял команду", state, keyboard)


def register_delete(dp: Dispatcher):
    dp.register_message_handler(delete_start, commands="delete", state="*")
    dp.register_message_handler(delete_start, commands="remove", state="*")
    dp.register_message_handler(delete_content, state=ProblemDelete.waiting_for_info)
    dp.register_message_handler(delete_check, state=ProblemDelete.waiting_for_checking)
