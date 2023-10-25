from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import User
from accounts.views import (
    UserLoginView,
    UserRegistrationView,
    logout_view
)

class AccountsUrlTestcase(TestCase):

    def setUp(self) -> None:
        self.signin_url = reverse('signin')
        self.signup_url = reverse('signup')
        self.signout_url = reverse('signout')

        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )
        
    def test_signin_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.signin_url)
        self.assertEqual(
            resolver_match.func.__name__, UserLoginView.as_view().__name__
            )
    
    def test_signup_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.signup_url)
        self.assertEqual(
            resolver_match.func.__name__, UserRegistrationView.as_view().__name__
            )
    
    def test_signout_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.signout_url)
        self.assertEqual(
            resolver_match.func.__name__, logout_view.__name__
            )