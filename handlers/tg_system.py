from aiogram.types import Message, InputFile
from aiogram.dispatcher import FSMContext
from settings import local_photo_path
from os.path import join


async def answer_and_finish(message: Message, text: str, state: FSMContext):
    await message.answer(text)
    await state.finish()


async def reply_and_finish(message: Message, text: str, state: FSMContext, kb=None):
    await message.reply(text, reply_markup=kb)
    await state.finish()


async def show_problem(message: Message, data: dict):

    s = "id: " + str(data["id"]) + \
        "\nname: " + str(data["name"]) + \
        "\ntext: " + str(data["text"]) + \
        "\ntags: " + str(data["tags"]) + "\n"

    await message.answer(s)

    if str(data["photo"]) != "nan":
        photo = InputFile(join(local_photo_path, data["name"] + ".jpg"))
        await message.answer_photo(photo)

    return
