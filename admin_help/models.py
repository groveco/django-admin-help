from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
import markdown


class AdminHelpManager(models.Manager):

    MISSING_LINK_TEXT = "Help doesn't exist for this topic. <a href='%s?type=%s'>Click here</a> to create it or <a href="%s">request it.</a>"

    def _get_ct(self, model):
        return ContentType.objects.filter(model=model.__name__.lower()).first()

    def for_model_class(self, model):
        return self.filter(type=self._get_ct(model)).first()

    def missing_message(self, model):
        self_ct = self._get_ct(self.model)
        url = urlresolvers.reverse("admin:%s_%s_add" % (self_ct.app_label, self_ct.model))
        return mark_safe(AdminHelpManager.MISSING_LINK_TEXT % (url, self._get_ct(model).id, reverse('admin_help_request')))


class AdminHelp(models.Model):

    type = models.ForeignKey(ContentType)
    help = models.TextField()

    objects = AdminHelpManager()

    @property
    def safe_help(self):
        contents = markdown.markdown(self.help)
        link = '<a href="%s">edit</a>' % self.get_absolute_url()
        result = '<br/>'.join([link, contents, link])
        return mark_safe(result)

    def get_absolute_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model),
                                    args=(self.id,))

    class Meta:
        verbose_name_plural = "Admin Help"
