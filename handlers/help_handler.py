from os.path import join
import random

from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from handlers.tg_system import answer_and_finish, reply_and_finish
from arg_parser.dict_parser import parse_dict
from controlling.object_controlling import server
from handlers.tg_system import show_problem

from settings import local_photo_path


async def help(message: Message):

    s = "Бот предназачен для cохранения задач в базе, которые затем бэкапятся на Я.Диск\n"
    s += "Существующие команды: \n\n"
    s += "/help - отобразить это сообщение\n"
    s += "\n"
    s += "/add - создать новую задачу в базе\n"
    s += "name: %sth%\n"
    s += "[tags: %sth%]\n"
    s += "[text: %sth%]\n"
    s += "[photo: ]\n"
    s += "[фото в следующем сообщение если был указан параметр photo:]\n"
    s += "\n"
    s += "/showtags или /tags или /alltags - отобразить все существующие теги\n"
    s += "\n"
    s += "/search или /show - поиск и отображение задач по заданным параметрам\n"
    s += "[name: %sth%}\n"
    s += "[tags: %sth%]\n"
    s += "[id: %sth%]\n"
    s += "(хотя бы один из этих параметров является обязательным, можно указать * для поиска по всем, f.e {id:*})\n"
    s += "\n"
    s += "/random - выдать случайную задачу из подмножества по тегам\n"
    s += "tags: %sthing%\n"
    s += "\n"
    s += "/delete - удалить задачу\n"
    s += "id: %sthing%\n"
    s += "\n"

    await message.reply(s)


def register_help(dp: Dispatcher):
    dp.register_message_handler(help, commands="help")
    dp.register_message_handler(help, commands="start")
