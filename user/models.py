from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser, PermissionsMixin, Group)
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

from phonenumber_field.modelfields import PhoneNumberField
from vod.models import Channel, Video, Comment


# -------------------- User --------------------


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, first_name, last_name, date_of_birth, gender, email,
                     password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given id must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, first_name=first_name, last_name=last_name,
                          date_of_birth=date_of_birth, gender=gender, email=email,
                          is_staff=is_staff, is_active=True, is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, first_name, last_name, date_of_birth, gender, email, password=None, **extra_fields):
        return self._create_user(username, first_name, last_name, date_of_birth, gender, email, password,
                                 False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, ' ', ' ', None, ' ', email, password,
                                 True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Id'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, digits and blank. /+/-/_ only.'),
                                validators=[validators.RegexValidator(r'^[\w.+-]+$', _('Enter a valid id.'), 'invalid')],
                                error_messages={'unique': _("A user with that id already exists.")})
    first_name = models.CharField(_('First name'), max_length=30)
    last_name = models.CharField(_('Last name'), max_length=150)
    date_of_birth = models.DateField(_('Date of birth'),null=True)
    CHOICES_GENDER = (
        (None, _('Gender')),
        ('m', _('Male')),
        ('f', _('Female')))
    gender = models.CharField(_('Gender'), max_length=1, choices=CHOICES_GENDER)
    email = models.EmailField(_('Email'), unique=True,
                              error_messages={'unique': _("A user with that email already exists.")})
    phone_number = PhoneNumberField(_('Phone number'),blank=True)
    profile_image = models.ImageField(_('Profile image'), upload_to='profile_image/%Y/%m/%d', blank=True)

    # 주소
    address1 = models.CharField(_('Address 1'), max_length=100, blank=True,
                                help_text=_('Street address, P.O box, company name, c/o'))         # 도로명주소, 우편박스, 회사이름, 대신 받는 사람
    address2 = models.CharField(_('Address 2'), max_length=100, blank=True,
                                help_text=_('Apartment, suite, unit, building, floor'))             # 아파트, 실, 건물, 빌딩, 층
    city = models.CharField(_('City'), max_length=50, blank=True)                                       # 도시
    state_province_region = models.CharField(_('State/Province/Region'), max_length=50, blank=True)   # 주/도/지역
    zip = models.CharField(_('ZIP'), max_length=20, blank=True)                                         # 우편번호
    city_region = models.CharField(_('City/Region'), max_length=50, blank=True)                        # 국가/지역

    # 계좌
    bank_name = models.CharField(_('Bank Name'), max_length=30, blank=True)
    account_holder = models.CharField(_('Account Holder'), max_length=180, blank=True)
    account_number = models.CharField(_('Account Number'), max_length=30, blank=True)

    is_staff = models.BooleanField(_('Staff'), default=False)
    is_creator = models.BooleanField(_('Creator'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('Date Join'), default=timezone.now)

    # 채널 구독
    # N(User 시청자) : M(Channel)
    subscription_channels = models.ManyToManyField(Channel, blank=True, related_name='user_subscription_channels_users', verbose_name=_('Subscription Channel'))
    # 좋아요 비디오
    # N(User 시청자, 진행자(own)) : M(Video)
    like_videos = models.ManyToManyField(Video, blank=True, related_name='user_like_videos_users', verbose_name=_('Liked Video'))
    # 좋아요 댓글
    # N(User 시청자, 진행자(own)) : M(Comment)
    like_comments = models.ManyToManyField(Comment, blank=True, related_name='user_like_comments_users', verbose_name=_('Liked Comment'))

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['date_joined']

    #  장고 제공 함수 / 삭제 가능
    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # 프로필 이미지 url
    @property
    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            return '/static/img/default_profile_image.jpg'

    # 채널 구독 개수
    @property
    def get_count_subscription_channels(self):
        return self.subscription_channels.count()

    # 좋아요 비디오 개수
    @property
    def get_count_like_videos(self):
        return self.like_videos.count()


# -------------------- 구독 --------------------

class Subscription(models.Model):
    # 1(User 시청자) : 1(Subscription)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_user_subscription', verbose_name=_('User'))
    subscription_create_date = models.DateTimeField(_('Subscription Create Date'), default=timezone.now)
    subscription_expire_date = models.DateTimeField(_('Subscription Expire Date'), blank=True)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        ordering = ['subscription_expire_date']

    # 구독 시 시청자 그룹에 자동 추가
    def save(self, *args, **kwargs):
        if not self.id:
            self.subscription_expire_date = self.subscription_create_date + timezone.timedelta(days=30)
        super(Subscription, self).save(*args, **kwargs)

