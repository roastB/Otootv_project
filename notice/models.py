from django.db import models
from django_summernote.models import Attachment
from django_summernote import fields as summer_fields

from django.dispatch import receiver
from django.db.models.signals import post_delete
from bs4 import BeautifulSoup

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# -------------------- 공지사항 --------------------
class Notice(models.Model):
    title = models.CharField(_('Title'),  max_length=100)
    # 1(User 관리자) : N(Notice)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='notice_owner_notices', verbose_name=_('Staff Name'))
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


# -------------------- handler --------------------

# 이미지 삭제
@receiver(post_delete, sender=Notice)
def notice_delete_handler(sender, **kwargs):
    listing_notice = kwargs['instance']
    if listing_notice.content:
        soup = BeautifulSoup(listing_notice.content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            storage, path = result.file.storage, result.file.path
            storage.delete(path)
            result.delete()




