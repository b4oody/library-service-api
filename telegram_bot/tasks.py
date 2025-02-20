from celery import shared_task

from telegram_bot.models import TelegramUser
from telegram_bot.utilities import send_telegram_message


@shared_task
def send_special_offer():
    message = """
    🚨 **Акція Тижня!** 🚨

    🎉 Сьогодні тільки для тебе - знижка 20% на весь асортимент! 🎉

    Залишилося лише кілька годин, поспішай! ⏳

    👉 Не пропусти шанс зекономити. Для подробиць натискай на кнопку нижче!
    """
    for user in TelegramUser.objects.all():
        send_telegram_message(user.telegram_id, message)
