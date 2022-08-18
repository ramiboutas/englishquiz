from django.urls import path

from .views import post_detail_view, post_list_view, all_posts_view, pdf_post_view

urlpatterns = [
    path("", post_list_view, name="blog_postlist"),
    path("all/", all_posts_view, name="blog_allposts"),
    path("<str:level>/<slug:slug>/", post_detail_view, name="blog_postdetail"),
    path("<str:level>/<slug:slug>/pdf/", pdf_post_view, name="blog_postpdf"),
]