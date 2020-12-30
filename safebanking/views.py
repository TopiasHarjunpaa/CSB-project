from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
from django.db.models import Q
import json

# Create your views here.
def index(request):
    user = request.user
    return render(request, "safebanking/index.html", {"user" : user})