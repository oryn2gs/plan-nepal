from django.test import TestCase
from django.urls import reverse, resolve
from subscriptions.views import SubscriptionCreateView

class SubscriptionUrlTestCase(TestCase):

    def setUp(self) -> None:
        self.create_url = reverse('create-subs')

    def test_create_subs_url_points_to_correct_view(self) -> None:
        resolver = resolve(self.create_url)
        self.assertEquals(
            resolver.func.view_class, SubscriptionCreateView
        )

    
