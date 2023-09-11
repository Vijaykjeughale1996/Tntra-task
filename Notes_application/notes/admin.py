from django.contrib import admin
from .models import Note, Image, NoteShare, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'is_staff', 'mobile_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'mobile_number'),
        }),
    )
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'updated_at')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('note', 'image')

@admin.register(NoteShare)
class NoteShareAdmin(admin.ModelAdmin):
    list_display = ('note', 'user')