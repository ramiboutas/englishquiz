from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import BlogPost




def post_list_view(request):
    last_posts = BlogPost.get_last_posts()
    popular_posts = BlogPost.get_popular_posts()
    context = {'last_posts': last_posts, 'popular_posts': popular_posts}
    return render(request, 'blog/post_list.html', context)


def all_posts_view(request):
    all_posts = BlogPost.get_all_posts()
    paginator = Paginator(all_posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/all_posts.html', context)


def post_detail_view(request, slug, level):
    post = get_object_or_404(BlogPost, slug=slug, level=level)
    post.add_view()
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)
