from django.test import TestCase
from testimonials.models import Testimonial

class TestTestimonialModel(TestCase):

    def setUp(self) -> None:

        Testimonial.objects.bulk_create([
            Testimonial(
                username="test_user_seven",
                content="Test content for testimonial",
            )
            for _ in range(1,7)
        ])
    

    def test_testimonial_model_str_method(self) -> None:
        queryset = Testimonial.objects.all()
        expected_str = "test_user from Test city, Test country"
        self.assertEqual(queryset[0].lower(), expected_str.lower())

    def test_get_random_testimonial_with_default_value(self) -> None:
        result = Testimonial.objects.get_random_testimonial()
        self.assertTrue(len(result), 6)
    
    def test_get_random_testimonial_with_stated_value(self) -> None:
        result = Testimonial.objects.get_random_testimonial(4)
        self.assertTrue(len(result), 4)

    