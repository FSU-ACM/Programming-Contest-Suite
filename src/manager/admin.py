from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from manager import models


class ProfileAdmin(admin.ModelAdmin):
    """
    Define Profile model interface in Django Admin.
    https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#modeladmin-objects
    """

    # list_display field incompatible with the "user__[first|last]_name" format so cant use Meta
    list_display = ("last_name", "first_name", "role",)
    list_filter = ("role", "checked_in",)
    search_fields = ["user__last_name", "user__first_name"]

    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name


class FacultyResource(resources.ModelResource):
    """
	Attach Faculty model to Django-Import-Export
	https://django-import-export.readthedocs.io/en/latest/getting_started.html#creating-a-resource
	"""
    class Meta:
        model = models.Faculty
        import_id_fields = ('email',)


class FacultyAdmin(ImportExportModelAdmin):
    """
    Django-Import-Export resource admin intrgration
    https://django-import-export.readthedocs.io/en/latest/advanced_usage.html#admin-integration
    """

    resource_class = FacultyResource


class CourseResource(resources.ModelResource):
    """
	Attach Course model to Django-Import-Export
	https://django-import-export.readthedocs.io/en/latest/getting_started.html#creating-a-resource
	"""

    instructor = fields.Field(column_name='instructor',attribute='instructor',widget=ForeignKeyWidget(models.Faculty))
    class Meta:
        model = models.Course


class CourseAdmin(ImportExportModelAdmin):
    """
    Django-Import-Export resource admin intrgration
    https://django-import-export.readthedocs.io/en/latest/advanced_usage.html#admin-integration
    """

    resource_class = CourseResource


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Faculty, FacultyAdmin)
admin.site.register(models.Course, CourseAdmin)
