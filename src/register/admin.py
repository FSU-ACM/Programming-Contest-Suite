from django.contrib import admin

from register import models


class TeamAdmin(admin.ModelAdmin):
    """
    Define Team model interface in Django Admin.
    https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#modeladmin-objects
    """

    list_display = ("name", "num_members", "division", "faculty")
    list_filter = ("division", "faculty")
    search_fields = ["name"]

admin.site.register(models.Team, TeamAdmin)