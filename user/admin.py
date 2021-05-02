from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'displayName')
    list_filter = ('id', 'displayName')
    search_fields = ('id', 'displayName')
