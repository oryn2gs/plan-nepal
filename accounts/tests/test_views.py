from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse
from testimonials.models import Testimonial

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
        self.http_referer = reverse('homepage')
        self.template_name = "accounts/signup.html"

        
        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )

        Testimonial.objects.bulk_create([
            Testimonial(
                user = self.user,
                content="test testimonil"
            )
            for _ in range(8)
        ])


    def test_user_registration_success(self) -> None:
        response = self.client.post(self.url, data=self.form_data)
        print(response)
        #fix the response status

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.success_url)
        self.assertTrue(User.objects.filter(email=self.form_data['email']).exists())
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], "Your account has been created successfully,  and you\'re logged in.")
    

   
    def test_user_registration_failure(self) -> None:
        self.form_data["confirm_password"] = "wrongpassword"

        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], "There was an error in the registration form.")


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

        Testimonial.objects.bulk_create([
            Testimonial(
                user = self.user,
                content="test testimonil"
            )
            for _ in range(8)
        ])
        
        self.url = reverse('signin')
        self.success_url = reverse('homepage')

    def test_login_success(self) -> None:
        response = self.client.post(self.url, data=self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], "Login in successfully.")
        self.assertRedirects(response, self.success_url)
    

        
    
    def test_login_failure(self) -> None:
        self.form_data["email"] = "wrong@email.com"
        response = self.client.post(self.url, data=self.form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signin.html")
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], "Invalid credentails")
    
   


class UserLogoutTestCase(TestCase) :

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@email.com",
            password = "password"
        )
        self.client.force_login(self.user)

    def test_user_logout_success(self):
        response = self.client.post(reverse('signout'))

        print(response)
        self.assertEqual(response.status_code, 302)
        messages =[
            str(messages) for messages in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], "Logout Successfully")


    