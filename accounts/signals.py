from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from accounts.models import Customer

def create_profile(sender,instance,created,**kwargs):
    if created:
        group = Group.objects.get(name="customer")
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            # name=request.POST.get("username"),
            # phone=request.POST.get("phone_number"),
            # email=request.POST.get("email"),
        )