from django.contrib import admin
from vod.models import Channel, Video, Comment

# Register your models here.


class VideoInline(admin.StackedInline):
    model = Video
    extra = 0


class ChannelAdmin(admin.ModelAdmin):
    inlines = [VideoInline]
    fieldsets = (
        (None, {'fields': ('category', 'name', 'user', 'description' )}),
        ('Background image', {'fields': ['background_image']}),
    )
    list_display = ( 'category', 'name', 'user', 'create_date', 'get_count_subscribe_channel')
    list_filter = ['category']


class VideoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('channel', 'title', 'description')}),
        ('Video', {'fields': ('video', 'video_url')}),
        ('Views', {'fields': ['views']}),
    )
    list_display = ('channel', 'title', 'update_date', 'get_count_like_video', 'views')


class CommentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'video', 'content')}),
        ('Reply Comment', {'fields': ['reply']}),
    )
    list_display = ('user', 'video',  'get_short_content', 'reply', 'update_date', 'get_count_like_comment')


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Comment, CommentAdmin)