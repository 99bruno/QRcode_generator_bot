from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.client.bot import Bot
from aiogram.types import FSInputFile
from aiogram.filters import Command

from app.templates.generate_qr import *

from app.keyboards.generate_qr import *

from app.states.generate_qr import GenerateQr

from app.scripts.generate_qr import generate_qr_code_with_logo, generate_qr_code

router = Router()


@router.message(Command("start"))
async def command_generate_qr_handler(message: types.Message) -> None:
    """
    Command generate qr handler

    :param message: telegram types Message

    :return: None

    :raises: None
    """

    await message.answer(generate_qr_message, reply_markup=generate_qr_keyboard)


@router.message(F.text == "Generate qr code with logo 🖼")
async def command_generate_qr_with_logo_handler(message: types.Message, state: FSMContext) -> None:
    """
    Command generate qr with logo handler

    :param message: telegram types Message
    :param state: telegram FSMContext

    :return: None

    :raises: None
    """

    await state.set_state(GenerateQr.photo_file)

    await message.answer(generate_qr_with_logo_message, reply_markup=types.ReplyKeyboardRemove())


@router.message(F.text == "Generate qr code without logo 📝")
async def command_generate_qr_without_logo_handler(message: types.Message, state: FSMContext) -> None:
    """
    Command generate qr without logo handler

    :param message: telegram types Message
    :param state: telegram FSMContext

    :return: None

    :raises: None
    """

    await state.set_state(GenerateQr.qr_text)

    await message.answer(generate_qr_without_logo_message, reply_markup=types.ReplyKeyboardRemove())


@router.message(GenerateQr.photo_file, F.content_type.in_([types.ContentType.PHOTO, types.ContentType.DOCUMENT]))
async def command_generate_qr_with_logo_handler(message: types.Message, state: FSMContext) -> None:
    """
    Command generate qr with logo handler that receives photo or document

    :param message: telegram types Message
    :param state: telegram FSMContext

    :return: None

    :raises: None
    """

    if message.content_type == types.ContentType.PHOTO:
        file_id = message.photo[-1].file_id
        border_size = 2
    elif message.content_type == types.ContentType.DOCUMENT:
        file_id = message.document.file_id
        border_size = 0
    else:
        await message.answer("Please send a valid photo or document.")
        return

    await state.update_data(photo_file=file_id, border_size=border_size)

    await message.answer(generate_qr_with_logo_text_message)
    await state.set_state(GenerateQr.qr_text)


@router.message(GenerateQr.qr_text, F.text)
async def command_generate_qr_with_logo_handler(message: types.Message, state: FSMContext, bot: Bot) -> None:
    """
    Command generate qr with logo handler that receives text

    :param message: telegram types Message
    :param state: telegram FSMContext
    :param bot: telegram Bot

    :return: None

    :raises: None
    """

    data = await state.get_data()
    if not data.get("photo_file"):
        qr_code_path = await generate_qr_code(message.text)
    else:
        qr_code_path = await generate_qr_code_with_logo(bot, message.text, data.get("photo_file"),
                                                        data.get("border_size"))

    await message.answer_photo(FSInputFile(qr_code_path), caption=generate_qr_confirmation_message,
                               reply_markup=generate_qr_keyboard)

    await state.clear()

