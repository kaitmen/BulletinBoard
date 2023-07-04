from .tasks import start_send_week_newsletter_task


def send_week_newsletter_cron_job():
    start_send_week_newsletter_task.delay()



