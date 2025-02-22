import os

import telebot
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(API_TOKEN)


def send_telegram_message(telegram_id, message):
    """
    Function for sending a message to a user via Telegram.
    """
    try:
        bot.send_message(telegram_id, message, parse_mode="Markdown")
    except Exception as e:
        print(f"Помилка при відправці повідомлення: {e}")
