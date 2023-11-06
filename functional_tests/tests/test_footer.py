from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from functional_tests.driver import driver


class FooterTestCase(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = driver(self.live_server_url)
        self.wait = WebDriverWait(self.browser, 10)

        self.about_us_url = self.live_server_url  + reverse('about-us')
        self.faq_url = self.live_server_url  + reverse('faq-list')

        from django.conf import settings
        settings.DEBUG = True

    def tearDown(self) -> None:
        self.browser.quit()


    def test_footer_links_has_a_correct_url(self) -> None:
        
        footer_links = self.browser.find_elements(
            By.CSS_SELECTOR, "ul#footer-links > li:not(:last-child) a"
            )
        expected_urls = {
            'about us' : self.live_server_url + reverse('about-us'),
            'faq' : self.live_server_url + reverse('faq-list')
        }

        for link in footer_links:
            name = link.text.strip().lower()
            href = link.get_attribute("href")

            self.assertEqual(href, expected_urls[name])
            # check the links matches with the desired url
        
        
    def test_footer_social_links_has_a_correct_url(self) -> None:
        social_links_container = self.browser.find_element(
            By.ID, "footer-social-links"
            )
        buttons = social_links_container.find_elements(By.CSS_SELECTOR, "a")

        expected_urls = {
            'facebook': "https://www.facebook.com/plannepal/",
            'twitter': "https://twitter.com/plannepaltravel",
            'instagram': "https://www.instagram.com/nepal_tourtrek/",
            'pinterest': "https://www.pinterest.com/plannepaltravel/",
        }

        for button in buttons:
            button_class = button.get_attribute("class")
            button_class = [name != "icon" for name in button_class.split()]

            for button in button_class:
                if button in expected_urls:
                    expected_url = expected_urls[button_class]
                    self.assertEquals(
                        button.get_attribute("href"), expected_url
                        )



    def test_subcription_email_form(self) -> None:
        # write a test after the view i scomplete
        subs_form = self.browser.find_element(By.ID, "subcribtion-form")
        email_field = subs_form.find_element(By.NAME, "email")
        print(subs_form, email_field)
        email_field.send_keys("oryn2gs@gmail.com")



        pass