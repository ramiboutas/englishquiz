from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.shortcuts import render, get_object_or_404

from .models import BlogPost




def post_list_view(request):
    objects = BlogPost.objects.filter(public=True)
    context = {'objects': objects}
    return render(request, 'blog/post_detail.html', context)


def post_detail_view(request, slug, level):
    object = get_object_or_404(BlogPost, slug=slug, level=level)
    context = {'object': object}
    return render(request, 'blog/post_detail.html', context)

