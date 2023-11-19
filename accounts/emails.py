from typing import Dict, Any
from django.contrib.auth.tokens import PasswordResetTokenGenerator as verification_token

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.core.mail import EmailMessage

from django.templatetags.static import static

def send_reset_password_email(request, user:Dict[str, Any]) -> bool:
    """Sends the recovery email to user with the link to reset user password.

    Args:
        request (_type_): initial request
        user (_type_): user instance

    Returns:
        _type_: True if email sent else False
    """

    mail_subject = "Password Reset"
    message = render_to_string("emails/reset-password-email.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'slug': urlsafe_base64_encode(force_bytes(user.slug)),
        'token': verification_token().make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(
        mail_subject, 
        message, 
        from_email=settings.EMAIL_HOST_USER, 
        to=[user.email])
    email.content_subtype = 'html'
    
    if email.send():
        return True
    return False