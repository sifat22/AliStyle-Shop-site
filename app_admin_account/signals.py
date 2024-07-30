# your_app/signals.py
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

User= get_user_model()


@receiver(user_signed_up)
def send_email_verification(sender, request, user, **kwargs):
    if not user.is_active:
        token= default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)     
        mail_subject = 'Please Activate your account!'
        message = render_to_string('app_account/account_verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        })
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])