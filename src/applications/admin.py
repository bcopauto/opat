from django.contrib import admin
from .models import Application

#admin.site.register(Application)
class ReadOnlyAdminMixin:

    def has_add_permission(self, request):
        return True

    def has_change_permision(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

@admin.register(Application)
class ProjectAdmin(ReadOnlyAdminMixin,admin.ModelAdmin):
    list_display = ("app_name", "id", "app_description", "app_is_active",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['app_name'].disabled = True
            form.base_fields['app_description'].disabled = True
            form.base_fields['app_is_active'].disabled = True
        return form   
