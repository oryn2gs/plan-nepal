from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from testimonials.models import Testimonial

from django.contrib.auth import get_user_model
User = get_user_model()


class TestimonialTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )

        self.data =  {
            "content" : 'content for for testimonial',
        }

        self.url = reverse("create-testimonial")
        self.success_url = reverse('homepage')
        self.signin_url = reverse('signin')
        

    def test_create_testimonial_success(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)

        saved_testimonial = Testimonial.objects.filter(
            user=self.user).first()
        self.assertIsNotNone(saved_testimonial)
        
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]

        self.assertEqual(response.url, self.success_url)
        self.assertEqual(
            messages[0].lower(), 
            "your testimonial has been added successfully"
        )
    
    def test_create_testimonial_failure_with_unauthenticated_user(self) -> None:
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.signin_url}?next={self.url}")

        



