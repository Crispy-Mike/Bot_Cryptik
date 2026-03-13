import telebot
import sqlite3
from telebot import types
import time
import os
from dotenv import load_dotenv
from data_bases import conn
from Data_base import user_db

# Загружаем переменные из .env (для локальной разработки)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

bot = telebot.TeleBot(BOT_TOKEN)

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        user_nikname TEXT,
        user_name TEXT,
        user_surname TEXT,
        user_is_bot BOOLEAN DEFAULT 0
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_and_sale (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        operation_type TEXT NOT NULL,
        first_currency TEXT NOT NULL,
        first_quantity REAL NOT NULL,
        second_currency TEXT NOT NULL,
        second_quantity REAL NOT NULL,
        timestamp DATETIME DEFAULT (datetime('now')),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
""")
conn.commit()


def register_user(func):
    def wrapper(message):
        user=message.from_user
        user_db.write(
            user_id_w=user.id,
            user_nikname_w=user.username,
            user_name_w=user.first_name,
            user_surname_w=user.last_name, 
            user_is_bot_w=user.is_bot
        )
        return func(message)
    return wrapper


@bot.message_handler(commands=["start"])
@register_user
def start_bot(message):
    try:
        with open(r"C:\Cryptik\first.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="Это бот для обмена криптовалюты, для подробностей его возможностей воспользуйтесь командой /help, для запуска используйте команду /cryptic."
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            "👋 Привет! Это бот для обмена криптовалюты.\n"
            "Для подробностей используйте /help\n"
            "Для запуска используйте /cryptic"
        )

@bot.message_handler(commands=["help"])
@register_user
def help_bot(message):
    help_text = """
🤖 *Доступные команды:*
/start - Начало работы
/help - Справка
/cryptic - Открыть обменник криптовалют
"""
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(commands=["cryptic"])
@register_user
def cryptic_bot(message):
    web_app_url = "https://crispy-mike.github.io/Cryspik/" 
    

    markup = types.InlineKeyboardMarkup()
    web_app_button = types.InlineKeyboardButton(
        text="🚀 Открыть окно обменника",
        web_app=types.WebAppInfo(url=web_app_url)
    )
    markup.add(web_app_button)
    
    bot.send_message(
        message.chat.id,
        "👇 *Нажмите кнопку ниже, чтобы открыть окно обменника:*\n\n"
        "После совершения операций в окне, данные вернутся в бот.",
        reply_markup=markup,
        parse_mode="Markdown"
    )


@bot.message_handler(content_types=['web_app_data'])
@register_user
def handle_web_app_data(message):
    data = message.web_app_data.data
    user_name = message.from_user.first_name

    bot.send_message(
        message.chat.id,
        f"✅ Спасибо, {user_name}!\n"
        f"Получены данные из окна: {data}\n\n"
        f"Для нового обмена используйте /cryptic"
    )

@bot.message_handler(commands=["profile"])
@register_user
def profile(message):
    bot.send_message(
        message.chat.id,
        f"""Имя: {message.from_user.first_name}
Фамилия: {message.from_user.last_name}
Никнейм: {message.from_user.username}
ID: {message.from_user.id}
Является ли ботом: {message.from_user.is_bot}"""
    )

@bot.message_handler(commands=["profiles"])
@register_user
def profile(message):
    if message.from_user.id == 1821635278:
        conn = sqlite3.connect("cryptik.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        
        # Формируем сообщение
        response = "=== ТАБЛИЦА users ===\n"
        for row in rows:
            response += str(row) + "\n"
        
        bot.send_message(message.chat.id, response)
        
        conn.close()

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()