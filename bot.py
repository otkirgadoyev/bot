from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputFile
import asyncio

BOT_TOKEN = "7185789337:AAFgrmBIMuxV17v_6qsPe-oTd2H1J148fBw"
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from django.core.files.base import ContentFile

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
from apps.bot.choices import Category
dp.middleware.setup(LoggingMiddleware())

callback_factory = CallbackData("doc", "id")


@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("Отправка", request_contact=True)
    keyboard.add(button)
    await message.answer(f"Ваш номер телефона: ", reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact_received(message: types.Message):
    phone_number = message.contact.phone_number
    telegram_id = message.from_user.id
    user, created = await asyncio.to_thread(User.objects.get_or_create, phone_number=phone_number,
                                            telegram_id=telegram_id)

    if created:
        await message.answer(
            text=(
                f"Этот пользователь {message.from_user.full_name} {phone_number} В списке под номером {phone_number}! Дождитесь ответа администратора."),
            reply_markup=types.ReplyKeyboardRemove()
        )

    else:
        if user.active == False:
            await message.answer(
                text=(
                    f"Этот {phone_number} номер зарегистрирован но не активен! Свяжитесь с администратором, чтобы активировать учетную запись."),
                reply_markup=types.ReplyKeyboardRemove()
            )

        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(
                types.InlineKeyboardButton(text="Загрузить файл"),
                types.InlineKeyboardButton(text="Загрузка файла"),
            )

            await message.answer(
                text=("Добро пожаловать в бот!"),
                reply_markup=keyboard
            )


@dp.message_handler(lambda message: message.text in ['Загрузить файл', 'Загрузка файла'],
                    content_types=types.ContentType.TEXT, state="*")
async def upload_file(message: types.Message):
    telegram_id = message.from_user.id
    user = await asyncio.to_thread(User.objects.get, telegram_id=telegram_id)
    if user.active:
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        if message.text == 'Загрузить файл':
            keyboard.add(
                types.InlineKeyboardButton(text="юридический"),
                types.InlineKeyboardButton(text="бухгалтер"),
                types.InlineKeyboardButton(text="кадр"),
                types.InlineKeyboardButton(text="входящая исходящая почта"),
                types.InlineKeyboardButton(text="Назад"),
            )
            await message.answer(
                text=" Выберите категорию для отправки файла",
                reply_markup=keyboard
            )
        elif message.text == 'Загрузка файла':
            keyboard.add(
                types.InlineKeyboardButton(text="получение из юридических писем"),
                types.InlineKeyboardButton(text="получение из писем бухгалтера"),
                types.InlineKeyboardButton(text="вывод из кадра"),
                types.InlineKeyboardButton(text="получение из входящей исходящей почты"),
                types.InlineKeyboardButton(text="Назад"),
            )
            await message.answer(
                text=" Выберите категорию загрузки",
                reply_markup=keyboard
            )
        else:
            await message.answer(f"Ваша команда: {message.text}")
    else:
        await message.answer(
            text="Вам не разрешено использовать бота.",
            reply_markup=types.ReplyKeyboardRemove()
        )


@dp.message_handler(
    lambda message: message.text in ['юридический', 'бухгалтер', 'кадр', 'входящая исходящая почта',
                                     "Назад", 'получение из юридических писем', 'получение из писем бухгалтера',
                                     'вывод из кадра', 'получение из входящей исходящей почты', "*"],
    content_types=types.ContentType.TEXT, state="*")
async def files(message: types.Message):
    telegram_id = message.from_user.id
    user = await asyncio.to_thread(User.objects.get, telegram_id=telegram_id)
    if user.active:
        if message.text == "юридический":
            mas = ("чтобы добавить юридический файл, отправьте файл боту."
                   " Введите команду /home, чтобы перейти к началу бота")
            await message.answer(
                text=mas,
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif message.text == "бухгалтер":
            mas = ("чтобы добавить бухгалтерский файл, отправьте файл боту."
                   " Введите команду /home, чтобы перейти к началу бота")
            await message.answer(
                text=mas,
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif message.text == "кадр":
            mas = ("чтобы добавить файл в файлы кадров, отправьте файл боту."
                   " Введите команду /home, чтобы перейти к началу бота")
            await message.answer(
                text=mas,
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif message.text == "входящая исходящая почта":
            mas = ("чтобы добавить файл в файлы входящей и исходящей почты, отправьте файл боту."
                   " Введите команду /home, чтобы перейти к началу бота")
            await message.answer(
                text=mas,
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif message.text == 'получение из юридических писем':
            files = await asyncio.to_thread(File.objects.filter, category=Category.yuridik)
            keyboard = InlineKeyboardMarkup()
            async for file in files:
                keyboard.add(InlineKeyboardButton(callback_data=f'doc_{file.id}', text=file.file.name))
            mas = "список юридических писем:"
            await message.answer(
                text=mas,
                reply_markup=keyboard
            )
        elif message.text == 'получение из писем бухгалтера':
            files = await asyncio.to_thread(File.objects.filter, category=Category.buxgalter)
            keyboard = InlineKeyboardMarkup()
            async for file in files:
                keyboard.add(InlineKeyboardButton(callback_data=f'doc_{file.id}', text=f"{file.file.name}"))
            mas = "список файлов писем бухгалтера:"
            await message.answer(
                text=mas,
                reply_markup=keyboard
            )
        elif message.text == 'вывод из кадра':
            files = await asyncio.to_thread(File.objects.filter, category=Category.kadr)
            keyboard = InlineKeyboardMarkup()
            async for file in files:
                keyboard.add(InlineKeyboardButton(callback_data=f'doc_{file.id}', text=f"{file.file.name}"))
            mas = "список файлов кадров:"
            await message.answer(
                text=mas,
                reply_markup=keyboard
            )
        elif message.text == 'получение из входящей исходящей почты':
            files = await asyncio.to_thread(File.objects.filter, category=Category.pochta)
            keyboard = InlineKeyboardMarkup()
            async for file in files:
                keyboard.add(InlineKeyboardButton(callback_data=f'doc_{file.id}', text=file.file.name))
            mas = "список входящих исходящих файлов:"
            await message.answer(
                text=mas,
                reply_markup=keyboard
            )
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(
                types.InlineKeyboardButton(text="Загрузить файл"),
                types.InlineKeyboardButton(text="Загрузка файла"),
            )
            await message.answer("Выберите категорию", reply_markup=keyboard)
    else:
        await message.answer(
            text="Использование бота для вас не разрешено.",
            reply_markup=types.ReplyKeyboardRemove()
        )


async def save_file(document: types.Document):
    file_info = await document.bot.get_file(document.file_id)
    file_path = document.file_name
    await document.bot.download_file(file_info.file_path, f"media/{file_path}")
    return file_path


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def download_file(message: types.Message):
    document = message.document
    file_path = await save_file(document)
    print(message.text)
    await asyncio.to_thread(File.objects.create, file=file_path)

    await message.answer(
        text="Файл загружен"
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('doc_'))
async def process_callback(callback_query: CallbackQuery):
    doc_id = int(callback_query.data.split('_')[1])
    document = await asyncio.to_thread(File.objects.get, id=doc_id)

    document_path = document.file.path
    input_file = InputFile(document_path)

    await callback_query.bot.answer_callback_query(callback_query.id)
    await callback_query.bot.send_document(callback_query.from_user.id, input_file)


@dp.message_handler(commands=['home'])
async def start_home(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        types.InlineKeyboardButton(text="Загрузить файл"),
        types.InlineKeyboardButton(text="Загрузка файла"),
    )

    await message.answer(
        text="Вы в начале бота",
        reply_markup=keyboard
    )


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp)
