from django.contrib import admin
from service.models import ReportContent, Report, HelpQuestion, HelpAnswer, Inquiry, Reply


class HelpAnswerInline(admin.StackedInline):
    model = HelpAnswer
    extra = 0


class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 0


class ReportContentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('category', 'user', 'content')}),
        ('Belong to', {'fields': ['belong_to']}),
    )
    list_display = ['category', 'content', 'belong_to', 'user', 'update_date']
    list_filter = ['category']


class ReportAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['user']}),
        ('Category', {'fields': ('channel', 'video', 'comment')}),
        ('Content', {'fields': ['content']}),
    )
    list_display = ['user', 'channel', 'video', 'comment', 'content', 'create_date']
    list_filter = ('channel', 'video', 'comment')


class HelpQuestionAdmin(admin.ModelAdmin):
    inlines = [HelpAnswerInline]
    fieldsets = (
        (None, {'fields': ('question', 'user',)}),
        ('Belong to', {'fields': ['belong_to']}),
    )
    list_display = ['question', 'user', 'update_date']


class InquiryAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]
    fieldsets = (
        (None, {'fields': ('title', 'user', 'content')}),
        ('views', {'fields': ['views']}),
    )
    list_display = ('title', 'user', 'update_date', 'views')


admin.site.register(ReportContent, ReportContentAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(HelpQuestion, HelpQuestionAdmin)
admin.site.register(Inquiry, InquiryAdmin)

