

from django.urls import path

from .views import telegram_view

urlpatterns = [
    path('telegram/', telegram_view, name='socialmedia_telegram'),
]