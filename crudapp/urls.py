from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("updateprofile/", views.updateprofile, name="updateprofile"),
    path("deleteinformation/", views.deleteinformation, name="deleteinformation")
]