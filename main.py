import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from parser import parse_medicine_info
from utils import chunk_text
import config

# Создаем объекты бота и диспетчера
bot = Bot(token=config.TOKEN)
dp = Dispatcher()


# Этот хэндлер будет обрабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        'Привет! Я бот, который поможет тебе найти информацию о препаратах. Отправь мне название препарата.')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Отправь мне название препарата и в ответ '
        'я пришлю тебе информацию о препарате'
    )


# Этот хэндлер будет срабатывать на сообщения с названием препарата
@dp.message()
async def send_medicine_info(message: Message):
    medicine_name = message.text
    info_list = parse_medicine_info(medicine_name)
    if info_list:
        for info in info_list:
            response = create_response(medicine_name, info)
            chunks = chunk_text(response)
            for chunk in chunks:
                await message.answer(chunk, parse_mode='HTML')
                await asyncio.sleep(1)
    else:
        await message.answer(f"Препарат {medicine_name} не найден.")


def create_response(medicine_name: str, info: dict) -> list:
    response = [
        f"<b>Препарат:</b> [{medicine_name}]({info['url']})\n\n",
        f"<b>Способы применения и дозы:</b>\n{info['dosages']}\n\n",
        f"<b>Показания к применению:</b>\n{info['indications']}\n\n",
        f"<b>Противопоказания:</b>\n{info['contraindications']}\n\n"
    ]
    return response


if __name__ == '__main__':
    dp.run_polling(bot)
