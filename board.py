from datetime import datetime
from db import get_session, Record

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


time_list = [
    "13:00",
    "13:40",
    "14:20",
    "15:00",
    "15:40",
    "16:20",
    "17:00",
]


class ChooseDateState(StatesGroup):
    day = State()
    time = State()
    who = State()
    aim = State()


def day_table(day):

    keyboard = InlineKeyboardMarkup()

    day_time_list = time_list.copy()

    day_records = get_day_table_by_time(day)

    for day_record in day_records:
        day_time_list.remove(day_record.time)

    for time in day_time_list:
        btn = InlineKeyboardButton(time, callback_data=time)
        keyboard.add(btn)

    return keyboard


def get_day_table_by_time(day):
    s = get_session()
    records = s.query(Record).filter_by(day = day).all()

    return records


