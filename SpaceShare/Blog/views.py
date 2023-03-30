from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView

from .models import Post, Tag


class Index(ListView):
    template_name = "Blog/index.html"
    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset().order_by("-date")[0:4]


class Posts(ListView):
    template_name = "Blog/posts.html"
    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset().order_by("-date")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "All Posts"
        return context


class Categories(ListView):
    pass


class Post(DetailView):
    pass
