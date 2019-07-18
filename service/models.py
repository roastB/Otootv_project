from django.db import models

from django_summernote import fields as summer_fields
from django_summernote.models import Attachment

from django.dispatch import receiver
from django.db.models.signals import post_delete
from bs4 import BeautifulSoup

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# -------------------- 신고 --------------------

class ReportContent(models.Model):
    CHOICES_CATEGORY = (
        (None, _('Category')),
        ('Channel', _('Channel')),
        ('Video', _('Video')),
        ('Comment', _('Comment')),
    )
    category = models.CharField(_('Category'), max_length=7, choices=CHOICES_CATEGORY)
    # 1(User 관리자) : N(ReportContent)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='service_owner_reportcontents', verbose_name=_('Staff User'))
    content = models.CharField(_('Title'), max_length=100)
    update_date = models.DateTimeField(_('Update Date'), auto_now=True)

    belong_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='service_belong_to_reportcontents', verbose_name=_('Belong To'))

    class Meta:
        verbose_name = _('Report Content')
        verbose_name_plural = _('Report Contents')

    def __str__(self):
        return self.content


class Report(models.Model):
    category = models.CharField(_('Category'), max_length=7, blank=True)
    # 1(User 시청자. 진행자(채널 주인) : N(Report)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='service_user_reports', verbose_name=_('User'))
    # 1(ReportContent) : N(Report)
    content = models.ForeignKey(ReportContent, on_delete=models.CASCADE,
                                related_name='service_content_reports', verbose_name=_('Content'))
    create_date = models.DateTimeField(_('Create Date'), auto_now_add=True)

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        ordering = ['-create_date']

    # category 자동 추가
    def save(self, *args, **kwargs):
        self.category = self.content.category
        super(Report, self).save(*args, **kwargs)


# -------------------- 도움말 --------------------

class Help(models.Model):
    # 1(User 관리자) : N(HelpQuestion)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='service_owner_helpquestions', verbose_name=_('Staff User'))

    question = models.CharField(_('Question'), max_length=100)
    content = summer_fields.SummernoteTextField(verbose_name=_('Content'), blank=True)
    update_date = models.DateTimeField(_('Update Date'), auto_now=True)

    belong_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='service_belong_to_helpquestions',  verbose_name=_('Belong To'))

    class Meta:
        verbose_name = _('Help')
        verbose_name_plural = _('Help')
        verbose_name = "Help"

    def __str__(self):
        return self.question


# -------------------- 문의하기 --------------------

class Inquiry(models.Model):
    # 1(User 로그인) : N(Inquiry)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='service_user_inquiries', verbose_name=_('User'))

    title = models.CharField(_('Title'), max_length=100)
    content = summer_fields.SummernoteTextField(verbose_name=_('Content'))
    views = models.PositiveIntegerField(_('Views'), default=0)
    create_date = models.DateTimeField(_('Create Date'), auto_now_add=True)
    update_date = models.DateTimeField(_('Update date'), auto_now=True)

    class Meta:
        verbose_name = _('Inquire')
        verbose_name_plural = _('Inquires')
        ordering = ['-update_date']

    def __str__(self):
        return self.title


class Reply(models.Model):
    # 1(User 관리자) : 1(Reply)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='service_user_replies',  verbose_name=_('Staff User'))
    # 1(Inquiry) : 1(Reply)
    inquiry = models.OneToOneField(Inquiry, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='service_inquiry_reply',  verbose_name=_('Inquire'))

    content = summer_fields.SummernoteTextField(verbose_name=_('Content'))
    update_date = models.DateTimeField(_('Update date'), auto_now=True)

    class Meta:
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')


# -------------------- handler --------------------

# Help 이미지 삭제
@receiver(post_delete, sender=Help)
def service_delete_handler(sender, **kwargs):
    listing_help = kwargs['instance']
    if listing_help.summer_field:
        soup = BeautifulSoup(listing_help.summer_field, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            storage, path = result.file.storage, result.file.path
            storage.delete(path)
            result.delete()

# Inquiry 이미지 삭제
@receiver(post_delete, sender=Inquiry)
def service_delete_handler(sender, **kwargs):
    listing_inquiry = kwargs['instance']
    if listing_inquiry.summer_field:
        soup = BeautifulSoup(listing_inquiry.summer_field, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            storage, path = result.file.storage, result.file.path
            storage.delete(path)
            result.delete()


# Reply 이미지 삭제
@receiver(post_delete, sender=Reply)
def service_delete_handler(sender, **kwargs):
    listing_reply = kwargs['instance']
    if listing_reply.summer_field:
        soup = BeautifulSoup(listing_reply.summer_field, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            storage, path = result.file.storage, result.file.path
            storage.delete(path)
            result.delete()
