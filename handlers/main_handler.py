from aiogram import Dispatcher
from handlers.add_handler import register_add
from handlers.search_handler import register_search


def register_all_handlers(dp: Dispatcher):

    register_add(dp)
    register_search(dp)
