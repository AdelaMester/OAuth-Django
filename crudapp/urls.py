from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("update/", views.updateprofile, name="updateprofile"),
    path("delete/", views.deleteinformation, name="deleteinformation")
]