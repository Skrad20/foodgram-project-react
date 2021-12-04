from django.contrib import admin
from .models import (
    CustomUser,
    Follow,
)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name']
    search_fields = ['^email', '^first_name']


admin.site.register(Follow)
admin.site.register(CustomUser, CustomUserAdmin)
