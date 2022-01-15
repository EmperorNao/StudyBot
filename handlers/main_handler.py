from aiogram import Dispatcher

from handlers.add_handler import register_add
from handlers.search_handler import register_search
from handlers.delete_handler import register_delete
from handlers.random_handler import register_random
from handlers.help_handler import register_help
from handlers.show_tags_handler import register_show_tags


def register_all_handlers(dp: Dispatcher):

    register_add(dp)
    register_search(dp)
    register_delete(dp)
    register_random(dp)
    register_help(dp)
    register_show_tags(dp)
