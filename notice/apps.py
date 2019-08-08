from django.apps import AppConfig


class NoticeConfig(AppConfig):
    name = 'notice'

    def ready(self):
        import notice.signals
