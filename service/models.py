from django.db import models
from vod.models import Channel, Video, Comment
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# -------------------- 신고 --------------------
class ReportContent(models.Model):
    CHOICES_CATEGORY = (
        (None, _('Category')),
        ('ch', _('Channel')),
        ('vi', _('Video')),
        ('co', _('Comment')),
    )
    category = models.CharField(_('Category'), max_length=2, choices=CHOICES_CATEGORY)
    # 1(User 관리자) : N(ReportContent)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='service_owner_reportcontents', verbose_name=_('Staff User'))
    content = RichTextUploadingField(_('Content'))
    update_date = models.DateTimeField(_('Update Date'), auto_now=True)

    belong_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='service_belong_to_reportcontents', verbose_name=_('Belong To'))

    class Meta:
        verbose_name = _('Report Content')
        verbose_name_plural = _('Report Contents')

    def __str__(self):
        return self.content


class Report(models.Model):
    # 1(User 시청자. 진행자(채널 주인) : N(Report)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='service_user_reports', verbose_name=_('User'))

    # 1(channel) : N(Report)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='service_channel_reports', verbose_name=_('Channel'))
    # 1(Video) : N(Report)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='service_video_reports', verbose_name=_('Video'))
    # 1(comment) : N(Report)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,  null=True, blank=True,
                                related_name='service_comment_reports', verbose_name=_('Comment'))

    # 1(ReportContent) : N(Report)
    content = models.ForeignKey(ReportContent, on_delete=models.CASCADE,
                                related_name='service_content_reports', verbose_name=_('Content'))
    create_date = models.DateTimeField(_('Create Date'), auto_now_add=True)

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        ordering = ['-create_date']


# -------------------- 도움말 --------------------
class HelpQuestion(models.Model):
    # 1(User 관리자) : N(HelpQuestion)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='service_owner_helpquestions', verbose_name=_('Staff User'))

    question = models.CharField(_('Question'), max_length=100)
    update_date = models.DateTimeField(_('Update Date'), auto_now=True)

    belong_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='service_belong_to_helpquestions',  verbose_name=_('Belong To'))

    class Meta:
        verbose_name = _('Help Question')
        verbose_name_plural = _('Help Questions')
        verbose_name = "Help"

    def __str__(self):
        return self.question


class HelpAnswer(models.Model):
    # 1(User 관리자) : N(HelpAnswer)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='service_owner_helpanswers',  verbose_name=_('Staff User'))

    # 1(HelpQuestion) : 1(HelpAnswer)
    question = models.OneToOneField(HelpQuestion, on_delete=models.CASCADE,
                                    related_name='service_question_helpanswer',  verbose_name=_('Question'))

    answer = RichTextUploadingField( verbose_name=_('Answer'))
    update_date = models.DateTimeField(_('Update Date'), auto_now=True)

    class Meta:
        verbose_name = _('Help Answer')
        verbose_name_plural = _('Help Answer')


# -------------------- 문의하기 --------------------
class Inquiry(models.Model):
    # 1(User 로그인) : N(Inquiry)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='service_user_inquiries', verbose_name=_('User'))

    title = models.CharField(_('Title'), max_length=100)
    content = RichTextUploadingField(verbose_name=_('Content'))
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

    content = RichTextUploadingField( verbose_name=_('Content'))
    update_date = models.DateTimeField(_('Update date'), auto_now=True)

    class Meta:
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')

