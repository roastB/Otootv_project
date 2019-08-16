from modeltranslation.translator import translator, TranslationOptions
from service.models import Help, CommentReport, VideoReport


class CommentReportTranslationOptions(TranslationOptions):
    fields = ('category',)


class VideoReportTranslationOptions(TranslationOptions):
    fields = ('category',)


class HelpTranslationOptions(TranslationOptions):
    fields = ('question', 'content',)


translator.register(VideoReport, VideoReportTranslationOptions)
translator.register(CommentReport, CommentReportTranslationOptions)
translator.register(Help, HelpTranslationOptions)


