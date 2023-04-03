from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView

from .models import Post, Tag, Author


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
        context['tags'] = Tag.objects.all().order_by("tag")
        return context


class PostsByTag(ListView):
    template_name = "Blog/posts.html"
    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset().filter(tags__tag=Tag.objects.get(tag=self.kwargs['str'])).order_by("-date")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = f"Posts with tag "+self.kwargs['str']
        context['tags'] = Tag.objects.exclude(
            tag=self.kwargs['str']).order_by("tag")
        return context


class Post(DetailView):
    template_name = "Blog/post.html"
    model = Post
    context_object_name = "post"


class Authors(ListView):
    template_name = "Blog/authors.html"
    model = Author
    context_object_name = "authors"


class Author(DetailView):
    template_name = "Blog/author.html"
    model = Author
    context_object_name = "author"

class About(TemplateView):
    pass
