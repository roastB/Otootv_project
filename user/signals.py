from user.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save

# 프로필 이미지 삭제
@receiver(post_delete, sender=User)
def profile_image_delete_handler(sender, instance, **kwargs):
    if instance.profile_image:
        storage, path = instance.profile_image.storage, instance.profile_image.path
        storage.delete(path)


# 프로필 이미지 변경
@receiver(pre_save, sender=User)
def profile_image_change_delete_handler(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = User.objects.get(pk=instance.pk).profile_image
        except User.DoesNotExist:
            return
        else:
            new_image_path = instance.profile_image.path
            if old_image and old_image.path != new_image_path:
                old_image.storage.delete(old_image.path)
