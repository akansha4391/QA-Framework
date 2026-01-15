from pytest_bdd import scenario, given, when, then, parsers
from qa_framework.core.drivers.factory import DriverFactory
from qa_framework.core.config import settings
import pytest

# Constants
LOGIN_URL = "https://www.saucedemo.com/"

@pytest.fixture(scope="function")
def driver():
    d = DriverFactory.get_driver(settings.BROWSER)
    yield d
    d.quit()

@scenario('../features/login.feature', 'Successful Login')
def test_login():
    pass

@given("I am on the sauce demo login page")
def open_login_page(driver):
    driver.goto(LOGIN_URL)

@when("I login with valid credentials")
def list_items(driver):
    driver.type("id=user-name", "standard_user")
    driver.type("id=password", "secret_sauce")
    driver.click("id=login-button")

@then("I should see the inventory page")
def verify_inventory(driver):
    assert "inventory" in driver.get_current_url()
    assert "Products" in driver.get_text(".title")
