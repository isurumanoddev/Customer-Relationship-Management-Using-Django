from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from accounts.models import Customer


def create_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="customers")
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )
        print("Customer Profile Created")


post_save.connect(create_profile, sender=User)


def update_profile(sender, instance, created, **kwargs):
    if created == False:
        print("Customer Profile Updated")


post_save.connect(update_profile, sender=User)
