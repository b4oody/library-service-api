import os

import requests
import telebot
from django.core.management import BaseCommand
from dotenv import load_dotenv

from telegram_bot.models import TelegramUser

load_dotenv()

API_URL = os.environ.get("API_BASE_URL")


class Command(BaseCommand):
    help = "Run the Telegram bot"

    def handle(self, *args, **options):
        bot = telebot.TeleBot(os.environ.get("TOKEN"))

        @bot.message_handler(commands=["start"])
        def start(message):
            if TelegramUser.objects.filter(telegram_id=message.from_user.id).exists():
                bot.send_message(
                    message.chat.id,
                    "Ваш акаунт вже прив'язаний!"
                )
            else:
                unique_token = message.text.split()[1] if len(message.text.split()) > 1 else None

                if unique_token:
                    response = requests.get(
                        f"{API_URL}/telegram/verify_token?token={unique_token}"
                    )

                    if response.status_code == 200:
                        user_data = response.json()
                        user_id = user_data.get("user_id")

                        user = requests.post(
                            f"{API_URL}/telegram/link_telegram_account/",
                            data={
                                "user_id": user_id,
                                "telegram_id": message.from_user.id
                            },
                        )

                        if user.status_code == 200:
                            bot.send_message(
                                message.chat.id,
                                "Ваш акаунт успішно прив'язано до Telegram."
                            )
                        else:
                            bot.send_message(
                                message.chat.id,
                                "Помилка під час прив'язки акаунту."
                            )
                    else:
                        bot.send_message(
                            message.chat.id,
                            "Невірний токен!"
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        "Токен не знайдено!"
                        "Перейдіть по посиланню для прив'язанння"
                    )

        bot.polling()
