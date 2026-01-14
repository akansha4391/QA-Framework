from typing import Any
from qa_framework.core.drivers.abstract_driver import AbstractDriver
from qa_framework.core.logger import get_logger

logger = get_logger("base_page")

class BasePage:
    """
    Base class for all Page Objects.
    """
    def __init__(self, driver: AbstractDriver):
        self.driver = driver

    def open(self, url: str) -> None:
        """Opens the specified URL."""
        logger.info(f"Navigating to {url}")
        self.driver.goto(url)

    def get_title(self) -> str:
        """Returns the page title."""
        return self.driver.get_title()

    def screenshot(self, filename: str) -> str:
        """Takes a screenshot."""
        return self.driver.screenshot(filename)
    
    # NOTE:
    # Because Selenium and Playwright handle element location differently 
    # (WebElement vs Locator), specific interactions (click, type) are best 
    # implemented in the specific page objects or by exposing the 
    # native driver via self.driver.get_driver() if complex interaction is needed.
    #
    # However, for a fully abstract framework, we could add methods like:
    # def click(self, selector: str): ...
    # But that requires mapping universal selectors to specific driver calls.
    # For now, we prefer keeping it light.
