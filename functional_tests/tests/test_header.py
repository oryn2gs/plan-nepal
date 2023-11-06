
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.driver import driver

from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
User = get_user_model()


class HeaderTestCase(StaticLiveServerTestCase):
    fixtures = ['fixtures/users_fixtures.json']

    def setUp(self) -> None:
        self.browser = driver(self.live_server_url)
        self.wait = WebDriverWait(self.browser, 10)

        self.signin_url = self.live_server_url + reverse('signin')
        self.signup_url = self.live_server_url + reverse('signup')
        self.signout_url = self.live_server_url + reverse('signout')

    def tearDown(self) -> None:
        self.browser.quit()

    def test_about_us_link(self) -> None:
        header_list = self.browser.find_element(By.ID, "header-list")
        about_link = header_list.find_element(By.LINK_TEXT, "About us")
        about_link.click()
        self.wait.until(
            EC.url_matches(self.live_server_url + reverse('about-us'))            
        )

    def test_accounts_signin_link_navigation(self) -> None:
        """ for unauthenticated users """

        try:
            account_button = self.browser.find_element(By.CSS_SELECTOR, "div#dropdown-btn.authenticate")
        except:
            None

        if account_button:
            account_button.click()
            self.wait.until(
                EC.visibility_of_element_located((By.ID, "dropdown-menu"))
            )
            account_menu = account_button.find_element(By.ID, "dropdown-menu")
            # check if the signin link navigates to signin link
            signin_button = account_menu.find_element(By.CSS_SELECTOR, "a[href='{}']".format(reverse('signin')))
            
            signin_button.click()
            self.wait.until(
                EC.url_matches(self.signin_url)
            )
            self.assertEqual(self.browser.current_url, self.signin_url)

    
    def test_accounts_signup_link_navigation(self) -> None:
        """ for unauthenticated users """

        try:
            account_button = self.browser.find_element(By.CSS_SELECTOR, "div#dropdown-btn.authenticate")
        except:
            None

        if account_button:
            account_button.click()
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.ID, "dropdown-menu"))
            )
            account_menu = account_button.find_element(By.ID, "dropdown-menu")
            signup_button = account_menu.find_element(
                By.CSS_SELECTOR, "a[href='{}']".format(reverse('signup')
                ))
            signup_button.click()
            WebDriverWait(self.browser, 10).until(
                EC.url_matches(self.signup_url)
            )
            self.assertEqual(self.browser.current_url, self.signup_url)

    def test_signout_links_for_authenticated_users(self) -> None:
    
        self.user = User.objects.get(email="testuserone@email.com")
        
        self.client.force_login(self.user)
        # !issue with finding the element.
        self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "div#dropdown-btn.account"
                ))
        )
   
        account_button = self.browser.find_element(
            By.CSS_SELECTOR, "div#dropdown-btn.account"
            )
        if account_button:
            account_button.click()
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#dropdown-btn > #dropdown-menu")
                    )
            )

            dropdown_menu = account_button.find_element(By.ID, "dropdown-menu")
            signout_button = dropdown_menu.find_element(By.CSS_SELECTOR, "ul li form button")
            signout_button.click()
            self.wait.until(
                EC.url_matches(self.signout_url)
            )




        


