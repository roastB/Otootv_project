from django.contrib import admin
from notice.models import Notice
from modeltranslation.admin import TranslationAdmin

class NoticeAdmin(TranslationAdmin):

    fieldsets = (
        (None, {'fields': ('title', 'user', 'content')}),
        ('views', {'fields': ['views']}),
    )
    list_display = ('title', 'user', 'update_date', 'views')


admin.site.register(Notice,NoticeAdmin)
