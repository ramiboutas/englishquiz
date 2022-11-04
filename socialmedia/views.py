from __future__ import annotations

from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .models import LinkedinPost, TelegramMessage


@cache_page(3600 * 24 * 1)
def telegram_view(request):
    telegram_messages = TelegramMessage.objects.all().order_by("-id")[:10]
    context = {"telegram_messages": telegram_messages}
    return render(request, "socialmedia/telegram.html", context)


@cache_page(3600 * 24 * 1)
def linkedin_view(request):
    linkedin_posts = LinkedinPost.objects.all().order_by("-id")[:10]
    context = {"linkedin_posts": linkedin_posts}
    return render(request, "socialmedia/linkedin.html", context)


@cache_page(3600 * 24 * 1)
def twitter_view(request):
    pass
