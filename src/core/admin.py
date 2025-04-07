from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from . import models

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):
    """
    Attach User model to Django-Import-Export
    https://django-import-export.readthedocs.io/en/latest/getting_started.html#creating-a-resource
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active', 'profile__checked_in')


class UserAdmin(ImportExportModelAdmin):
    """
    Django-Import-Export resource admin intrgration
    https://django-import-export.readthedocs.io/en/latest/advanced_usage.html#admin-integration
    """
    
    resource_class = UserResource
    list_display = ("last_name", "first_name", "username", "email", "is_active",)
    list_filter = ("is_active",)
    search_fields = ["last_name", "first_name", "username", "email"]


class SponsorAdmin(admin.ModelAdmin):
    """
    Define Sponsor model interface in Django Admin.
    https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#modeladmin-objects
    """

    list_display = ('name', 'url', 'logo_thumbnail', 'message')
    search_fields = ['name', 'message']

    def logo_thumbnail(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" style="width: 300px; height: auto;" />')
        return '-'

# Re-register User model for django-import-export integration
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(models.Sponsor, SponsorAdmin)
