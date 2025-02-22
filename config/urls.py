"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/library-service/",
        include("service.urls"),
        name="library-service"
    ),
    path(
        "api/v1/library-service/user/",
        include("user.urls"),
        name="user"
    ),
    path(
        "api/v1/library-service/telegram/",
        include("telegram_bot.urls"),
        name="telegram-bot",
    ),
    path(
        "api/v1/library-service/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),
    # Optional UI:
    path(
        "api/v1/library-service/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/library-service/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
