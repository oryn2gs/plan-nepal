from bookings import forms
from bookings import models as bookings_model
from bookings.forms import (
    BookingForm,
)
from packages import models as packages_model
from datetime import time, date

from django.contrib.auth import get_user_model
User = get_user_model()

from django.test import TestCase
class BookingFormTestCase(TestCase):
    fixtures =[
        'fixtures/destinations_fixtures.json',
        'fixtures/users_fixtures.json',
        "fixtures/packages_fixtures.json",
        "fixtures/types_fixtures.json",

    ]

    def setUp(self) -> None:
        # self.user = User.objects.get(email="testuserone@email.com")
        # self.package = packages_model.objects.get(
        #     slug= "test-package-one"
        # )

        self.data = {
            "kids":  1,
            "adults": 2,
            "arrival_date":  date(2023, 12, 2),
            "arrival_time": time(12, 12, 00),
            "airlines": "some airlines",
            "flight_number": "A2345",
        }

    def test_form_valid(self) -> None:
        form = BookingForm(data=self.data)
        if not form.is_valid():
            print("form-errors:", form.errors)

        self.assertTrue(form.is_valid())

    


        