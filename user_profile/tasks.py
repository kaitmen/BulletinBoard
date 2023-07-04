from celery import shared_task

from .emails import send_code_email


@shared_task
def start_send_code_email_task(user_id, code_id):
    send_code_email(user_id, code_id)
