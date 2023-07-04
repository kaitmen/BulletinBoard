from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import *
from .tasks import *
from .models import Profile, RegisterCode


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        code = RegisterCode.objects.create(user=instance, code=get_random_code(), token=get_random_token())
        start_send_code_email_task.delay(instance.id, code.id)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()