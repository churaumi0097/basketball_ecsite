from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.Login.as_view(),name = "login"),
    path("logout/",views.Logout.as_view(),name = "logout"),
    path("signup/",views.Signup.as_view(),name = "signup"),
    path("profile/",views.Profile.as_view(),name = "profile"),
]