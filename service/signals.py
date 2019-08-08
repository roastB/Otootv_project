from service.models import Help, Inquiry, Reply
from django_summernote.models import Attachment

from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from bs4 import BeautifulSoup


# help 이미지 available = True
@receiver(post_save, sender=Help)
def help_available_true_handler(sender, instance, **kwargs):
    if instance.content:
        soup = BeautifulSoup(instance.content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            result.available = True
            result.save()

# help 이미지 삭제
@receiver(post_delete, sender=Help)
def help_delete_handler(sender, instance, **kwargs):
    if instance.content:
        soup = BeautifulSoup(instance.content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            storage, path = result.file.storage, result.file.path
            storage.delete(path)
            result.delete()


# Inquiry 이미지 available = True
@receiver(post_save, sender=Inquiry)
def inquiry_available_true_handler(sender, instance, **kwargs):
    if instance.content:
        soup = BeautifulSoup(instance.content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            result.available = True
            result.save()


# inquiry 이미지 삭제
@receiver(post_delete, sender=Inquiry)
def inquiry_delete_handler(sender, instance, **kwargs):
    if instance.content:
        soup = BeautifulSoup(instance.content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            storage, path = result.file.storage, result.file.path
            storage.delete(path)
            result.delete()


# reply 이미지 available = True
@receiver(post_save, sender=Reply)
def reply_available_true_handler(sender, instance, **kwargs):
    if instance.content:
        soup = BeautifulSoup(instance.content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            result.available = True
            result.save()


# reply 이미지 삭제
@receiver(post_delete, sender=Reply)
def reply_delete_handler(sender,instance, **kwargs):
    if instance.content:
        soup = BeautifulSoup(instance.content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            result = Attachment.objects.get(file=src[7:])
            storage, path = result.file.storage, result.file.path
            storage.delete(path)
            result.delete()
