from django.test import TestCase

class SubscriptionCreateViewTestCase(TestCase):
    fixtures =[
        "fixtures/subscriptions_fixtures.json"
    ]

    def setUp(self) -> None:
        from django.urls import reverse
        self.url = reverse('create-subs')
        self.data = {
            "email": "new@email.com"
        }

    def test_create_subs_success(self) -> None:
        response = self.client.post(self.url, data=self.data)
        self.assertEquals(response.status_code, 302)
        from django.contrib.messages import get_messages
        from subscriptions.models import Subscription
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]
        self.assertEquals("Subscription added successfully", messages[0])
        self.assertTrue(Subscription.objects.all().count() == 3)

        