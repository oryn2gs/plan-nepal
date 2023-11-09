from django.test import TestCase
from subscriptions.forms import SubscriptionsForm

class SubscriptionFormTestCase(TestCase):
    fixtures =[
        "fixtures/subscriptions_fixtures.json"
    ]

    def setUp(self) -> None:
        self.data = {
            'email': "test@email.com"
        }

    def test_subscription_form_valid(self)-> None:
        form = SubscriptionsForm(data=self.data)
        self.assertTrue(form.is_valid())
    
    def test_subscription_form_invalid_email_already_register(self)-> None:
        self.data = {
            "email": "testsubsone@email.com"
        }
        form = SubscriptionsForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn(
            "Email you\'ve provided is already in the subscription list.", 
            form.errors["email"])



