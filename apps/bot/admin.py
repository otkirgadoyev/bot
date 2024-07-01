from django.contrib import admin
from .models import User, File


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "telegram_id", "full_name", "active"]


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["id", "file", "category"]
    list_editable = ["category"]