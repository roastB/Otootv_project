import logging

from django.core.management.base import BaseCommand,  CommandError
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['시청자', '진행자']
MODELS1 = ['video', 'channel']
MODELS2 =['comment', 'report']
PERMISSIONS = ['add', 'change', 'delete', 'view']


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        new_group1 = Group.objects.create(name=GROUPS[0])
        new_group2 = Group.objects.create(name=GROUPS[1])

        for model in MODELS1:
            name = 'Can {} {}'.format(PERMISSIONS[3], model)
            try:
                model_add_perm = Permission.objects.get(name=name)
                print("Creating {}".format(name))
            except Permission.DoesNotExist:
                logging.warning("Permission not found with name '{}'.".format(name))
                continue
            new_group1.permissions.add(model_add_perm)

            for permission in PERMISSIONS:
                name = 'Can {} {}'.format(permission, model)
                try:
                    model_add_perm = Permission.objects.get(name=name)
                    print("Creating {}".format(name))
                except Permission.DoesNotExist:
                    logging.warning("Permission not found with name '{}'.".format(name))
                    continue
                new_group2.permissions.add(model_add_perm)

        for model in MODELS2:
            for permission in PERMISSIONS:
                name = 'Can {} {}'.format(permission, model)
                try:
                    model_add_perm = Permission.objects.get(name=name)
                    print("Creating {}".format(name))
                except Permission.DoesNotExist:
                    logging.warning("Permission not found with name '{}'.".format(name))
                    continue
                new_group1.permissions.add(model_add_perm)
                new_group2.permissions.add(model_add_perm)

        print("Created default group and permissions.")
