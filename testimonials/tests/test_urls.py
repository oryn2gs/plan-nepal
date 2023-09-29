from django.test import TestCase
from django.urls import reverse, resolve
from testimonials.views import create_testimonial

class YourViewTestCase(TestCase):

    def setUp(self) -> None:
        self.url = reverse('create-testimonial')
        return super().setUp()

    def test_create_testimonial_url_resolves_to_create_testimonial_view(self) -> None:
        resolver_match = resolve(self.url)
        self.assertEqual(resolver_match.func, create_testimonial)
