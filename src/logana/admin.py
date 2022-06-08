from django.contrib import admin
from .models import Project,Domain


admin.site.register(Domain)


class ReadOnlyAdminMixin:

    def has_add_permission(self, request):
        return True

    def has_change_permision(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

@admin.register(Project)
class ProjectAdmin(ReadOnlyAdminMixin,admin.ModelAdmin):
    list_display = ("project_name", "id", "creation_date", "project_description", "is_active", "app_id")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['project_name'].disabled = True
            form.base_fields['project_description'].disabled = True
            form.base_fields['is_active'].disabled = True
            form.base_fields['is_shared'].disabled = True
            #These fields wil be populated in the background once project is start
            form.base_fields['logs_start_date'].disabled = True
            form.base_fields['logs_end_date'].disabled = True
            form.base_fields['no_rows'].disabled = True
            form.base_fields['no_cols'].disabled = True
            
        return form




