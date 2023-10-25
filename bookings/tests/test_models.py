from django.test import TestCase
from datetime import date, time

from bookings.models import (
    Inquiry, 
    InquiryAnswer, 
    Booking
    )
from packages.models import (
    Package,
    Destination
)
from django.contrib.auth import get_user_model
User = get_user_model()



class BookingModelTestCase(TestCase):

    def setUp(self) -> None:
        
        self.user = User.objects.create(
            email = "test@email.com",
            password = "password"
        )

        self.destination = Destination.objects.create(name="Destination 1")

        self.package = Package.objects.create(
            destination=self.destination,
            name="Package One",
            price=100.00,
            active=True,
        )

        self.booking = Booking.objects.create(
            user = self.user,
            package = self.package,
            kids = 1,
            adults = 2,
            arrival_time = time(12, 32),
            arrival_date = date(2023, 10, 21)
        )

    def test_str_method(self):
        excepted_string = f"Bookings made by {self.user.email} for {self.package.name}"
        self.assertEqual(str(self.booking), excepted_string)

    def test_booking_total_price(self) -> None:
        self.assertEqual(self.booking.total_price, 300)


class InquiryModelTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email = "test@email.com",
            password = "password"
        )

        self.inquiry1 = Inquiry.objects.create(
            user = self.user,
            inquiry_type = "packages",
            inquiry_resolved = True
        )
        self.inquiry2 = Inquiry.objects.create(
            user = self.user,
            inquiry_type = "packages",
            inquiry_resolved = False
        )

        self.inquiry3 = Inquiry.objects.create(
            user = self.user,
            inquiry_type = "packages",
            inquiry_resolved = True,
            active = False,
        )

        self.inquiry_answer = InquiryAnswer.objects.create(
            inquiry = self.inquiry1,
            user = self.user,
            content = "some teext"
        )


    def test_str_method(self) -> None:
      
        self.assertEqual(str(self.inquiry1), str(self.inquiry1.id))

    def test_get_all_resolved_inquiry_method(self) -> None:
        resolved_queries = Inquiry.objects.filter_inquiry_by_resolved_value(resolved=True)

        self.assertIn(self.inquiry1, resolved_queries)
        self.assertEqual(len(resolved_queries), 1)
    
    def test_get_all_unresolved_inquiry_method(self) -> None:
        results = Inquiry.objects.filter_inquiry_by_resolved_value(
            resolved=False
            )
        self.assertIn(self.inquiry2, results)
        self.assertEqual(len(results), 1)

    
class InquiryAnswerModelTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email = "test@email.com",
            password = "password"
        )

        self.inquiry = Inquiry.objects.create(
            user = self.user,
            inquiry_type = "packages",
            inquiry_resolved = True
        )
        
        self.inquiry_answer = InquiryAnswer.objects.create(
            inquiry = self.inquiry,
            user = self.user,
            content = "some text"
        )
    

    def test_str_method(self) -> None:
        self.assertEqual(str(self.inquiry_answer), str(self.inquiry_answer.id))