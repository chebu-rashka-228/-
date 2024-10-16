import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup)

from pydantic import ValidationError

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

BOT_TOKEN = '6834075828:AAFG7-5Xep3Fy5i81e4XOfEBe-64acQJmrc'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Записать'),
            KeyboardButton(text='Получить')

        ]
    ],
    resize_keyboard=True)


class Form(StatesGroup):
    name = State()


@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    await message.answer(text=f"Привет, {message.from_user.username}, это мой бот для отбора в ЦТ!\n ",
                         reply_markup=start_kb)


@dp.message(StateFilter(Form.name), F.text == 'Получить')
async def process_name(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        await message.answer(data["name"])
    except ValidationError:
        await message.answer("Не было записано текстового сообщения")


@dp.message(F.text == 'Записать')
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше сообщение:")
    await state.set_state(Form.name)


@dp.message(StateFilter(Form.name))
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сообщение успешно записано! ")


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
