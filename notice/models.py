from django.db import models
from django_summernote import fields as summer_fields

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# -------------------- 공지사항 --------------------
class Notice(models.Model):
    title = models.CharField(_('Title'),  max_length=100)
    # 1(User 관리자) : N(Notice)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='notice_owner_notices', verbose_name=_('Staff user'))
    content = summer_fields.SummernoteTextField(verbose_name=_('Content'))
    views = models.PositiveIntegerField(_('Views'), default=0)
    create_date = models.DateTimeField(_('Create Date'), auto_now_add=True)
    update_date = models.DateTimeField(_('Update date'), auto_now=True)

    class Meta:
        verbose_name = _('Notice')
        verbose_name_plural = _('Notices')
        ordering = ['-update_date']

    def __str__(self):
        return self.title
