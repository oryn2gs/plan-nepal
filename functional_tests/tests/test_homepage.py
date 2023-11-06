
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.driver import driver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse


class HomepageTestCase(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = driver(self.live_server_url)


    def tearDown(self) -> None:
        self.browser.quit()

    def test_homepage_render_success(self) -> None:
        self.assertEquals(self.browser.title, "homepage")
        hero_header = self.browser.find_element(By.CLASS_NAME, "hero-section__header")
        self.assertEquals(hero_header.text, "Blessed are the curious for they shall have adventures.")
    

    def test_faq_button_render_and_navigation_success_to_faq_page(self) -> None:
        faq_button = self.browser.find_element(By.LINK_TEXT, "Ask us Question")
        self.assertTrue(faq_button.is_displayed())
        faq_button.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('faq-list'))


class PackageCardTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/packages_fixtures.json', 
        'fixtures/destinations_fixtures.json', 
        'fixtures/types_fixtures.json'
        ]

    def setUp(self) -> None:
        self.browser = driver(self.live_server_url)
        self.wait = WebDriverWait(self.browser, 10)
      
    def tearDown(self) -> None:
        self.browser.quit()

    def test_pill_button_function(self) -> None:
        """ test pill button and its functions """

        pill_buttons = self.browser.find_elements(
            By.CSS_SELECTOR, "#package-slide button"
            )

        second_button = pill_buttons[1] # cause the first button is a default with the value of "All"
        button_text = second_button.text 

        second_button.click()
        self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "package-card"))
        )

        card_container = self.browser.find_element(By.ID, "card-container")
        package_cards = card_container.find_elements(By.CSS_SELECTOR, "div.package-card")
        for card in package_cards:
            self.assertEquals(
                button_text, card.get_attribute("data-type")
                ) # checks if the data-types of the fresh rendered cards is same as the filtered value ----(which is button text)



    def test_package_card_rendered(self) -> None:
      
        package_cards = self.browser.find_elements(By.CSS_SELECTOR, "div.package-card")

        for package_card in package_cards:
            self.assertTrue(package_card.is_displayed())

        # ---- test package details url 
        card_container = self.browser.find_element(By.ID, "card-container")
        first_card = card_container.find_element(
            By.CSS_SELECTOR, "div:first-child"
            )
        slug = first_card.get_attribute("data-id")
        book_button = first_card.find_element(By.LINK_TEXT, "Book Now")
        book_button.click()
        expected_url = self.live_server_url + f"/packages/{slug}/"
        WebDriverWait(self.browser, 10).until(
            EC.url_matches(expected_url)
        )
      
        self.assertEqual(self.browser.current_url, expected_url)
        


    

        # get the first card with the data-id of "everest-treaking"
        # find the button with the link text of book now
        # click the buttton and check if the navigation url == to live_url + reverse('package-detail')


class TestimonialTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/testimonials_fixtures.json', 'fixtures/users_fixtures.json']

    def setUp(self) -> None:
        self.browser = driver(self.live_server_url)
        self.browser.implicitly_wait(10)
      
    def tearDown(self) -> None:
        self.browser.quit()      

    def test_testimonial_card_rendered(self) -> None:
        testimonial_cards = self.browser.find_elements(
            By.CLASS_NAME, "testimonial-card"
            )
        for testimonial in testimonial_cards:
            self.assertTrue(testimonial.is_displayed())
        





        
    



        


        

    


        


    