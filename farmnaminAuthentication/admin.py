from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Authentication

User = get_user_model()  # Get the built-in User model

# Unregister default User model first
admin.site.unregister(User)

# Re-register User model with custom options
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'date_joined', 'is_active', 'is_staff')
    search_fields = ('user__username',) 
    list_filter = ('is_staff', 'is_active')

# Register other models
admin.site.register(Authentication)
