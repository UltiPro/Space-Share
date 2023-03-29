from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("categories", views.Categories.as_view(), name="categories")
]