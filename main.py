import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData
from aiogram_calendar import SimpleCalendar, simple_cal_callback

from config import BOT_TOKEN

from db import *

from board import day_table, ChooseDateState


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_bot(mes: types.Message):

    add_user(mes.from_user.id, mes.from_user.username)

    await mes.answer("Балзия әпкиге жазылу ушін /table басыңыз.")


@dp.message_handler(commands=['table'])
async def show_table(mes: types.Message):

    await ChooseDateState.day.set()

    await mes.answer("Күнді басыңыз", reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter(), state=ChooseDateState.day)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    new_date = date.strftime("%Y-%m-%d")

    if selected:

        if datetime.today() > date:
            await callback_query.message.answer("Келешек күнді тандаңыз :)", reply_markup=await SimpleCalendar().start_calendar())

        else:
            await state.update_data(day = new_date)

            await ChooseDateState.time.set()

            await callback_query.bot.send_message(callback_query.from_user.id, "Уақыт таңдаңыз", reply_markup = day_table(new_date))


@dp.callback_query_handler(state=ChooseDateState.time)
async def time(callback_query: CallbackQuery, state: FSMContext):

    await state.update_data(time = callback_query.data)

    await callback_query.message.edit_reply_markup(reply_markup=None)

    await callback_query.message.answer("Толық атыңыз бен тобыңызды жазыңыз!")

    await ChooseDateState.who.set()


@dp.message_handler(state=ChooseDateState.who)
async def who(mes: types.Message, state: FSMContext):

    await state.update_data(who = mes.text)

    await mes.answer("Келу мақсатыңызды жазыңыз!")

    await ChooseDateState.aim.set()


@dp.message_handler(state=ChooseDateState.aim)
async def aim(mes: types.Message, state: FSMContext):

    data = await state.get_data()

    add_record(data['day'], data['time'], data['who'], mes.text)

    await state.finish()

    await mes.answer(f"Сіз {data['day']} күні сағат {data['time']} жазылдыңыз.\nСізді күтеміз!")

    await mes.bot.send_message(499895952, f"Сізге жаңа адам жазылды:\n{data['day']}\n{data['time']}\n{data['who']}\n{mes.text}")


def start():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start()