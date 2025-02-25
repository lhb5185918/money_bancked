from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nick_name', 'created_at')
    search_fields = ('username', 'nick_name')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
