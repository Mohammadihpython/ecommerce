from django.contrib import admin
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone_number", "date_joined"]
    list_filter = ["date_joined"]
    ordering = ["-date_joined"]
    search_fields = ["phone_number", "last_name", "first_name"]
