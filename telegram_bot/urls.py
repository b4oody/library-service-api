from django.urls import path

from telegram_bot import views

urlpatterns = [
    path("generate_link/", views.generate_link, name="telegram-generate-link"),
    path("verify_token/", views.verify_token, name="telegram-verify_token"),
    path("link_telegram_account/", views.link_telegram_account, name="telegram_link_account"),
]

app_name = "telegram_bot"

