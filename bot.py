import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ChatType

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

DEFAULT_PHOTO_URL = "https://picsum.photos/800/600"
waiting_for_photo = set()
saved_photo_id = None


@dp.message(Command("setphoto"))
async def set_photo_cmd(message: types.Message):
    if message.chat.type != ChatType.PRIVATE:
        await message.reply("Эту команду можно использовать только в личке.")
        return
    waiting_for_photo.add(message.from_user.id)
    await message.reply("Отправь мне фото, которое я буду использовать.")


@dp.message()
async def on_message(message: types.Message):
    global saved_photo_id

    if message.from_user.id in waiting_for_photo and message.photo:
        saved_photo_id = message.photo[-1].file_id
        waiting_for_photo.remove(message.from_user.id)
        await message.reply("Фото сохранено.")
        return

    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                username = (await bot.me()).username
                mention_text = message.text[entity.offset:entity.offset + entity.length]
                if mention_text == f"@{username}":
                    if saved_photo_id:
                        await message.reply_photo(saved_photo_id)
                    else:
                        await message.reply_photo(DEFAULT_PHOTO_URL)
                    break


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

