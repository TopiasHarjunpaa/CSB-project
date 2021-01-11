from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import User_account
from django.db.models import Q
from django.urls import reverse
from django.db import connection
import json

# Create your views here.
def index(request):
    return render(request, "safebanking/index.html")

def errorView(request):
    return render(request, "safebanking/error.html")

def logoutView(request):
    del request.session["user_id"]
    return redirect("index")

@csrf_exempt
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
            request.session["error"] = "Wrong username or password"
            return redirect("error")
            #return render(request, "safebanking/error.html", {"message" : "Wrong username or password"})

@csrf_exempt
def signinView(request):
    if request.method == "GET":
        return render(request, "safebanking/signin.html")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #Prevent creating a user with already existing username
        if len(User_account.objects.filter(username = username)) != 0:
            request.session["error"] = "User already exist!"
            return redirect("error") 
            #return render(request, "safebanking/error.html", {"message" : "User already exist!"})
        else:
            user = User_account.objects.create(username = username, password = password, balance = 1000)
            user_id = user.id
            request.session["user_id"] = user_id
            return redirect(reverse("main", kwargs = {"User_account_id" : user_id}))            
    
def mainView(request, User_account_id):
    user = User_account.objects.get(id = User_account_id)
    return render(request, "safebanking/main.html", {"owner" : user})

@csrf_exempt
def transferView(request, User_account_id):
    user = User_account.objects.get(id = User_account_id)
    users = User_account.objects.all()
    request.session["message"] = ""
    if request.method == "GET":
        return render(request, "safebanking/transfer.html", {"users" : users, "owner" : user})

    if request.method == "POST":
        to = User_account.objects.get(id = request.POST.get("to"))
        amount = int(request.POST.get("amount"))

        #Prevent adding negative amounts etc...
        if amount >= 0:
            user.balance -= amount
            to.balance += amount
            user.save()
            to.save()
            request.session["message"] = "Succesfull transfer"      
        else:
            request.session["message"] = "Transfer failed"
        
        #Maybe redirect back to mainpage?
        return render(request, "safebanking/transfer.html", {"users" : users, "owner" : user})    

@csrf_exempt
def depositView(request, User_account_id):
    user = User_account.objects.get(id = User_account_id)
    request.session["message"] = ""
    if request.method == "GET":
        return render(request, "safebanking/deposit.html", {"owner" : user})

    if request.method == "POST":
        amount = request.POST.get("amount")
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE safebanking_user_account SET balance = balance + {amount} WHERE id = {User_account_id}")
                request.session["message"] = "Succesfull deposit" 
        except:
            request.session["message"] = "Failed" 

        #Maybe redirect back to mainpage?
        return render(request, "safebanking/deposit.html", {"owner" : user})       

