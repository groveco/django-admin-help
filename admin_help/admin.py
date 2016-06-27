from django.contrib import admin
from admin_help.models import AdminHelp
from admin_help.forms import AdminHelpAdminForm
from django.contrib.contenttypes.models import ContentType


class AdminHelpAdmin(admin.ModelAdmin):
    form = AdminHelpAdminForm

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """ Order the drop down by """
        if db_field.name == "type":
            kwargs["queryset"] = ContentType.objects.all().order_by('model')
        return super(AdminHelpAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(AdminHelp, AdminHelpAdmin)