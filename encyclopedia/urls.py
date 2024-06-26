from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("random_page", views.random_page, name="random_page"),
    path("not_found", views.not_found, name="not_found")
]
