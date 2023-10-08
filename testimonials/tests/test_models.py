from django.test import TestCase
from testimonials.models import Testimonial
from django.contrib.auth import get_user_model
User = get_user_model()

class TestTestimonialModel(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )

        Testimonial.objects.bulk_create([
            Testimonial(
                user = self.user,
                content="Test content for testimonial",
            )
            for _ in range(1,7)
        ])
    

    def test_testimonial_model_str_method(self) -> None:
        queryset = Testimonial.objects.all()
        expected_str = f"Testimonial from {self.user.email}"
        self.assertEqual(str(queryset[0]), expected_str)

    def test_get_random_testimonial_with_default_value(self) -> None:
        result = Testimonial.objects.get_random_testimonial()
        self.assertTrue(len(result), 6)
    
    def test_get_random_testimonial_with_stated_value(self) -> None:
        result = Testimonial.objects.get_random_testimonial(4)
        self.assertTrue(len(result), 4)

    