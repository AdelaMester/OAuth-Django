from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os
from uuid import uuid4
import urllib.parse
import requests
import json
import psycopg2

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
redirect_uri = "https://oauth-crudapp.herokuapp.com/callback"


# Create your views here.
def index(request):
    return render(request, "crudapp/index.html")

def home(request):
    if request.method == 'GET':

        # Log in validation, if no session['name'] redirect to / route
        if 'name' not in request.session:
            return HttpResponseRedirect("/")
        return render(request, "crudapp/home.html",{
            'name': request.session['name']

        })

def profile(request):
    if request.method == 'GET':

        # Log in validation, if no session['name'] redirect to / route
        if 'name' not in request.session:
            return HttpResponseRedirect("/")

        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        cur.execute("SELECT * FROM details WHERE username=%s", (request.session['name'],))
        profile_info = cur.fetchone()


        # Displays details from table and validates fields are not empty
        if profile_info:
            username = profile_info[0]
            address = profile_info[1]
            contact_number = profile_info[2]
        else:
            username = request.session['name']
            address = "Address not set"
            contact_number = "Contact number not set"
        cur.close()
        conn.close()
        return render(request, "crudapp/profile.html", {
            "username": username,
            "address": address,
            "contact_number": contact_number
        })

def updateprofile(request):
    # Log in validation, if no session['name'] redirect to / route
    if 'name' not in request.session:
            return HttpResponseRedirect("/")

    if request.method == 'GET':
        return render(request, "crudapp/updateprofile.html")

    # Connect to database and update information one by one
    if request.method == 'POST':
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        if request.POST.get('Address'):
            address = request.POST.get('Address')
            cur.execute("UPDATE details SET address =%s WHERE username=%s", (address, request.session['name']))
            conn.commit()
        else:
            number = request.POST.get('Contact_number')
            cur.execute("UPDATE details SET contact_number =%s WHERE username=%s", (number, request.session['name']))
            conn.commit()
        cur.close()
        conn.close()
        return HttpResponseRedirect("/profile/")


def insertinformation(request):
    # Log in validation, if no session['name'] redirect to / route
    if 'name' not in request.session:
            return HttpResponseRedirect("/")

    if request.method == 'GET':
        return render(request, "crudapp/insertinformation.html")

    # Connect to the database and check if any insertion was done, if not, insert information into database
    if request.method == 'POST':
        address = request.POST.get('Address')
        number = request.POST.get('Contact_number')
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        cur.execute("SELECT * FROM details WHERE username=%s", (request.session['name'],))
        row = cur.fetchone()
        if not row:
            cur.execute("INSERT INTO details (username, address, contact_number) VALUES (%s, %s, %s)", (request.session['name'], address, number))
            conn.commit()
        cur.close()
        conn.close()
        return HttpResponseRedirect("/profile/")


def deleteinformation(request):
    # Log in validation, if no session['name'] redirect to / route
    if 'name' not in request.session:
            return HttpResponseRedirect("/")

    if request.method == 'GET':
        return render(request, "crudapp/deleteinformation.html")

    # Connect to the database and delete information
    if request.method == 'POST':
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        cur.execute("DELETE FROM details WHERE username=%s", (request.session['name'],))
        conn.commit()
        cur.close()
        conn.close()
        return HttpResponseRedirect("/profile/")

# Resquests identity (authorize oauth app from github documentation)
def request_identity(request):
    state = str(uuid4())
    params = {"client_id": client_id,
              "response_type": "code",
              "redirect_uri": redirect_uri,
              "state": state,
              "scope": "user"
              }
    return HttpResponseRedirect('https://github.com/login/oauth/authorize?' + urllib.parse.urlencode(params))

# Github request sent via redirect_uri to exchange code and state for the access_token
def callback(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        state= request.GET.get('state')

        #returns the access_token
        post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": redirect_uri,
                 "client_id": client_id,
                 "client_secret": client_secret
                 }
        response = requests.post("https://github.com/login/oauth/access_token", data=post_data)
        at = response.text[13:53]
        name = username(at)
        request.session['name'] = name
        print(name)

        # Connect to database to save the username and access_token if username doesn't already exist
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (name,))
        row = cur.fetchone()
        if not row[0]:
            cur.execute("INSERT INTO users (username, access_token) VALUES (%s, %s)", (name, at))
            conn.commit()
        cur.close()
        conn.close()
        return render(request, "crudapp/home.html", {
            "name": name
        })

# Returns the username
def username(access_token):
    headers = {"Authorization": "token " + str(access_token)}
    response = requests.get("https://api.github.com/user", headers=headers)
    name = response.json()
    return name["login"]


