import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
if not API_TOKEN:
    raise ValueError("❌ TELEGRAM_API_TOKEN is not set!")

# Разрешённые пользователи (ID)
allowed_users_env = os.getenv("ALLOWED_USERS", "")
ALLOWED_USERS = [int(user_id) for user_id in allowed_users_env.split(",") if user_id]

target_chats_env = os.getenv("TARGET_CHATS", "")

# Чаты
TARGET_CHATS = [int(chat_id) for chat_id in target_chats_env.split(",") if chat_id]

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()


def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

@dp.startup()
async def on_startup(dispatcher: Dispatcher):
    logging.info("🚀 Бот запущен и готов к работе!")


@dp.shutdown()
async def on_shutdown(dispatcher: Dispatcher):
    logging.info("🛑 Бот остановлен.")

@dp.message(F.photo)
async def forward_photo(message: Message):
    if not is_allowed(message.from_user.id):
        await message.reply("⛔ У вас нет доступа к этой функции.")
        return

    caption = message.caption or ""
    photo = message.photo[-1].file_id

    for chat_id in TARGET_CHATS:
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)


@dp.message(F.text)
async def forward_text(message: Message):
    if not is_allowed(message.from_user.id):
        await message.reply("⛔ У вас нет доступа к этой функции.")
        return

    for chat_id in TARGET_CHATS:
        await bot.send_message(chat_id=chat_id, text=message.text)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
