import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== память =====
orders = {}
order_id = 1

# ===== меню =====
def menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💳 Карта под оплату")],
            [KeyboardButton(text="📋 Мои заявки")]
        ],
        resize_keyboard=True
    )

# ===== старт =====
@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer("Бот запущен 👋", reply_markup=menu())

# ===== создать заявку =====
@dp.message(F.text == "💳 Карта под оплату")
async def create_order(message: types.Message):
    global order_id

    orders[order_id] = {
        "user_id": message.from_user.id,
        "status": "new"
    }

    await message.answer(f"Заявка #{order_id} создана ✅")

    order_id += 1

# ===== список заявок =====
@dp.message(F.text == "📋 Мои заявки")
async def my_orders(message: types.Message):
    uid = message.from_user.id

    user_orders = [
        f"#{i} - {o['status']}"
        for i, o in orders.items()
        if o["user_id"] == uid
    ]

    if not user_orders:
        await message.answer("У тебя нет заявок")
    else:
        await message.answer("\n".join(user_orders))

# ===== запуск =====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())