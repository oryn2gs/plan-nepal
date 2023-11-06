from urllib.parse import urlparse
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
User = get_user_model()

from bookings.models import Booking, Inquiry, InquiryAnswer
from packages.models import Destination, Package


from datetime import date, time

    
class BookingCreateTestCase(TestCase):

    def setUp(self) -> None:

        self.destination = Destination.objects.create(name="Destination 1")

        self.package = Package.objects.create(
            destination=self.destination,
            name="Package One",
            price=100.00,
            active=True,
        )


        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )

        self.data = {
            "kids" : 1,
            "adults" : 2,
            "airlines" : "Etihad",
            "flight_number" : "2rvbV",
            "arrival_date" : date(2023, 10, 20),
            "arrival_time" : time(12, 32),
            "airport_pickup": True,
        }

        self.url = reverse('create-booking', kwargs={'package_slug': self.package.slug})
        self.rediect_url = reverse('package-detail', kwargs={'package_slug': self.package.slug})
        self.login_url = reverse('signin')

    def test_booking_made_success(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, 302)

        saved_booking = Booking.objects.first()
        self.assertIsNotNone(saved_booking)
        
        messages = [
            str(message) for message in get_messages(response.wsgi_request)
            ]
        self.assertEqual(messages[0], "Bookings made succefully, we\'ve sent a confirmation message to your email")
        self.assertEqual(urlparse(response.url).path, self.rediect_url)


    def test_booking_made_failure_unauthenticated_user(self) -> None:
        data = {
            "kids" : 1,
            "adults" : 2,
            "airlines" : "Etihad",
            "flight_number" : "2rvbV",
            "arrival_date" : date(2023, 10, 20),
            "arrival_time" : time(12, 32),
            "airport_pickup": True,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.url).path, self.login_url)
    


class FaqListViewTestCase(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )

        inquiries = []
        for i in range(1, 7):
            inquiry = Inquiry(
                user=self.user,
                inquiry_type="packages",
                question=f"Some question {i}",
                inquiry_resolved=i % 2 == 0,  
                active=True,
            )
            inquiries.append(inquiry)

        Inquiry.objects.bulk_create(inquiries)
        self.url = reverse('faq-list')


    def test_faq_list_page_has_inquiries_data(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/faq-list.html')
        self.assertIn('faq_resolved', response.context)
        self.assertIn('faq_unresolved', response.context)


class PostInquiryViewTestCase(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )

        self.form_data = {
            "inquiry_type": "packages",
            "question": "some question",
        }
        self.client.force_login(self.user)

        self.url = reverse("post-inquiry")
        self.redirect_url = reverse('faq-list')
        self.signin_url = reverse('signin')

    def test_post_inquiry_success(self) -> None:
        response = self.client.post(self.url, data= self.form_data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Inquiry.objects.first())
        self.assertRedirects(response, self.redirect_url)
        messages = [
            str(messages) for messages in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], "Your Inquiry has been posted, we\'ll notify you once our operator responds.")

    
    def test_post_inquiry_faliure_with_no_content(self) -> None:
        form_data = {"inquiry_type": "packages"}
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 400)

        self.assertFalse(Inquiry.objects.first())
        messages = [
            str(messages) for messages in get_messages(response.wsgi_request)
        ]
      
        self.assertEqual(messages[0], "Missing field question, please complete the form")

    
    def test_post_inquiry_faliure_with_unauthenticated_user(self) -> None:
        self.client.logout()
        response = self.client.post(self.url, data=self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.url).path, self.signin_url)
    
   
class PostInquiryAnswerTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )
        self.superuser = User.objects.create_superuser(
            email = "superuser@email.com",
            password = "password"
        )

        self.inquiry = Inquiry.objects.create(
            user = self.user,
            inquiry_type = "packages",
            question = "some question"
        )

        self.form_data = {
            "content" : "some text"
        }

        self.url = reverse("reply-inquiry")
        self.client.force_login(self.superuser)


    def test_post_inquiry_answer_success(self) -> None:
        self.form_data["inquiry_id"] = self.inquiry.id

        response = self.client.post(self.url, data=self.form_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(InquiryAnswer.objects.first())
        messages = [
            str(messages) for messages in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], "Your answer to customer queries, has been added succefully.")
    
    
    def test_post_inquiry_answer_failure_missing_field(self) -> None:
        response = self.client.post(self.url, data=self.form_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(InquiryAnswer.objects.first())
        messages = [
            str(messages) for messages in get_messages(response.wsgi_request)
        ]
        self.assertEqual(messages[0], f"This inquiry_id is required, please complete the form")
    
        
class InquiryFilterTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )
        import random
        Inquiry.objects.bulk_create([
            Inquiry(
                user = self.user,
                inquiry_type =  "packages",
                question = "some question",
                inquiry_resolved = random.choice([True, False])
            )
            for _ in range(8)
        ])

        self.url = reverse("faq-list-filter")


    
    def test_filter_inquiry_success_for_resolved_faq(self):
        query = "packages"
        response = self.client.get(self.url + f"?query={query}")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/faq-card.html')
        self.assertIn("some question", str(response.content))


    def test_filter_inquiry_success_for_unresolved_faq(self):
        query = "unresolved"
        response = self.client.get(self.url + f"?query={query}")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/faq-card.html')
        self.assertIn("some question", str(response.content))


    def test_filter_inquiry_error(self):
        query = "invalid_type"
        response = self.client.get(self.url + f"?query={query}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "There is no content related to the tag.", 
            str(response.content)
            )
    
    