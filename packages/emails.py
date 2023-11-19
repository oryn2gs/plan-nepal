
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

from bookings.models import Booking
from django.contrib.auth import get_user_model
User = get_user_model()

def send_booking_confirmation_email(request, user:User, booking:Booking) -> bool:
    mail_subject = "Booking Confirmation"
    message = render_to_string("emails/booking-confirmation-email.html", {
        'user': user,
        "profile": user.profile,
        'booking': booking,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(
        mail_subject, 
        message, 
        from_email=settings.EMAIL_HOST_USER, 
        to=[user.email]
        )
    email.content_subtype = 'html'
    if email.send():
        return True
    return False