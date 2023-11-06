import asyncio
import logging
from typing import List

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from data import database as db
from tbot1.handlers import gs, cs
from tbot1token import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=bot)
dp.include_routers(gs.router, cs.router)


async def on_startup(_):
    await db.db_start()


class trainday:
    weekday: str
    exercise: str


class schedule:
    id: str
    train: List[trainday]


@dp.message(Command("start"))
async def welcome(message: Message) -> None:
    await message.answer("<b>Привет!</b>\n"
                         "Здесь ты найдешь своё <i>расписание тренировок</i>)\n"
                         "Начнем?\n"
                         "Пиши <b>/get_schedule</b> для получения расписания!\n"
                         "Чтобы составить свое расписание, пиши <b>/create_schedule</b>")


@dp.message(Command("change_schedule"))
async def change_schedule():
    pass


async def main():
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == "__main__":
    asyncio.run(main())
