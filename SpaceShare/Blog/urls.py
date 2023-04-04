from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("posts", views.Posts.as_view(), name="posts"),
    path("posts/<str:str>,", views.PostsByTag.as_view(), name="posts_by_tag"),
    path("post/<slug:slug>", views.Post.as_view(), name="post"),
    path("authors", views.Authors.as_view(), name="authors"),
    path("author/<slug:slug>", views.Author.as_view(), name="author"),
    path("author/<slug:slug>/posts",
         views.AuthorPosts.as_view(), name="author_posts"),
    path("author/<slug:slug>/posts/<str:str>",
         views.AuthorPostsByTag.as_view(), name="author_posts_by_tag"),
    path("about-us", views.About.as_view(), name="about_us")
]
