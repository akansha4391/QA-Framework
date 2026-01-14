from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    # Selectors
    USERNAME_INPUT = "id=user-name"
    PASSWORD_INPUT = "id=password"
    LOGIN_BUTTON = "id=login-button"
    ERROR_MESSAGE = "css=h3[data-test='error']"

    def navigate(self):
        self.driver.goto(self.URL)

    def login(self, username, password):
        self.driver.type(self.USERNAME_INPUT, username)
        self.driver.type(self.PASSWORD_INPUT, password)
        self.driver.click(self.LOGIN_BUTTON)
    
    def get_error_message(self):
        return self.driver.get_text(self.ERROR_MESSAGE)
