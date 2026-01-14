import pytest
from qa_framework.core.drivers.factory import DriverFactory
from qa_framework.core.drivers.selenium_driver import SeleniumDriver
from qa_framework.core.drivers.playwright_driver import PlaywrightDriver
from qa_framework.core.exceptions import DriverInitializationError

def test_get_selenium_driver(mocker):
    """Test that SeleniumDriver is initialized when browser is chrome/firefox."""
    mocker.patch('qa_framework.core.config.settings.USE_PLAYWRIGHT', False)
    # Mock the actual driver init to allow running without browser
    mocker.patch('qa_framework.core.drivers.selenium_driver.webdriver.Chrome')
    
    driver = DriverFactory.get_driver()
    assert isinstance(driver, SeleniumDriver)

def test_get_playwright_driver(mocker):
    """Test that PlaywrightDriver is initialized when USE_PLAYWRIGHT is True."""
    mocker.patch('qa_framework.core.config.settings.USE_PLAYWRIGHT', True)
    # Mock Playwright sync_playwright
    mock_playwright = mocker.patch('qa_framework.core.drivers.playwright_driver.sync_playwright')
    
    driver = DriverFactory.get_driver()
    assert isinstance(driver, PlaywrightDriver)


