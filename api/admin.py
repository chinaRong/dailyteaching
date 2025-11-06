from django.contrib import admin
from .models import UserData


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'created_at')
    readonly_fields = ('created_at',)
