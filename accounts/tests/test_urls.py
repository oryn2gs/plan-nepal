from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import User
from accounts.views import (
    UserLoginView,
    UserRegistrationView,
    # logout_view,
    LogoutView,
    RequestResetPasswordView,
    RequestResetPasswordDoneView,
    ResetPasswordConfirmView
)

class AccountsUrlTestcase(TestCase):

    def setUp(self) -> None:
        self.signin_url = reverse('signin')
        self.signup_url = reverse('signup')
        self.signout_url = reverse('signout')
        self.request_password_reset_url = reverse('request-reset-password')
        self.reset_password_done_url = reverse('reset-password-done')
        self.reset_password_confirm_url = reverse('reset-password-confirm')

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
            resolver_match.func.__name__, 
            LogoutView.as_view().__name__
            )
    
    def test_request_reset_password_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.request_password_reset_url)
        self.assertEqual(
            resolver_match.func.__name__, 
            RequestResetPasswordView.as_view().__name__
            )
    
    def test_request_reset_password_done_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.reset_password_done_url)
        self.assertEqual(
            resolver_match.func.__name__, 
            RequestResetPasswordDoneView.as_view().__name__
            )
    
    def test_request_reset_password_confirm_url_resolves_to_correct_view(self) -> None:
        resolver_match = resolve(self.reset_password_confirm_url)
        self.assertEqual(
            resolver_match.func.__name__, 
            ResetPasswordConfirmView.as_view().__name__
            )