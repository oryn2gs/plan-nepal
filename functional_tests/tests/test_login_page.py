from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.driver import driver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginPageTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users_fixtures.json',
        ]

    def setUp(self) -> None:
        self.url = self.live_server_url + reverse('signin')
        self.success_url = self.live_server_url + reverse('homepage')

        self.browser = driver(self.url)
        self.wait = WebDriverWait(self.browser, 10)

        self.wait.until(
            EC.url_matches(self.url)
        )

    def tearDown(self) -> None:
        self.browser.quit()

    def test_form_displayed(self) -> None:
        self.assertEquals(self.browser.title.lower(), "signin")
        
        login_form = self.browser.find_element(By.ID, "login-form")
        self.assertTrue(login_form.is_displayed())

    def test_reset_password_link(self) -> None:
        reset_link = self.browser.find_element(
            By.CSS_SELECTOR, "a.reset-link"
            )
        #! Check when set
        # self.assertEquals(reset_link.get_attribute("href"), )

    def test_signup_link(self) -> None:
        signup_link = self.browser.find_element(
            By.LINK_TEXT, "signup"
            )
        self.assertEqual(
            signup_link.get_attribute("href"), 
            self.live_server_url + reverse('signup')
        )


    def test_login_form_submission(self) -> None:
        self.user = User.objects.get(email="testuserone@email.com")

        # --------> Test login form submission
        form_set = self.browser.find_elements(By.CSS_SELECTOR, "div.form-set")
        for set in form_set:
            input_field = set.find_element(By.TAG_NAME, "input")
            input_field.clear()
            input_type = input_field.get_attribute("name")
            if input_type == "email":
                input_field.send_keys(self.user.email)
            elif input_type == "password": 
                input_field.send_keys("#Stone4crows")

        submit_button = self.browser.find_element(
            By.CSS_SELECTOR, "button#login_button")
        submit_button.click()
        self.wait.until(
            EC.url_matches(self.success_url)
        )

        # ------>check the success mess alertt
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul#toast-messages li.message p.success"))
        )

        message = self.browser.find_element(
            By.CSS_SELECTOR, "ul#toast-messages li.message p.success")


        self.assertEquals("Success: Login in successfully.", message.text)


    def test_login_form_invalid_input_fields(self) -> None:

        form_set = self.browser.find_elements(By.CSS_SELECTOR, "div.form-set")
        for field in form_set:
            input_field = field.find_element(By.TAG_NAME, "input")
            input_field.clear()
            input_type = input_field.get_attribute("name")
            if input_type == "email":
                input_field.send_keys("wrongemail@")
                input_field.send_keys(Keys.TAB)

            elif input_type == "password": 
                input_field.send_keys("")
                input_field.send_keys(Keys.TAB)
          
        expected_messages =[
            "Please enter a valid email",
            "Please enter a valid password",
        ]
        error_messages = self.browser.find_elements(
            By.CLASS_NAME, "field-error")

        for message in error_messages:
            self.assertTrue(message.text in expected_messages)






        