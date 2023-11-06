from typing import List

from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import sqlite3 as sq

from tbot1.data.database import cur

router = Router()


class trainday:
    weekday: str
    exercise: str


class schedule:
    id: str
    train: List[trainday]


class schedule_get(StatesGroup):
    choosing_schedule_id = State()


@router.message(Command("get_schedule"))
async def hello_get_schedule(message: Message, state: FSMContext):
    await message.answer("Введите <b>ID</b> Вашего расписания")
    await state.set_state(schedule_get.choosing_schedule_id)


@router.message(
    schedule_get.choosing_schedule_id
)
async def get_schedule(message: Message, state: FSMContext):
    try:
        s_id = message.text
        cur.execute(f"SELECT * FROM schedule WHERE id={s_id}")
        i, mon, tue, wed, thu, fri, sat, sun = cur.fetchone()
        await message.answer(f"<b>Вот Ваше расписание</b> <i>(Обязательно запомните его ID)</i>\n"
                             f"<b>ID</b> расписания: <i>{i}</i>\n"
                             f"<b>Понедельник</b>: {mon}\n"
                             f"<b>Вторник</b>: {tue}\n"
                             f"<b>Среда</b>: {wed}\n"
                             f"<b>Четверг</b>: {thu}\n"
                             f"<b>Пятница</b>: {fri}\n"
                             f"<b>Суббота</b>: {sat}\n"
                             f"<b>Воскресенье</b>: {sun}\n")
        await state.clear()
    except sq.Error:
        await message.answer("Расписания с такими <b>ID</b> не существует :/")

