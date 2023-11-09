from django.test import TestCase
from django.urls import reverse, resolve
from bookings.views import (
    create_booking, 
    post_inquiry,
    reply_inquiry,
    filter_inqury
    )

class BookingUrlTestcase(TestCase):

    def setUp(self) -> None:
        from packages.models import (
            Destination,
            Package,
            Type
        )

        self.destination = Destination.objects.create(name="destination")
        self.type = Type.objects.create(name="type")

        self.package = Package.objects.create(
            destination = self.destination,
            name = "package",
            price = 100.00
        )
        self.package.type.add(self.type)

        self.create_booking_url = reverse('create-booking', kwargs={
            "package_slug": self.package.slug
            })
     

        
    def test_create_booking_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.create_booking_url)
        self.assertEqual(
            resolver_match.func.__name__, create_booking.__name__
            )


class InquiryUrlTestcase(TestCase):

    def setUp(self) -> None:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )


        self.filter_inquiry_url = reverse('faq-list-filter')
        self.post_inquiry_url = reverse('post-inquiry')
        self.reply_inquiry_url = reverse('reply-inquiry')
        
    def test_filter_inquiry_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.filter_inquiry_url)
        self.assertEqual(
            resolver_match.func.__name__, filter_inqury.__name__
            )
    
    def test_post_inquiry_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.post_inquiry_url)
        self.assertEqual(
            resolver_match.func.__name__, post_inquiry.__name__
            )
    
    def test_reply_inquiry_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.reply_inquiry_url)
        self.assertEqual(
            resolver_match.func.__name__, reply_inquiry.__name__
            )
        



