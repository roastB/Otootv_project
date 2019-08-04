import logging

from django.core.management.base import BaseCommand,  CommandError
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['시청자', '진행자']


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        try:
            group = Group.objects.get(name='시청자')
        except Group.DoesNotExist:
            new_group1 = Group.objects.create(name=GROUPS[0])
            new_group2 = Group.objects.create(name=GROUPS[1])

