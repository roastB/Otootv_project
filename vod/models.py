from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.db import models
from treebeard.mp_tree import MP_Node


# -------------------- 채널 카테고리 --------------------
class Category(MP_Node):
    name = models.CharField(max_length=30)

    #node_order_by = ['name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return 'Category: %s' % self.name

    def __str__(self):
        return self.name


# -------------------- 채널 -------------------

class Channel(models.Model):
    # 1(Channel) : N(Category)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='vod_category_channels', verbose_name=_('Category'))
    name = models.CharField(_('Name'), max_length=100)
    # 1(User 진행자) : N(Channel)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vod_user_channels', verbose_name=_('User'))
    description = models.TextField(_('Description'), max_length=1000, blank=True)
    background_image = models.ImageField(_('Background Image'), upload_to='background_image/%Y/%m/%d', blank=True)
    create_date = models.DateTimeField(_('Channel Create Date'), auto_now_add=True)

    # 배경 이미지 url
    @property
    def get_background_image_url(self):
        if self.background_image:
            return self.background_image.url
        else:
            return '/static/image/default_background_image.jpg'

    # 구독 개수
    @property
    def get_count_subscription_channel(self):
        return self.user_subscription_channels_users.count()

    class Meta:
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')
        ordering = ['-create_date']

    def __str__(self):
        return self.name


# -------------------- 비디오--------------------

class Video(models.Model):
    # 1(Channel) : N(Video)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='vod_channel_videos', verbose_name=_('Channel'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vod_user_videos', verbose_name=_('User') )
    title = models.CharField(_('Title'), max_length=100)
    description = models.TextField(_('Description'), max_length=1000, blank=True)
    video = models.FileField(_('Video'), upload_to='video/%Y/%m/%d', blank=True)
    video_url = models.URLField(_('Video URL'), blank=True)
    views = models.PositiveIntegerField(_('Views'), default=0)
    create_date = models.DateTimeField(_('Create Date'), auto_now_add=True)
    update_date = models.DateTimeField(_('Update date'), auto_now=True)

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
        ordering = ['-update_date']

    # 좋아요 개수
    @property
    def get_count_like_video(self):
        return self.user_like_videos_users.count()

    def __str__(self):
        return self.title

# -------------------- 댓글 --------------------


class Comment(models.Model):
    # 1(User 시청자, 진행자) : N(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vod_user_comments', verbose_name=_('Comment'))
    # 1(Video) : N(Comment)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='vod_video_comments', verbose_name=_('Video'))
    content = models.TextField(_('Content'), max_length=1000)
    create_date = models.DateTimeField(_('Create Date'), auto_now_add=True)
    update_date = models.DateTimeField(_('Update date'), auto_now=True)

    reply = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='vod_reply_comments', verbose_name=_('Reply'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    # 좋아요 개수
    @property
    def get_count_like_comment(self):
        return self.user_like_comments_users.count()

    @property
    def get_short_content(self):
        return self.content[0:70]

    def __str__(self):
        return self.content[0:70]

