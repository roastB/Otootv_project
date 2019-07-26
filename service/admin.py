from django.contrib import admin
from service.models import VideoReport, CommentReport, Help, Inquiry, Reply


class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 0


class VideoReportAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['user']}),
        ('Report_Video', {'fields': ['video']}),
        ('Content', {'fields': ('category', 'content')}),
    )
    list_display = ['user', 'video', 'category', 'create_date']
    list_filter = ['video', 'category']


class CommentReportAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['user']}),
        ('Report_Video', {'fields': ['comment']}),
        ('Content', {'fields': ('category', 'content')}),
    )
    list_display = ['user', 'comment', 'category', 'create_date']
    list_filter = ['category']


class HelpAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('question', 'content')}),
        ('Belong to', {'fields': ['belong_to']}),
    )
    list_display = ['question', 'update_date']


class InquiryAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]
    fieldsets = (
        (None, {'fields': ('title', 'user', 'content')}),
        ('views', {'fields': ['views']}),
    )
    list_display = ('title', 'user', 'update_date', 'views')


admin.site.register(VideoReport, VideoReportAdmin)
admin.site.register(CommentReport, CommentReportAdmin)
admin.site.register(Help, HelpAdmin)
admin.site.register(Inquiry, InquiryAdmin)

