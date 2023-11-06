import sqlite3 as sq
from typing import List

from aiogram.filters import Command
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from tbot1.data.database import cur
from tbot1.keyboards.for_cs import get_y_n_kb
from tbot1.data.database import db

router = Router()


class trainday:
    weekday: str
    exercise: str


class schedule:
    id: str
    train: List[trainday]


class schedule_create(StatesGroup):
    choose = State()
    id_fill = State()
    mon_fill = State()
    tue_fill = State()
    wed_fill = State()
    thu_fill = State()
    fri_fill = State()
    sat_fill = State()
    sun_fill = State()
    eo = State()


temp_list = []


@router.message(Command("create_schedule"))
async def instruction(message: Message, state: FSMContext):
    await message.answer('Приступим!\n'
                         'Вам предстоит внести в каждый день недели ваши упражнения\n'
                         'Если хотите отдохнуть - пишите "oтдых"\n'
                         '<b>Начнем?</b>', reply_markup=get_y_n_kb())
    await state.set_state(schedule_create.choose)


@router.message(
    schedule_create.choose,
    F.text.lower() == "нет"
)
async def stop_creating_schedule(message: Message, state: FSMContext):
    await message.answer(f'Хорошо, возвращайтесь к этому шагу, когда вам понадобится своё собственное расписание\n'
                         f'Чтобы получить уже готовое расписание, пишите <b>/get_schedule</b>', reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


@router.message(
    schedule_create.choose,
    F.text.lower() == "да!"
)
async def start_creating_schedule(message: Message, state: FSMContext):
    await message.answer('Приступим!\n'
                         'Сейчас вам надо будет ввести уникальный <b>ID</b> вашего будущего расписания', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(schedule_create.id_fill)


@router.message(
    schedule_create.id_fill
)
async def id_create(message: Message, state: FSMContext):
    try:
        global new_id
        new_id = message.text
        insert_id = ("INSERT INTO schedule"
                     "(id)"
                     "VALUES"
                     "(?)")
        cur.execute(insert_id, new_id)
        db.commit()
        await state.set_state(schedule_create.mon_fill)
        await message.answer('Отлично, <b>ID</b> свободно!\n'
                             'Теперь напишите текстом ваши тренировки в понедельник')

    except sq.Error as error:
        await message.answer(f'Этот <b>ID</b> уже занят\n'
                             f'Попробуйте снова)\n'
                             f'{error}')
        await state.set_state(schedule_create.choose)


@router.message(
    schedule_create.mon_fill
)
async def mon_create(message: Message, state: FSMContext):
    global mon
    mon = message.text
    await message.answer('Супер!\n'
                         'Напишите текстом ваши тренировки во вторник')
    await state.set_state(schedule_create.tue_fill)


@router.message(
    schedule_create.tue_fill
)
async def tue_create(message: Message, state: FSMContext):
    global tue
    tue = message.text
    await message.answer('Супер!\n'
                         'Напишите текстом ваши тренировки в среду')
    await state.set_state(schedule_create.wed_fill)


@router.message(
    schedule_create.wed_fill
)
async def wed_create(message: Message, state: FSMContext):
    global wed
    wed = message.text
    await message.answer('Супер!\n'
                         'Напишите текстом ваши тренировки четверг')
    await state.set_state(schedule_create.thu_fill)


@router.message(
    schedule_create.thu_fill
)
async def thu_create(message: Message, state: FSMContext):
    global thu
    thu = message.text
    await message.answer('Супер!\n'
                         'Напишите текстом ваши тренировки в пятницу')
    await state.set_state(schedule_create.fri_fill)


@router.message(
    schedule_create.fri_fill
)
async def fri_create(message: Message, state: FSMContext):
    global fri
    fri = message.text
    await message.answer('Супер!\n'
                         'Напишите текстом ваши тренировки в субботу')
    await state.set_state(schedule_create.sat_fill)


@router.message(
    schedule_create.sat_fill
)
async def sat_create(message: Message, state: FSMContext):
    global sat
    sat = message.text
    await message.answer('Супер!\n'
                         'Напишите текстом ваши тренировки в воскресение')
    await state.set_state(schedule_create.sun_fill)


@router.message(
    schedule_create.sun_fill
)
async def sun_create(message: Message, state: FSMContext):
    sun = message.text
    insert_schedule = ("INSERT OR REPLACE INTO schedule"
                       "(id, mon, tue, wed, thu, fri, sat, sun)"
                       "VALUES"
                       "(?, ?, ?, ?, ?, ?, ?, ?)")
    insert_values = [new_id, mon, tue, wed, thu, fri, sat, sun]
    cur.execute(insert_schedule, insert_values)
    db.commit()
    await message.answer('Это успех!\n'
                         'Ваше расписание готово!')
    await state.set_state(schedule_create.tue_fill)
    await state.clear()
