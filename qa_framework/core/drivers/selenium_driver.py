from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from qa_framework.core.drivers.abstract_driver import AbstractDriver
from qa_framework.core.config import settings
from qa_framework.core.logger import get_logger
from qa_framework.core.exceptions import DriverInitializationError

logger = get_logger("selenium_driver")

class SeleniumDriver(AbstractDriver):
    """
    Selenium implementation of the AbstractDriver.
    """
    def __init__(self):
        self.driver = None

    def start(self) -> None:
        try:
            browser = settings.BROWSER.lower()
            headless = settings.HEADLESS
            
            logger.info("Initializing Selenium Driver", browser=browser, headless=headless)

            if browser == "chrome":
                options = ChromeOptions()
                if headless:
                    options.add_argument("--headless")
                
                if settings.REMOTE_GRID_URL:
                    self.driver = webdriver.Remote(command_executor=settings.REMOTE_GRID_URL, options=options)
                else:
                    self.driver = webdriver.Chrome(options=options)

            elif browser == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                
                if settings.REMOTE_GRID_URL:
                    self.driver = webdriver.Remote(command_executor=settings.REMOTE_GRID_URL, options=options)
                else:
                    self.driver = webdriver.Firefox(options=options)
            else:
                raise DriverInitializationError(f"Unsupported browser: {browser}")
                
            self.driver.implicitly_wait(settings.IMPLICIT_WAIT)
            self.driver.maximize_window()
            
        except Exception as e:
            logger.error("Failed to initialize Selenium Driver", error=str(e))
            raise DriverInitializationError("Selenium init failed", original_exception=e)

    def quit(self) -> None:
        if self.driver:
            logger.info("Quitting Selenium Driver")
            self.driver.quit()
            self.driver = None

    def goto(self, url: str) -> None:
        self.driver.get(url)

    def get_title(self) -> str:
        return self.driver.title

    def get_driver(self):
        return self.driver

    def screenshot(self, path: str) -> str:
        self.driver.save_screenshot(path)
        return path

    def find_element(self, selector: str):
        """
        Finds an element with Self-Healing capabilities.
        """
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import NoSuchElementException
        from qa_framework.core.healing.healer import Healer

        # Determine strategy (heuristic validation)
        strategy = By.CSS_SELECTOR
        if selector.startswith("//") or selector.startswith("("):
            strategy = By.XPATH
        elif selector.startswith("id="):
            strategy = By.ID
            selector = selector.replace("id=", "")
        elif selector.startswith("name="):
            strategy = By.NAME
            selector = selector.replace("name=", "")

        try:
            return self.driver.find_element(strategy, selector)
        except NoSuchElementException:
            if settings.ENABLE_SELF_HEALING:
                logger.warning(f"Element not found: {selector}. Attempting Self-Healing...")
                healer = Healer(self.driver.page_source)
                new_selector = healer.heal(selector)
                
                if new_selector:
                    logger.info(f"Retrying with healed selector: {new_selector}")
                    # Strategy for healed selector is usually CSS or ID based on Healer logic
                    # For simplicity, if it starts with #, treat as CSS, else CSS (tag name)
                    return self.driver.find_element(By.CSS_SELECTOR, new_selector)
            
            raise

    def click(self, selector: str):
        el = self.find_element(selector)
        el.click()

    def type(self, selector: str, text: str):
        el = self.find_element(selector)
        el.send_keys(text)
