from django.test import TestCase
from testimonials.models import Testimonial

class TestTestimonialModel(TestCase):

    def setUp(self) -> None:
        self.testimonial = Testimonial.objects.create(
            username="test_user",
            content="Test content for testimonial",
            city="Test city",
            country="Test country"
        )
    

    def test_testimonial_model_str_method(self):
        expected_str = "test_user from Test city, Test country"
        self.assertEqual(str(self.testimonial), expected_str)