from django.conf import settings
from django.core.mail import send_mail


def send_mail_to_admin(extra_subject="", body_text=""):
    subject = f'www.englishstuff.online | {extra_subject}'

    send_mail(subject,body_text, settings.EMAIL_HOST_USER,
            [settings.ADMIN_EMAIL_FOR_NOTIFICATIONS],
            fail_silently=True,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD,
        )
