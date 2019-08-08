from vod.models import Channel, Video
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save


# 채널 배경 이미지 삭제
@receiver(post_delete, sender=Channel)
def background_image_delete_handler(sender,instance, **kwargs):
    if instance.background_image:
        storage, path = instance.background_image.storage, instance.background_image.path
        storage.delete(path)

# 채널 배경 이미지 변경
@receiver(pre_save, sender=Channel)
def background_image_change_delete_handler(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = Channel.objects.get(pk=instance.pk).background_image
        except Channel.DoesNotExist:
            return
        else:
            new_image_path = instance.background_image.path
            if old_image and old_image.path != new_image_path:
                old_image.storage.delete(old_image.path)

# 비디오 삭제
@receiver(post_delete, sender=Video)
def video_delete_handler(sender,instance, **kwargs):
    if instance.video:
        storage, path = instance.video.storage, instance.video.path
        storage.delete(path)

# 비디오 변경
@receiver(pre_save, sender=Video)
def video_change_delete_handler(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_video = Video.objects.get(pk=instance.pk).video
        except Video.DoesNotExist:
            return
        else:
            new_video_path = instance.video.path
            if old_video and old_video.path != new_video_path:
                old_video.storage.delete(old_video.path)