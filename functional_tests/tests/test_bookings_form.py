from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.driver import driver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()


from packages.models import (
    Destination,
    Type,
    Package,
    TourTimeline
)


class BookinFormTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users_fixtures.json',
        'fixtures/packages_fixtures.json',
        'fixtures/destinations_fixtures.json',
        'fixtures/types_fixtures.json',
        ]

    def setUp(self) -> None:
        self.package = Package.objects.get(name="test package one")

        self.booking_url = self.live_server_url + reverse(
            'create-booking',     
            kwargs={
            'package_slug': self.package.slug
            })
        
        self.url = self.live_server_url + reverse(
            'package-detail', 
            kwargs= {
            'package_slug': self.package.slug
        })

        self.browser = driver(self.url, headless=False)
        self.wait = WebDriverWait(self.browser, 10)

        self.wait.until(
            EC.url_matches(self.url)
        )

    # def tearDown(self) -> None:
    #     self.browser.quit()

    def test_booking_form_displayed(self) -> None:
        self.assertEquals(self.browser.title.lower(), "package detail")
        
        booking_form = self.browser.find_element(By.ID, "booking-form")
        self.assertTrue(booking_form.is_displayed())



    # def test_booking_form_submission(self) -> None:

    #     # --------> Test signup form submission
    #     form_set = self.browser.find_elements(By.CSS_SELECTOR, "div.form-set")
    #     for set in form_set:
    #         input_field = set.find_element(By.TAG_NAME, "input")
    #         input_field.clear()
    #         input_type = input_field.get_attribute("name")
    #         if input_type == "email":
    #             input_field.send_keys("testuserthree@email.com")
    #         elif input_type == "password": 
    #             input_field.send_keys("#Stone4crows")
    #         elif input_type == "confirm_password": 
    #             input_field.send_keys("#Stone4crows")

    #     submit_button = self.browser.find_element(
    #         By.CSS_SELECTOR, "button#signup_button")
    #     submit_button.click()
    #     self.wait.until(
    #         EC.url_matches(self.success_url)
    #     )

    #     # ------>check the success mess alertt
    #     self.wait.until(
    #         EC.presence_of_element_located(
    #             (By.CSS_SELECTOR, "ul#toast-messages li.message p.success")
    #             ))

    #     message = self.browser.find_element(
    #         By.CSS_SELECTOR, "ul#toast-messages li.message p.success")

    #     self.assertEquals(
    #         "Success: Your account has been created successfully, and you\'re logged in.", message.text)


    # def test_signup_form_invalid_input_fields(self) -> None:

    #     form_set = self.browser.find_elements(By.CSS_SELECTOR, "div.form-set")
    #     for field in form_set:
    #         input_field = field.find_element(By.TAG_NAME, "input")
    #         input_field.clear()
    #         input_type = input_field.get_attribute("name")
    #         if input_type == "email":
    #             input_field.send_keys("wrongemail@")
    #             input_field.send_keys(Keys.TAB)

    #         elif input_type == "password": 
    #             input_field.send_keys("#notStonengkn")
    #             input_field.send_keys(Keys.TAB)
            
    #         elif input_type == "confirm_password": 
    #             input_field.send_keys("mismatching")
    #             input_field.send_keys(Keys.TAB)
          
    #     expected_messages =[
    #         "Please enter a valid email",
    #         "Please enter a valid password, password must contain atleast one uppercase, lowercase, number and symbol",
    #         "Password and Confirm Password must match"
    #     ]
    #     error_messages = self.browser.find_elements(
    #         By.CLASS_NAME, "field-error")

    #     for message in error_messages:
    #         self.assertTrue(message.text in expected_messages)






        