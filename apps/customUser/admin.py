from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'role')  # Campos que se mostrarán en la lista de objetos


admin.site.register(User, UserAdmin)