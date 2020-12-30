from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("login/", views.loginView, name = "login"),
    path("signin/", views.signinView, name = "signin"),
    path("main/", views.mainView, name = "main")
]