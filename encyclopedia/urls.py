from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("randompage", views.randompage, name="randompage"),
    path("newpage/", views.newpage, name="newpage"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("<str:title>", views.entries, name="entries"),
]
