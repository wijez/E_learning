from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from E_learning.app.models import Users, Courses


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'role', 'created_at', 'updated_at')
    fields = ('username', 'name', 'email', 'role', 'image')
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'name', 'role', 'image', 'password1', 'password2')
        }),
    )


admin.site.register(Users, CustomUserAdmin)
admin.site.register(Courses)