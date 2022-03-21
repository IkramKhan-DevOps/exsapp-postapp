from urllib import request

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email(user, detail):
    current_site = get_current_site(request)
    mail_subject = 'User Account Creation.'
    message = render_to_string('admins/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'username': user.username,
        'email': user.email,
        'password': "default@password",
        'detail': detail,
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
