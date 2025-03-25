from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Ensure this is your custom user model

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'date_joined', 'is_active', 'is_staff')
    search_fields = ('username', 'email',)
    list_filter = ('is_staff', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
