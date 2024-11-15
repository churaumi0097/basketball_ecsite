from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model 
from django import forms

CustomUser = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [CustomUser.USERNAME_FIELD] + CustomUser.REQUIRED_FIELDS + ["password1","password2"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = [CustomUser.USERNAME_FIELD] + ["password1","password2"]


