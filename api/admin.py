from django.contrib import admin
from api.models import CustomUserModel


@admin.register(CustomUserModel)
class CustomUserModelAdmin(admin.ModelAdmin):
    list_display=('id','username','email','first_name','last_name')
