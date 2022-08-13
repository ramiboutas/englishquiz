from django.urls import path

from .views import post_detail_view, post_list_view, all_posts_view

urlpatterns = [
    path("", post_list_view, name="blog_postlist"),
    path("all/", all_posts_view, name="blog_allposts"),
    path("<str:level>/<slug:slug>/", post_detail_view, name="blog_postdetail"),
]