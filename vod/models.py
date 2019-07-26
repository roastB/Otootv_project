from django.db import models
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from django.db.models.signals import post_delete


# -------------------- 채널 카테고리 form--------------------
class Category(forms.Form):

    Category1 = (
        ('edu', _('Education')),
        ('trav', _('Travel')),
        ('game', _('Game')),
        ('shop', _('Shopping')),
        ('fitn', _('Fitness'))
    )

    # -------------------- 교육--------------------
    Edu_Level2 = (
        ('elem', _('Elementary School')),
        ('midd', _('Middle School')),
        ('high', _('High school')),
        ('sky', _('Sky Castle')),
        ('genr', _('General'))
    )

    Edu_Lev_Elementary3 = (
        ('eng', _('English')),
        ('kor', _('Korean')),
        ('math', _('Math')),
        ('scie', _('Science')),
        ('etc', _('Etc'))
    )

    Edu_Lev_Middle3 = (
        ('eng', _('English')),
        ('kor', _('Korean')),
        ('math', _('Math')),
        ('scie', _('Science')),
        ('ssat', 'SSAT'),
        ('etc', _('Etc'))
    )

    Edu_Lev_High3 = (
        ('eng', _('English')),
        ('kor', _('Korean')),
        ('math', _('Math')),
        ('scie', _('Science')),
        ('sat', 'SAT'),
        ('act', 'ACT'),
        ('etc', _('Etc'))
    )

    Edu_Lev_General3 = (
        ('toelc', _('TOEIC')),
        ('toefl', _('TOEFL')),
        ('teps', _('TEPS')),
        ('etc', _('Etc'))
    )

    # -------------------- 여행-------------------

    Tra_Country2 = (
        ('nora', _('North America')),
        ('soua', _('South America')),
        ('euro', _('Europe')),
        ('aust', _('Australia')),
        ('etc', _('Etc'))
    )

    # -------------------- 쇼핑-------------------
    Sho_Category = (
            ('clo', _('clothing')),
            ('acc', _('Accessories')),
            ('etc', _('Etc'))
    )

    Category1 = forms.ChoiceField(label=_("Category"), choices=Category1, widget=forms.RadioSelect())

    Edu_Level2 = forms.ChoiceField(label=_("Education Level"), choices=Edu_Level2, widget=forms.RadioSelect())
    Edu_Lev_Elementary3 = forms.ChoiceField(label=_("Elementary School Course"), choices=Edu_Lev_Elementary3, widget=forms.RadioSelect())
    Edu_Lev_Middle3 = forms.ChoiceField(label=_("Middle School Course"), choices=Edu_Lev_Middle3, widget=forms.RadioSelect())
    Edu_Lev_High3 = forms.ChoiceField(label=_("High School Course"), choices=Edu_Lev_High3, widget=forms.RadioSelect())
    Edu_Lev_General3 = forms.ChoiceField(label=_("General Course"), choices=Edu_Lev_General3, widget=forms.RadioSelect())

    Tra_Country2 = forms.ChoiceField(label=_("Travel Country"), choices=Tra_Country2, widget=forms.RadioSelect())
    Sho_Category = forms.ChoiceField(label=_("Shopping Category"),choices=Sho_Category, widget=forms.RadioSelect())


# -------------------- 채널 -------------------

class Channel(models.Model):

    category1 = models.CharField(_('Category1'), max_length=5)
    category2 = models.CharField(_('Category2'), max_length=5, blank=True)
    category3 = models.CharField(_('Category3'), max_length=5, blank=True)

    name = models.CharField(_('Name'), max_length=100)
    # 1(User 진행자) : N(Channel)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vod_owner_channels', verbose_name=_('User'))
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
    def get_count_subscribe_channel(self):
        return self.user_subscribe_channels_users.count()

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


# -------------------- handler --------------------

# 채널 배경 이미지 삭제
@receiver(post_delete, sender=Channel)
def photo_delete_handler(sender, **kwargs):
    listing_image = kwargs['instance']
    if listing_image.background_image:
        storage, path = listing_image.background_image.storage, listing_image.background_image.path
        storage.delete(path)


# 비디오 삭제
@receiver(post_delete, sender=Video)
def video_delete_handler(sender, **kwargs):
    listing_video = kwargs['instance']
    if listing_video.video:
        storage, path = listing_video.video.storage, listing_video.video.path
        storage.delete(path)
