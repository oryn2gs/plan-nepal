from django.test import TestCase
from django.urls import reverse, resolve
from bookings.views import create_booking

class CreateBookingUrlTestcase(TestCase):

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

        self.homepage_url = reverse('create-booking', kwargs={
            "package_slug": self.package.slug
            })
        
    def test_create_booking_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.homepage_url)
        self.assertEqual(
            resolver_match.func.__name__, create_booking.__name__
            )