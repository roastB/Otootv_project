from notice.models import Notice
from django_summernote.models import Attachment
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from bs4 import BeautifulSoup


# notice 이미지 available = True
@receiver(post_save, sender=Notice)
def notice_available_true_handler(sender, instance, **kwargs):
    if instance.content:
        soup = BeautifulSoup(instance.content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            result.available = True
            result.save()

# notice 이미지 삭제
@receiver(post_delete, sender=Notice)
def notice_delete_handler(sender, instance, **kwargs):
    if instance.content:
        soup = BeautifulSoup(instance.content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            storage, path = result.file.storage, result.file.path
            storage.delete(path)
            result.delete()

