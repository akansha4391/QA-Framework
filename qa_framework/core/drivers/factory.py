from qa_framework.core.drivers.abstract_driver import AbstractDriver
from qa_framework.core.drivers.selenium_driver import SeleniumDriver
from qa_framework.core.drivers.playwright_driver import PlaywrightDriver
from qa_framework.core.drivers.mobile_driver import MobileDriver
from qa_framework.core.config import settings
from qa_framework.core.exceptions import DriverInitializationError

class DriverFactory:
    """
    Factory to create the appropriate driver instance based on configuration.
    """
    @staticmethod
    def get_driver() -> AbstractDriver:
        # Check for Mobile First
        if settings.MOBILE_PLATFORM_NAME:
            driver = MobileDriver()
        elif settings.USE_PLAYWRIGHT:
            driver = PlaywrightDriver()
        else:
            driver = SeleniumDriver()
        
        driver.start()
        return driver
