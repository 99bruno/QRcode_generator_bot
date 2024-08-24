import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv

from app.handlers import register_all_handlers


async def main() -> None:
    """
    Main function to start the bot

    :logic: Load the environment variables, create the bot and dispatcher instances, and start the bot

    :return: None

    :raises: None
    """

    load_dotenv()

    bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(register_all_handlers())

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Successfully Exit, Bot is Stopped")
