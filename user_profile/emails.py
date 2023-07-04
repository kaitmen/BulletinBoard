from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from .models import *


def send_code_email(user_id, code_id):
    user = User.objects.get(pk=user_id)
    code = RegisterCode.objects.get(pk=code_id)
    link = f"{settings.FRONTEND_URL}/{code.token}"
    html_content = render_to_string(
        'emails/send_code.html',
        {
            'user': user,
            'code': code.code,
            'link': link
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{user.username} registered',
        body="We send code to your email",
        from_email=settings.SERVER_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
