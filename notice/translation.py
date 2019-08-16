from modeltranslation.translator import translator, TranslationOptions
from notice.models import Notice


class NoticeTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)

translator.register(Notice, NoticeTranslationOptions)


