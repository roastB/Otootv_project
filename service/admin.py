from django.contrib import admin
from service.models import ReportContent, Report, Help, Inquiry, Reply


class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 0


class ReportContentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Content', {'fields': ('category', 'content')}),
        ('Belong to', {'fields': ['belong_to']}),
    )
    list_display = ['category', 'content', 'belong_to', 'user', 'update_date']
    list_filter = ['category']


class ReportAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['user']}),
        ('Content', {'fields': ('category', 'content')}),
    )
    list_display = ['user', 'category', 'create_date']
    list_filter = ['category']

class HelpAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('question', 'content', 'user')}),
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
admin.site.register(Help, HelpAdmin)
admin.site.register(Inquiry, InquiryAdmin)

