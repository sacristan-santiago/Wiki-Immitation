from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("page/add", views.addPage, name="page_add"),
    path("page/edit/<str:title>", views.editPage, name="page_edit"),
    path("random", views.randomPage, name="random")
]
