from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index-page"),
    path("posts", views.posts, name="posts-page"),
    path("posts/<slug:slug>", views.posts_detail, name="post-detail-page")
]
