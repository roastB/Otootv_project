from django.apps import AppConfig


class VodConfig(AppConfig):
    name = 'vod'

    def ready(self):
        import vod.signals