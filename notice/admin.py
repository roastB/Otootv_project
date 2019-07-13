from django.contrib import admin
from notice.models import Notice


class NoticeAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('title', 'user', 'content')}),
        ('views', {'fields': ['views']}),
    )
    list_display = ('title', 'user', 'update_date', 'views')


admin.site.register(Notice,  NoticeAdmin)
