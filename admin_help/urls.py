from django.conf.urls import url
from admin_help.views import RequestHelpView
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
   url(r'help-request/$', staff_member_required(RequestHelpView.as_view()), name='admin_help_request'),
]
