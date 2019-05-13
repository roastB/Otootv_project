from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User, Subscribe
from user.forms import UserCreationForm


class UsersAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Profile image', {'fields': ['profile_image']}),
        ('Personal info', {'fields': ('first_name', 'last_name','date_of_birth', 'gender', 'email','phone_number')}),
        ('Address', {'fields': ('address1', 'address2', 'city', 'state_province_region', 'zip', 'city_region')}),
        ('Account', {'fields': ('bank_name', 'account_number', 'account_holder')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Subscribe', {'fields': ('subscribe_channels', 'like_videos', 'like_comments')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'gender',
                       'date_of_birth', 'email', 'phone_number')}),
    )
    add_form = UserCreationForm
    filter_horizontal = ('groups', 'user_permissions', 'subscribe_channels', 'like_videos', 'like_comments')
    list_display = ('username', 'email', 'date_joined', 'is_active', 'get_count_subscribe_channels', 'get_count_like_videos')
    list_filter = ('is_active', 'groups', 'is_staff')
    search_fields = ('username', 'email')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribe_create_date', 'subscribe_expire_date')


admin.site.register(User, UsersAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
