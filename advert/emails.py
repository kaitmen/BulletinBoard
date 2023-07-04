from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from datetime import datetime, timedelta

from user_profile.models import Profile

from .models import Advert, Review


def send_review_active(review_id):
    review = Review.objects.get(pk=review_id)
    html_content = render_to_string(
        'emails/active_review.html',
        {
            'review': review,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Your review was activated',
        body=f'Your review to advert {review.advert.title} was activated',
        from_email=settings.SERVER_EMAIL,
        to=[review.author.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_review_created(review_id):
    review = Review.objects.get(pk=review_id)
    html_content = render_to_string(
        'emails/new_review.html',
        {
            'review': review,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{review.author.username} left review',
        body=f'{review.author.username} left review to your advert {review.advert.title}',
        from_email=settings.SERVER_EMAIL,
        to=[review.advert.author.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_week_newsletter():
    one_week_ago = datetime.today() - timedelta(days=7)
    users = list(Profile.objects.filter(get_newsletter=True).values_list("email", flat=True))
    week_adverts = Advert.objects.filter(created_at__gte=one_week_ago)

    html_content = render_to_string(
        'emails/week_newsletter.html',
        {
            'adverts': week_adverts,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Newsletter on last week!',
        body=f'Hello, check new advert on this week!',
        from_email=settings.SERVER_EMAIL,
        to=users,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
