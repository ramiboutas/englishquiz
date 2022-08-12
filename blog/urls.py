from django.urls import path


from .views import post_detail_view, post_list_view

urlpatterns = [
    path("", post_list_view, name="blog_postlist"),
    path("<str:level>/<slug:slug>", post_detail_view, name="blog_postdetail"),
]