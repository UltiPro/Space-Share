from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("posts", views.Posts.as_view(), name="posts"),
    path("posts/<str:str>,", views.PostsByTag.as_view(), name="posts_by_tag"),
    path("post/<slug:slug>", views.Post.as_view(), name="post_by_slug"),

    path("posts/<str:str>", views.Categories.as_view(), name="posts_by_find"),
    path("categories", views.Categories.as_view(), name="categories"),
    path("about", views.Categories.as_view(), name="about")
]
