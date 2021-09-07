from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("insertinformation/", views.insertinformation, name="insertinformation"),
    path("updateprofile/", views.updateprofile, name="updateprofile"),
    path("deleteinformation/", views.deleteinformation, name="deleteinformation"),
    path("request_identity/", views.request_identity, name="request_identity"),
    path("callback/", views.callback, name="callback"),
]