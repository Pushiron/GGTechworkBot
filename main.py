import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties

API_TOKEN = "8035684778:AAGNHBd67M6kUZPPrp2QaAUwE__Q5gtM8Qg"

# Разрешённые пользователи (ID)
ALLOWED_USERS = {645755081, 201850955, 201473362, 928133422, 263879658, 1389666510}

DEBUG_CHAT = -4943149624  # Местные

# Чаты
TARGET_CHATS = [
    -4231782629,  # Хорека
    -4851122930,  # Онлайн заявочник
    -4179421868,  # Сибэкс
    -1002187443869,  # Планшеты
    -4192894206,  # Нижнеудинск
    -4173517051,  # GG
    -1002217495330,  # АК
]

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# Флаг режима
debug_mode = False


def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS


@dp.message(F.command("debug_on"))
async def debug_on(message: Message):
    global debug_mode
    if not is_allowed(message.from_user.id):
        await message.reply("⛔ У вас нет доступа.")
        return

    debug_mode = True
    await message.reply("✅ Режим DEBUG включен. Все сообщения будут пересылаться только в DEBUG_CHAT.")


@dp.message(F.command("debug_off"))
async def debug_off(message: Message):
    global debug_mode
    if not is_allowed(message.from_user.id):
        await message.reply("⛔ У вас нет доступа.")
        return

    debug_mode = False
    await message.reply("✅ Режим DEBUG выключен. Все сообщения будут пересылаться в чаты TARGET_CHATS.")


@dp.message(F.photo)
async def forward_photo(message: Message):
    if not is_allowed(message.from_user.id):
        await message.reply("⛔ У вас нет доступа к этой функции.")
        return

    caption = message.caption or ""
    photo = message.photo[-1].file_id

    if debug_mode:
        await bot.send_photo(chat_id=DEBUG_CHAT, photo=photo, caption=caption)
    else:
        for chat_id in TARGET_CHATS:
            await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)


@dp.message(F.text)
async def forward_text(message: Message):
    if not is_allowed(message.from_user.id):
        await message.reply("⛔ У вас нет доступа к этой функции.")
        return

    if debug_mode:
        await bot.send_message(chat_id=DEBUG_CHAT, text=message.text)
    else:
        for chat_id in TARGET_CHATS:
            await bot.send_message(chat_id=chat_id, text=message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
