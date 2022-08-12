from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.shortcuts import render, get_object_or_404

from .models import BlogPost




def post_list_view(request):
    # object_list = BlogPost.objects.filter(public=True)
    last_posts = BlogPost.get_last_posts()
    popular_posts = BlogPost.get_popular_posts()
    context = {'last_posts': last_posts, 'popular_posts': popular_posts}
    return render(request, 'blog/post_list.html', context)


def post_detail_view(request, slug, level):
    object = get_object_or_404(BlogPost, slug=slug, level=level)
    object.add_view()
    context = {'object': object}
    return render(request, 'blog/post_detail.html', context)

