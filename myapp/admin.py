from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Account

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'nick_name', 'date_joined', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('nick_name', 'email', 'avatar', 'description')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'nick_name', 'email')
    ordering = ('username',)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_type', 'balance', 'created_at')
    list_filter = ('account_type', 'created_at')
    search_fields = ('account_name',)

admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
