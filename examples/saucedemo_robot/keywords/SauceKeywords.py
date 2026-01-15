from qa_framework.core.drivers.factory import DriverFactory
from qa_framework.core.config import settings

class SauceKeywords:
    def __init__(self):
        self.driver = None

    def open_browser(self):
        self.driver = DriverFactory.get_driver(settings.BROWSER)
        self.driver.goto("https://www.saucedemo.com")

    def login(self, username, password):
        self.driver.type("id=user-name", username)
        self.driver.type("id=password", password)
        self.driver.click("id=login-button")

    def page_should_contain_text(self, text):
        # A simple check using page source or specific element
        # Here we just assume if text is in body
        # For robustness, we should look for specific elements
        found = self.driver.find_element(f"//*[contains(text(), '{text}')]")
        if not found:
            raise AssertionError(f"Text '{text}' not found")
            
    def close_browser(self):
        if self.driver:
            self.driver.quit()
