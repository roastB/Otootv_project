from django.core.management.base import BaseCommand
from django.utils import timezone
from user.models import Subscription


class Command(BaseCommand):
    help = 'Deletes expired subscribe user rows'

    def handle(self, *args, **options):
        now = timezone.now()
        Subscription.objects.filter(subscription_expire_date__lt=now).delete()