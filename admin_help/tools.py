from django.contrib.admin import site
import object_tools
from admin_help.models import AdminHelp


class Help(object_tools.ObjectTool):
    name = 'help'
    label = 'Help'

    def view(self, request, extra_context=None):
        modeladmin = site._registry.get(self.model)
        help_model = AdminHelp.objects.for_model_class(self.model)
        if help_model:
            modeladmin.message_user(request,
                                    help_model.safe_help,
                                    extra_tags='safe',
                                    level='success')
        else:
            modeladmin.message_user(request,
                                    AdminHelp.objects.missing_message(self.model),
                                    extra_tags='safe',
                                    level='warning')

        return modeladmin.changelist_view(request)

object_tools.tools.register(Help)