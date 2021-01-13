from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("login/", views.loginView, name = "login"),
    path("signin/", views.signinView, name = "signin"),
    path("main/<int:User_account_id>/", views.mainView, name = "main"),
    path("error/", views.errorView, name = "error"),
    path("logout/", views.logoutView, name = "logout"),
    path("transfer/<int:User_account_id>/", views.transferView, name = "transfer"),
    path("deposit/<int:User_account_id>/", views.depositView, name = "deposit")
]