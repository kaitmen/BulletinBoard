from celery import shared_task

from .emails import *


@shared_task
def start_send_review_task(review_id):
    send_review_created(review_id)


@shared_task
def start_send_review_active_task(review_id):
    send_review_active(review_id)


@shared_task
def start_send_week_newsletter_task():
    send_week_newsletter()