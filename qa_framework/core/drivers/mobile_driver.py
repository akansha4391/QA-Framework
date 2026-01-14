from typing import Dict, Any, Optional
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from qa_framework.core.drivers.abstract_driver import AbstractDriver
from qa_framework.core.config import settings
from qa_framework.core.logger import get_logger
from qa_framework.core.exceptions import DriverInitializationError, ElementInteractionError

logger = get_logger("mobile.driver")

class MobileDriver(AbstractDriver):
    """
    Appium-based driver for Mobile Automation (Android/iOS).
    """

    def __init__(self):
        self.driver = None
        self.platform = settings.MOBILE_PLATFORM_NAME.lower() if settings.MOBILE_PLATFORM_NAME else None

    def start(self):
        logger.info(f"Initializing Mobile Driver for platform: {self.platform}")
        
        if not self.platform:
            raise DriverInitializationError("MOBILE_PLATFORM_NAME is not set in configuration.")

        try:
            options = self._get_options()
            self.driver = webdriver.Remote(command_executor=settings.APPIUM_SERVER_URL, options=options)
            logger.info("Mobile Driver initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Appium Driver: {e}")
            raise DriverInitializationError(f"Appium Init Failed: {e}")

    def _get_options(self) -> AppiumOptions:
        if self.platform == 'android':
            options = UiAutomator2Options()
        elif self.platform == 'ios':
            options = XCUITestOptions()
        else:
            raise DriverInitializationError(f"Unsupported mobile platform: {self.platform}")

        # Common Capabilities
        if settings.MOBILE_DEVICE_NAME:
            options.device_name = settings.MOBILE_DEVICE_NAME
        if settings.MOBILE_APP_PATH:
            options.app = settings.MOBILE_APP_PATH
        if settings.MOBILE_UDID:
            options.udid = settings.MOBILE_UDID
        
        # Merge any extra caps if needed (could be extended via config)
        return options

    def quit(self):
        if self.driver:
            logger.info("Quitting Mobile Driver")
            self.driver.quit()

    def goto(self, url: str):
        # For mobile apps, goto might be deep links or irrelevant
        logger.warning("goto() called on MobileDriver. Using 'get' for potential Deep Link or Hybrid implementation.")
        self.driver.get(url)

    def find_element(self, selector: str) -> Any:
        try:
            # Defaulting to Accessibility ID or XPath depending on selector content
            if selector.startswith("//") or selector.startswith("("):
                return self.driver.find_element("xpath", selector)
            else:
                # Assume Accessibility ID by default for robust mobile automation
                return self.driver.find_element("accessibility id", selector)
        except Exception as e:
            raise ElementInteractionError(f"Could not find element: {selector}", e)

    def click(self, selector: str):
        element = self.find_element(selector)
        logger.info(f"Clicking element: {selector}")
        element.click()

    def type(self, selector: str, text: str):
        element = self.find_element(selector)
        logger.info(f"Typing '{text}' into {selector}")
        element.send_keys(text)

    def get_title(self) -> str:
        return self.driver.title # Often context dependent in native apps

    def screenshot(self, path: str):
        logger.info(f"Saving screenshot to {path}")
        self.driver.save_screenshot(path)
