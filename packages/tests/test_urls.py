from django.test import TestCase

from django.urls import reverse, resolve
from packages.views import (
    Homepage, 
    AboutUsPage,
    PackageDetailPage, 
    filter_packages
    )

from packages.models import (
    Destination, 
    Type, 
    Package
    )

class HomepageUrlTestcase(TestCase):

    def setUp(self) -> None:
        self.homepage_url = reverse('homepage')
        
    def test_homepage_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.homepage_url)
        self.assertEqual(
            resolver_match.func.__name__, Homepage.as_view().__name__
            )

class AboutUsPageUrlTestcase(TestCase):

    def setUp(self) -> None:
        self.about_us = reverse('about-us')
        
    def test_aboutus_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.about_us)
        self.assertEqual(
            resolver_match.func.__name__, AboutUsPage.as_view().__name__
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

        self.package_detail_url = reverse('package-detail', kwargs={'package_slug': self.package.slug})
        
    def test_package_detail_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.package_detail_url)
        self.assertEqual(
            resolver_match.func.__name__, PackageDetailPage.as_view().__name__
            )

class PackageFilterUrlTestcase(TestCase):

    def setUp(self) -> None:
        self.package_filter_url = reverse('packages-filter')
        
    def test_package_filter_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.package_filter_url)
        self.assertEqual(
            resolver_match.func.__name__, filter_packages.__name__
            )



