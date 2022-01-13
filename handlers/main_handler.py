from aiogram import Dispatcher

from handlers.add_handler import register_add
from handlers.search_handler import register_search
from handlers.delete_handler import register_delete
from handlers.random_handler import register_random


def register_all_handlers(dp: Dispatcher):

    register_add(dp)
    register_search(dp)
    register_delete(dp)
    register_random(dp)
