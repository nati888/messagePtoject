from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from message.models import Message, User


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    list_display = ["id", "sender", "receiver", "subject", "creation_date", "seen"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = ["date_joined", "last_login"]
    list_filter = ["username", "email"]

