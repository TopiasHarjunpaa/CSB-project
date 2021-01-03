from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import User_account
from django.db.models import Q
from django.urls import reverse
import json

# Create your views here.
def index(request):
    return render(request, "safebanking/index.html")

#Check if this needed?
def errorView(request):
    return render(request, "safebanking/error.html")

def logoutView(request):
    del request.session["user_id"]
    return redirect("index")

def loginView(request):
    if request.method == "GET":
        #Check if user has already logged in
        if request.session.get("user_id", None):
            return redirect(reverse("main", kwargs = {"User_account_id" : request.session["user_id"]}))
        else:        
            return render(request, "safebanking/login.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User_account.objects.filter(username = username, password = password)
        #Check if there is user with same credentials on a database
        if len(user) != 0:
            user_id = user[0].id
            request.session["user_id"] = user_id
            return redirect(reverse("main", kwargs = {"User_account_id" : user_id}))
        else:
            return render(request, "safebanking/error.html", {"message" : "Wrong username or password"})

def signinView(request):
    if request.method == "GET":
        return render(request, "safebanking/signin.html")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #Prevent creating a user with already existing username
        if len(User_account.objects.filter(username = username)) != 0:
            return render(request, "safebanking/error.html", {"message" : "User already exist!"})
        else:
            user = User_account.objects.create(username = username, password = password, balance = 1000)
            user_id = user.id
            request.session["user_id"] = user_id
            return redirect(reverse("main", kwargs = {"User_account_id" : user_id}))            
    
def mainView(request, User_account_id):
    user = User_account.objects.get(id = User_account_id)
    users = User_account.objects.all()
    return render(request, "safebanking/main.html", {"users" : users, "owner" : user})

def transferView(request):
    to = User_account.objects.get(id = request.GET.get("to"))
    user = User_account.objects.get(id = int(request.GET.get("user_id"))) #Reason for unsafety (better with session)
    amount = int(request.GET.get("amount"))

    #Prevent adding negative amounts etc...
    user.balance -= amount
    to.balance += amount

    user.save()
    to.save()

    return redirect(reverse("main", kwargs = {"User_account_id" : user.id}))  

