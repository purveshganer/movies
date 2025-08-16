from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name="login_page"),
    path("register/", views.register_page, name="register_page"),

    # APIs
    path("api/register/", views.register_api, name="register_api"),
    path("api/login/", views.login_api, name="login_api"),
]