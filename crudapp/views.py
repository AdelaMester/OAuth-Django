from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')


# Create your views here.
def index(request):
    print(client_id)
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