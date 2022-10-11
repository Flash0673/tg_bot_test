import asyncio

import aiogram.dispatcher.filters
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import tg_bot_token
from sheets import Sheets
import messages

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

menu = types.ReplyKeyboardMarkup(
    [
        [
            types.KeyboardButton(text="Видеоматериалы")
        ],
        [
            types.KeyboardButton(text="Дополнительные материалы")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(messages.hello_mes, reply=False)
    await bot.send_message(chat_id=message.chat.id, text=messages.make_schedule_mes)

@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
    await message.reply(messages.retrun_to_menu, reply=False)

@dp.message_handler(commands=["menu"])
async def start_command(message: types.Message):
    await message.reply(messages.menu_mes, reply=False, reply_markup=menu)

@dp.message_handler(aiogram.dispatcher.filters.Text(equals=["Видеоматериалы", "Дополнительные материалы"]))
async def send_materials(message: types.Message):
    sheet = Sheets()
    if message.text == "Видеоматериалы":
        materials = sheet.send_main_materials()
        await message.answer(materials)
        await message.answer(messages.retrun_to_menu)
    elif message.text == "Дополнительные материалы":
        materials = sheet.send_additional_materials()
        await message.answer(materials)
        await message.answer(messages.retrun_to_menu)


@dp.message_handler()
async def make_schedule(message: types.Message):
    time_converter = {
        "сек": 1,
        "мин": 60,
        "ч": 3600
    }
    try:
        parsed_mes = message.text.split()
        if len(parsed_mes) < 2:
            raise ValueError()
        schedule_time = int(parsed_mes[0])
        if schedule_time <= 0:
            raise ValueError()
        units = parsed_mes[1]
        if units not in time_converter:
            raise TypeError()

    except (TypeError, ValueError):
        await bot.send_message(chat_id=message.chat.id, text=messages.err_mas)
        return
    schedule_time *= time_converter[units]
    await bot.send_message(chat_id=message.chat.id, text=messages.schedule_completed.replace("schedule", message.text),
                           reply_markup=menu
                           )
    while True:
        await asyncio.sleep(schedule_time)
        await bot.send_message(chat_id=message.chat.id, text=messages.schedule_mes)





if __name__ == "__main__":
    executor.start_polling(dp)

