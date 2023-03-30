from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("posts", views.Posts.as_view(), name="posts"),  # dokończ
    path("posts/<str:str>", views.Categories.as_view(),
         name="posts_by_find"),  # dokończ
    path("post/<slug:slug>", views.Categories.as_view(),
         name="post_by_tag"),  # dokończ
    path("categories", views.Categories.as_view(), name="categories"),  # dokończ
    path("about", views.Categories.as_view(), name="about")  # dokończ
]
