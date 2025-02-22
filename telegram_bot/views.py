from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from config.settings.base import BOT_NAME_TELEGRAM
from telegram_bot.models import TelegramUser

BOT_NAME = BOT_NAME_TELEGRAM


def generate_link(request):
    user_request = get_user_model()(id=request.user.id)
    user_telegram, _ = TelegramUser.objects.get_or_create(
        user=user_request
    )
    link = f"https://t.me/{BOT_NAME}?start={user_telegram.unique_token}"
    return HttpResponse(f"Перейдіть за лінком: {link}")


def verify_token(request):
    token = request.GET.get("token")
    try:
        user = TelegramUser.objects.get(unique_token=token)
        return JsonResponse({"status": "success", "user_id": user.user.id})
    except TelegramUser.DoesNotExist:
        return JsonResponse(
            {
                "status": "error",
                "message": "Invalid token"
            },
            status=400
        )


@csrf_exempt
def link_telegram_account(request):
    user_id = request.POST.get("user_id")
    print(user_id)
    telegram_id = request.POST.get("telegram_id")
    print(telegram_id)

    try:
        user = TelegramUser.objects.get(user_id=user_id)
        user.telegram_id = telegram_id
        user.save()
        return JsonResponse({"status": "success"})
    except TelegramUser.DoesNotExist:
        return JsonResponse(
            {
                "status": "error",
                "message": "User not found"
            },
            status=400
        )
