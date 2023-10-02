from django.test import TestCase

from django.urls import reverse, resolve
from packages.views import Homepage, PackageDetailPage

from packages.models import (
    Destination, 
    Type, 
    Package
    )

class PackageUrlTestcase(TestCase):

    def setUp(self) -> None:
        self.homepage_url = reverse('homepage')
        
    def test_homepage_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.homepage_url)
        self.assertEqual(
            resolver_match.func.__name__, Homepage.as_view().__name__
            )

class PackageDetailUrlTestcase(TestCase):

    def setUp(self) -> None:
        self.destination = Destination.objects.create(name="Destination 1")
        self.type = Type.objects.create(name="Type 1")
        self.package = Package.objects.create(
            name= "package",
            destination = self.destination,
            price = 100.00
        )
        self.package.type.add(self.type)

        self.package_detail_url = reverse('package-detail', kwargs={'slug': self.package.slug})
        
    def test_package_detail_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.package_detail_url)
        self.assertEqual(
            resolver_match.func.__name__, PackageDetailPage.as_view().__name__
            )
