from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputFile
import asyncio

BOT_TOKEN = "7185789337:AAFgrmBIMuxV17v_6qsPe-oTd2H1J148fBw"
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData

logging.basicConfig(level=logging.DEBUG)

Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=Bot)

import django
import sys
import os

# --------- < DJANGO SETUP > -----------
path_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(path_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.develop")
django.setup()
# --------  < / DJANGO SETUP > --------
from apps.bot.models import User, File

dp.middleware.setup(LoggingMiddleware())

callback_factory = CallbackData("doc", "id")


@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("Yuborish", request_contact=True)
    keyboard.add(button)
    await message.answer(f"Telefon raqam: ", reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact_received(message: types.Message):
    phone_number = message.contact.phone_number
    telegram_id = message.from_user.id
    user, created = await asyncio.to_thread(User.objects.get_or_create, phone_number=phone_number,
                                            telegram_id=telegram_id)
    if created:
        await message.reply(
            f"Ushbu foydalanuvchi {message.from_user.full_name} {phone_number} raqami bilan ro'yhatga olindi !")
    else:
        await message.reply(f"Ushbu {phone_number} raqam allaqachon ro'yhatdan o'tgan !")

    # keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    # keyboard.add(
    #     types.InlineKeyboardButton(text="Fayl yuklash"),
    #     types.InlineKeyboardButton(text="Fayl yuklab olish"),
    # )
    await message.answer("Admin javobini kuting !")


@dp.message_handler(lambda message: message.text in ['Fayl yuklash', 'Fayl yuklab olish'],
                    content_types=types.ContentType.TEXT, state="*")
async def upload_file(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if message.text == 'Fayl yuklash':
        keyboard.add(
            types.InlineKeyboardButton(text="1-ishxona fayllari"),
            types.InlineKeyboardButton(text="2-ishxona fayllari"),
            types.InlineKeyboardButton(text="3-ishxona fayllari"),
            types.InlineKeyboardButton(text="Orqaga"),
        )
        await message.answer(
            text=" upload Kategoriyani tanlang",
            reply_markup=keyboard
        )
    elif message.text == 'Fayl yuklab olish':
        keyboard.add(
            types.InlineKeyboardButton(text="1-ishxona fayllaridan olish"),
            types.InlineKeyboardButton(text="2-ishxona fayllaridan olish"),
            types.InlineKeyboardButton(text="3-ishxona fayllaridan olish"),
            types.InlineKeyboardButton(text="Orqaga"),
        )

        await message.answer(
            text=" download Kategoriyani tanlang",
            reply_markup=keyboard
        )
    else:
        await message.answer(f"Sizning buyrugingiz: {message.text}")


@dp.message_handler(
    lambda message: message.text in ['1-ishxona fayllari', '2-ishxona fayllari', '3-ishxona fayllari',
                                     '1-ishxona fayllaridan olish', "Orqaga",
                                     '2-ishxona fayllaridan olish', '3-ishxona fayllaridan olish', "*"],
    content_types=types.ContentType.TEXT, state="*")
async def files(message: types.Message):
    files = await asyncio.to_thread(File.objects.all)
    keyboard = InlineKeyboardMarkup()
    async for file in files:
        keyboard.add(InlineKeyboardButton(callback_data=f'doc_{file.id}', text=file.file.name))
    if message.text == "1-ishxona fayllari":
        mas = "1- ishxona fayllari ro'yhati"
        await message.answer(
            text=mas,
            reply_markup=keyboard
        )
    elif message.text == "2-ishxona fayllari":
        mas = "2-ishxona faylini yuklang"
        await message.answer(
            text=mas,
            reply_markup=keyboard
        )
    elif message.text == "3-ishxona fayllari":
        mas = "3-ishxona faylini yuklang"
        await message.answer(
            text=mas,
            reply_markup=keyboard
        )
    elif message.text == '1-ishxona fayllaridan olish':
        mas = "1-ishxona fayllari ro'yxati:"
        await message.answer(
            text=mas,
            reply_markup=keyboard
        )
    elif message.text == '2-ishxona fayllaridan olish':
        mas = "2-ishxona fayllari ro'yxati:"
        await message.answer(
            text=mas,
            reply_markup=keyboard
        )
    elif message.text == '3-ishxona fayllaridan olish':
        mas = "3-ishxona fayllari ro'yxati:"
        await message.answer(
            text=mas,
            reply_markup=keyboard
        )
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(
            types.InlineKeyboardButton(text="Fayl yuklash"),
            types.InlineKeyboardButton(text="Fayl yuklab olish"),
        )
        await message.answer("Kategoriyani tanlang", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('doc_'))
async def process_callback(callback_query: CallbackQuery):
    print("callback_query", callback_query)
    print("callback_query.data", callback_query.data)
    print("callback_query.data.split", callback_query.data.split("_"))
    doc_id = int(callback_query.data.split('_')[1])
    document = await asyncio.to_thread(File.objects.get, id=doc_id)

    document_path = document.file.path
    input_file = InputFile(document_path)

    await callback_query.bot.answer_callback_query(callback_query.id)
    await callback_query.bot.send_document(callback_query.from_user.id, input_file)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp)

