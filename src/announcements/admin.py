from django.contrib import admin

from announcements import models


class AnnouncementAdmin(admin.ModelAdmin):
    """
    Define Announcement model interface in Django Admin.
    https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#modeladmin-objects
    """

    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(models.Announcement, AnnouncementAdmin)
