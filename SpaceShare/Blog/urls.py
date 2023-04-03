from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("posts", views.Posts.as_view(), name="posts"),
    path("posts/<str:str>,", views.PostsByTag.as_view(), name="posts_by_tag"),
    path("post/<slug:slug>", views.Post.as_view(), name="post_by_slug"),
    path("authors", views.Authors.as_view(), name="authors"),
    path("author/<slug:slug>", views.Author.as_view(), name="author"),
    path("about", views.About.as_view(), name="about")
]
