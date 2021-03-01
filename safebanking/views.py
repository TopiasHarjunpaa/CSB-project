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
from random import sample
from string import digits

def index(request):
    #Check if user has already logged in
    if request.session.get("user_id", None):
        return redirect(reverse("main", kwargs = {"User_account_id" : request.session["user_id"]}))
    else:        
        return render(request, "safebanking/index.html")

def errorView(request):
    return render(request, "safebanking/error.html")

def logoutView(request):
    del request.session["user_id"]
    del request.session["admin"]

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
            #Create sessions
            user_id = user[0].id
            request.session["user_id"] = user_id
            if user[0].status == 2:
                request.session["admin"] = True
            else:
                request.session["admin"] = False
            return redirect(reverse("main", kwargs = {"User_account_id" : user_id}))
        else:
            request.session["error"] = "Wrong username or password"
            return redirect("error")

def signinView(request):
    if request.method == "GET":
        #Check if user has already logged in
        if request.session.get("user_id", None):
            return redirect(reverse("main", kwargs = {"User_account_id" : request.session["user_id"]}))
        else:        
            return render(request, "safebanking/signin.html")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #Prevent creating a user with already existing username
        if len(User_account.objects.filter(username = username)) != 0:
            request.session["error"] = "User already exist!"
            return redirect("error") 
        else:
            #Draw account number
            an = "".join(sample(list(digits), 4)) + "-" + "".join(sample(list(digits), 4))
            user = User_account.objects.create(username = username, password = password, balance = 1000, account_number = an, status = 1) 
            #Create sessions
            user_id = user.id
            request.session["user_id"] = user_id
            if user.status == 2:
                request.session["admin"] = True
            else:
                request.session["admin"] = False

            return redirect(reverse("main", kwargs = {"User_account_id" : user_id}))            

def adminView(request, User_account_id):
    user = User_account.objects.get(id = User_account_id)
    users = User_account.objects.all()
    
    if request.method == "POST":
        #Add admin rights
        if request.POST.get("new_admin_id") != None:
            new_admin = User_account.objects.get(id = request.POST.get("new_admin_id"))
            new_admin.status = 2
            new_admin.save()
        #Remove admin rights
        if request.POST.get("old_admin_id") != None:
            old_admin = User_account.objects.get(id = request.POST.get("old_admin_id"))
            old_admin.status = 1
            old_admin.save()

    return render(request, "safebanking/admin.html", {"users" : users, "owner" : user})

def mainView(request, User_account_id):
    user = User_account.objects.get(id = User_account_id)

    if request.method == "POST":
        motto = request.POST.get("motto")
        user.motto = motto
        user.save()
        return redirect(reverse("main", kwargs = {"User_account_id" : User_account_id}))

    return render(request, "safebanking/main.html", {"owner" : user})

def transferView(request, User_account_id):
    user = User_account.objects.get(id = User_account_id)
    users = User_account.objects.all()
    request.session["message"] = ""

    #Check that form is filled
    if request.GET.get("to") != None and request.GET.get("amount") != None:
        to = User_account.objects.get(id = request.GET.get("to"))
        amount = int(request.GET.get("amount"))

        #Prevent adding negative amounts etc...
        if amount >= 0:
            user.balance -= amount
            to.balance += amount
            user.save()
            to.save()
            request.session["message"] = "Succesfull transfer"      
        else:
            request.session["message"] = "Transfer failed"
    
    return render(request, "safebanking/transfer.html", {"users" : users, "owner" : user})    

def depositView(request, User_account_id):
    user = User_account.objects.get(id = User_account_id)
    request.session["message"] = ""
    if request.method == "GET":
        return render(request, "safebanking/deposit.html", {"owner" : user})

    if request.method == "POST":
        amount = request.POST.get("amount")
        try:
            with connection.cursor() as cursor:
                #In order to see balance update, it requires refreshing the page.
                cursor.execute(f"UPDATE safebanking_user_account SET balance = balance + {amount} WHERE id = {User_account_id}")
                request.session["message"] = "Succesfull deposit"
        except:
            request.session["message"] = "Failed" 

        return render(request, "safebanking/deposit.html", {"owner" : user})       

