from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .models import TelegramMessage

@cache_page(3600 * 24 * 1)
def telegram_view(request):
    telegram_messages = TelegramMessage.objects.all().order_by('-id')[:10]
    context = {'telegram_messages': telegram_messages}
    return render(request, 'socialmedia/telegram.html', context)

