from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from testimonials.models import Testimonial
from django.core.files.uploadedfile import SimpleUploadedFile


class TestimonialTestCase(TestCase):

    def setUp(self):
        # ? using default images for a test purpose to get the image_byte
        
        self.data =  {
            "username" : "test user",
            "content" : 'content for for testimonial',
            "user_image" : self._create_mock_image(),
            "city" : "test city",
            "country" : 'test country'

        }

    def test_create_testimonial(self):
        """ 
        test post testimonial success, and redirect users to referer urls 
        """

        response = self.client.post(reverse(
            "create-testimonial"), data=self.data, HTTP_REFERER="/previous_url/")

        saved_testimonial = Testimonial.objects.filter(
            username="test user").first()
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
        ]

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(saved_testimonial)
        self.assertEqual(response.url, '/previous_url/')
        self.assertEqual(
            messages[0].lower(), 
            "your testimonial has been added successfully"
        )
    
    def _create_mock_image(self):

        with open("media/testimonial_image/default.png", "rb") as file:
            file_content = file.read()

        test_image = SimpleUploadedFile(
            name = "test_image.png", 
            content = file_content, 
            content_type="image/png"
        )
       
        return test_image

    def tearDown(self):
        try:
            testimonial = Testimonial.objects.get(username="test user")
            testimonial.delete()
        except Testimonial.DoesNotExist:
            pass 



# --------------------------------------- get tests
        # self.testimonial = Testimonial.objects.create(
        #     username = "test user one",
        #     content = 'test content for testimonial',
        #     user_image = self.test_image,
        #     city = "test city",
        #     country = 'test country'
        # )

    # def test_get_testimonial(self):
    #     """ test fetch all testimonial success """

    #     response = self.client.get(reverse('testimonials'))

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("testimonials", response.context)
        
    #     returned_testimonials = response.context['testimonials']
    #     self.assertLessEqual(len(returned_testimonials), 6)
    #     self.assertIn(self.testimonial, returned_testimonials)

    