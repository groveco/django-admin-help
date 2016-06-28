from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View


class RequestHelpView(View):
    template_name = 'request_help.html'

    def get(self, request, *args, **kwargs):
        ct_id = request.GET.get('ct_id', None)
        ct = ContentType.objects.filter(pk=ct_id).first()
        friendly = '%s - %s' % (ct.app_label, ct.model)
        if ct:
            return render(request, self.template_name, {'ct_id': ct_id, 'friendly': friendly})
        raise Http404("ContentType does not exist")

    def post(self, request, *args, **kwargs):
        ct_id = request.POST.get('ct_id', None)
        inquiry = request.POST.get('inquiry', None)
        ct = ContentType.objects.filter(pk=ct_id).first()
        if ct:
            if hasattr(settings, 'ADMIN_HELP_REQUEST_RECIPIENTS'):
                emails = settings.ADMIN_HELP_REQUEST_RECIPIENTS
            else:
                emails = [a[1] for a in settings.ADMINS]
            friendly = '%s - %s' % (ct.app_label, ct.model)
            subject = 'Django Admin help requested for %s by %s.' % (friendly, request.user)
            send_mail(subject,
                      'Request details: "%s"' % inquiry,
                      'admin-help-request@%s' % settings.DOMAIN_NAME,
                      emails)
        else:
            raise Http404("ContentType does not exist")
