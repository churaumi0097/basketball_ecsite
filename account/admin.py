from django.contrib import admin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email","last_name","first_name","is_staff")
    list_filter = ("date_joined",)