from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .tasks import *
from .models import Review


@receiver(post_save, sender=Review)
def create_review(sender, instance, created, **kwargs):
    if created:
        start_send_review_task.delay(instance.id)


@receiver(pre_save, sender=Review)
def save_review(sender, instance, update_fields=None, **kwargs):
    try:
        old_instance = Review.objects.get(id=instance.id)
        if 'active' in update_fields and not old_instance.active:
            start_send_review_active_task.delay(instance.id)
    except:
        return None
