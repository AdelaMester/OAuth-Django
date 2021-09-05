from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os
from uuid import uuid4
import urllib.parse

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
redirect_uri = "https://oauth-crudapp.herokuapp.com/callback"


# Create your views here.
def index(request):
    return render(request, "crudapp/index.html")


def profile(request):
    if request.method == 'GET':
        return render(request, "crudapp/profile.html")

def updateprofile(request):
    if request.method == 'GET':
        return render(request, "crudapp/updateinformation.html")

def deleteinformation(request):
    if request.method == 'GET':
        return render(request, "crudapp/deleteinformation.html")

def request_identity(request):
    state = str(uuid4())
    params = {"client_id": client_id,
              "response_type": "code",
              "redirect_uri": redirect_uri,
              "state": state,
              "duration": "temporary",
              "scope": "user"
              }
    return HttpResponseRedirect('https://github.com/login/oauth/authorize?' + urllib.parse.urlencode(params))

def callback(request):
    if request.method == 'GET':
        return render(request, "crudapp/home.html")
