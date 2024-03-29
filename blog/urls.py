from __future__ import annotations

from django.urls import path

from .views import all_posts_view
from .views import post_detail_view
from .views import post_list_view

urlpatterns = [
    path("", post_list_view, name="blog_postlist"),
    path("all/", all_posts_view, name="blog_allposts"),
    path("<slug:slug>/", post_detail_view, name="blog_postdetail"),
]
