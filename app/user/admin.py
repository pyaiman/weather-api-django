"""
Customized django-admin
"""

from django.contrib import admin
from .models import User
from django.utils.translation import gettext_lazy as _

class UserAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['email', 'name']    
    readonly_fields = ['last_login']

admin.site.register(User, UserAdmin)
