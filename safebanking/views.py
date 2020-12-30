from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import User_account
from django.db.models import Q
import json

# Create your views here.
def index(request):
    return render(request, "safebanking/index.html")

def loginView(request):
    if request.method == "GET":
        return render(request, "safebanking/login.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User_account.objects.filter(username = username, password = password)
        if user is not None:
            return redirect("/main")
        else:
            return redirect("/error", {"message" : "Wrong username or password"})

def signinView(request):
    if request.method == "GET":
        return render(request, "safebanking/signin.html")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if User_account.objects.filter(username = username) is not None:
            return redirect("/error", {"message" : "User already exist!"})
        else:
            user = User_account.objects.create(username = username, password = password, balance = 1000)
            return redirect("/main")
    
def mainView(request):
    return render(request, "safebanking/main.html")
