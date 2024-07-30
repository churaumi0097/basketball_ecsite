from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import SignupForm, LoginForm
from .models import CustomUser
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login,authenticate


class Signup(CreateView):
    model = CustomUser
    form_class = SignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("list")



class Login(LoginView):
    form_class = LoginForm
    template_name = "account/login.html"
    success_url = reverse_lazy("list")

    def form_vaild(self,form):
        response = super().form_vaild(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username = username, password = password)
        login(self.request,user)
        return response


class Logout(LogoutView):
    template_name = "account/logout"


class Profile(TemplateView):
    template_name = "account/profile.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.user.email
        context["first_name"] = self.request.user.first_name
        context["last_name"] = self.request.user.last_name
        context["address"] = self.request.user.address
        context["date_joined"] = self.request.user.date_joined
        return context


