from typing import Any
from selenium import webdriver

def driver(url: str, browser: str = "firefox", headless:bool = True) -> webdriver:
    """Create a driver instance

    Args:
        live_server_url (str): live_server_url from django LiveServerTestCase
        browser (str, optional): Browser name. Defaults to "firefox".

    Returns:
        webdriver: webdriver
    """
    
    if browser == "chrome":
        BrowserOptions = webdriver.ChromeOptions()
        BrowserOptions.add_argument("-headless") if headless else None
        driver = webdriver.Chrome(options=BrowserOptions)
    else:
        BrowserOptions = webdriver.FirefoxOptions()
        BrowserOptions.add_argument("-headless") if headless else None
        driver = webdriver.Firefox(options=BrowserOptions)

    driver.get(url)

    return driver