from django.contrib import admin

from core.models import Note, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Note)
class ChatAdmin(admin.ModelAdmin):
    pass
