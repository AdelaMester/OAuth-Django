from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, "crudapp/home.html")

def profile(request):
    if request.method == 'GET':
        return render(request, "crudapp/profile.html")

def updateprofile(request):
    if request.method == 'GET':
        return render(request, "crudapp/updateinformation.html")

def deleteinformation(request):
    if request.method == 'GET':
        return render(request, "crudapp/deleteinformation.html")