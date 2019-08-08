from django.core.management.base import BaseCommand
from django_summernote.models import Attachment


class Command(BaseCommand):
    help = 'Deletes summernote attachment rows'

    def handle(self, *args, **options):
        queryset = Attachment.objects.filter(available=False)
        for result in queryset:
            storage, path = result.file.storage, result.file.path
            storage.delete(path)
            result.delete()
