from unittest.mock import patch

from accounts import forms

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes 
from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse
from django.conf import settings
from django.core import mail
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegistrationTestCase(TestCase):

    def setUp(self) -> None:
        self.form_data = {
            "email": "test@email.com",
            "password": "password",
            "confirm_password": "password"
        }
        self.url = reverse('signup')
        self.success_url = reverse('homepage')
        self.template_name = "accounts/signup.html"
        self.form_class = forms.UserRegistrationForm

    def test_registration_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)
        
    def test_registration_form_used(self):
        response = self.client.get(self.url)
        form = response.context['form'] 
        self.assertIsInstance(form, forms.UserRegistrationForm)

    def test_user_registration_success(self) -> None:
        response = self.client.post(self.url, data=self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)
        user = User.objects.get(email=self.form_data["email"])
        self.assertTrue(user)
        self.assertTrue(user.is_authenticated)
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], "Your account has been created successfully, and you\'re logged in.")
        
    
class UserLoginTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email= "test@email.com",
            password= "password"
        )
        self.form_data = {
            "email": "test@email.com",
            "password": "password"
        }


        self.url = reverse('signin')
        self.success_url = reverse('homepage')

    def test_login_success(self) -> None:
        response = self.client.post(self.url, data=self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], "Logged in successfully.")
        self.assertRedirects(response, self.success_url)
    

    
class UserLogoutTestCase(TestCase) :

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@email.com",
            password = "password"
        )
        self.client.force_login(self.user)

    def test_user_logout_success(self):
        response = self.client.post(reverse('signout'))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages =[
            str(messages) for messages in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], "Logout Successfully")


class RequestResetPasswordTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@email.com",
            password = "password",
        )
        
        verification_token = PasswordResetTokenGenerator()
        self.token = verification_token.make_token(self.user)
        self.slug = urlsafe_base64_encode(force_bytes(self.user.slug))
        self.url = reverse('request-reset-password')

    @patch('accounts.emails.send_reset_password_email')
    def test_request_reset_password_success(self, mock_send_email) -> None:
        form_data = {
            "email": "testuser@email.com"
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)

        self.assertEquals(len(mail.outbox), 1)  
        email = mail.outbox[0]

        self.assertEquals(email.subject, 'Password Reset')
        self.assertEquals(email.from_email, settings.EMAIL_HOST_USER)
        self.assertEquals(email.to, [self.user.email])

        # ? Check token and slug in email
        self.assertIn(self.token, email.body)
        self.assertIn(self.slug, email.body)
    

class ResetPassowordConfirmViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@email.com",
            password = "password",
        )
        
        verification_token = PasswordResetTokenGenerator()
        self.token = verification_token.make_token(self.user)
        self.slug = urlsafe_base64_encode(force_bytes(self.user.slug))

        self.kwargs = {
            'slug': self.slug,
            'token': self.token
        }


    def test_verification_success(self) -> None:
        self.url = reverse("reset-password-confirm", kwargs=self.kwargs)

        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
    
    def test_verification_failure_invalid_slug(self) -> None:
        self.kwargs["slug"] = "invalidslug"
        self.url = reverse("reset-password-confirm", kwargs=self.kwargs)

        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 404)
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]
        
        self.assertEqual(
            messages[0], 
            "There was a issue decoding account id, Please try again later.")
    
    def test_verification_failure_invalid_token(self) -> None:
        self.kwargs["token"] = "invalidtoken"
        self.url = reverse("reset-password-confirm", kwargs=self.kwargs)

        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 404)

        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]
        self.assertEqual(
            messages[0], 
            "Verification Token is Invalid or Expired, Please try again.")
        
    
class ResetPassowordCompleteViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@email.com",
            password = "password",
        )
        self.url = reverse('reset-password-complete')
        session = self.client.session
        session['slug'] = self.user.slug
        session.save()

    def test_form_rendered(self) -> None:
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        form = response.context['form'] 
        self.assertIsInstance(form, forms.PasswordResetForm)
        
    def test_update_user_password_success(self) -> None:
        form_data = {
            "password": "#StrongPassword23",
            "confirm_password": "#StrongPassword23"
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEquals(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(form_data["password"]))

     
       