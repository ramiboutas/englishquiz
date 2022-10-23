from __future__ import annotations

from django.core.mail import mail_admins


def mail_admins_with_an_exception(e):
    mail_subject = "Exception | English Stuff Online"
    mail_message = f" An exception occurred: \n {e}"
    mail_admins(
        mail_subject,
        mail_message,
        fail_silently=False,
        connection=None,
        html_message=None,
    )
