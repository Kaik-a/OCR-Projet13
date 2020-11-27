"""Urls for accounts"""
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("authenticate/", views.login, name="authenticate"),
    path("check_mail/", views.check_mail, name="check_mail"),
    path("delete-friend/<friend>", views.delete_friend, name="delete-friend"),
    path("friends", views.friends, name="friends"),
    path("login/", views.get_user_info, name="login"),
    path("logout/", views.sign_out, name="logout"),
    path("reset_password/<user>", views.reset_password, name="reset_password"),
    path("send_reset/<user>", views.send_reset, name="send_reset"),
    path("subscription/", views.subscribe, name="subscription"),
    path("user_account/", views.user_account, name="user_account"),
    path("validate/<guid>", views.validate, name="validate"),
]
