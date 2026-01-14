from playwright.sync_api import sync_playwright, Page, Browser
from qa_framework.core.drivers.abstract_driver import AbstractDriver
from qa_framework.core.config import settings
from qa_framework.core.logger import get_logger
from qa_framework.core.exceptions import DriverInitializationError

logger = get_logger("playwright_driver")

class PlaywrightDriver(AbstractDriver):
    """
    Playwright implementation of the AbstractDriver.
    """
    def __init__(self):
        self._playwright = None
        self._browser: Browser = None
        self._page: Page = None

    def start(self) -> None:
        try:
            logger.info("Initializing Playwright Driver", browser=settings.BROWSER, headless=settings.HEADLESS)
            self._playwright = sync_playwright().start()
            
            browser_type = settings.BROWSER.lower()
            launch_args = {"headless": settings.HEADLESS}

            if browser_type == "chrome":
                self._browser = self._playwright.chromium.launch(**launch_args)
            elif browser_type == "firefox":
                self._browser = self._playwright.firefox.launch(**launch_args)
            elif browser_type == "webkit":
                self._browser = self._playwright.webkit.launch(**launch_args)
            else:
                # Default to chromium if unknown, or raise error
                 self._browser = self._playwright.chromium.launch(**launch_args)
            
            self._page = self._browser.new_page()

        except Exception as e:
            logger.error("Failed to initialize Playwright Driver", error=str(e))
            raise DriverInitializationError("Playwright init failed", original_exception=e)

    def quit(self) -> None:
        if self._browser:
            logger.info("Quitting Playwright Driver")
            self._browser.close()
            self._playwright.stop()
            self._page = None
            self._browser = None
            self._playwright = None

    def goto(self, url: str) -> None:
        self._page.goto(url)

    def get_title(self) -> str:
        return self._page.title()

    def get_driver(self):
        return self._page

    @property
    def page(self) -> Page:
        return self._page

    def screenshot(self, path: str) -> str:
        self._page.screenshot(path=path)
        return path
