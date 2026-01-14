from typing import Any, Dict, List
from qa_framework.core.drivers.abstract_driver import AbstractDriver
from qa_framework.core.drivers.selenium_driver import SeleniumDriver
from qa_framework.core.drivers.playwright_driver import PlaywrightDriver
from qa_framework.core.logger import get_logger

logger = get_logger("a11y_manager")

class AccessibilityManager:
    """
    Manager to run Accessibility checks using Axe-core.
    Supports both Selenium and Playwright.
    """
    
    def __init__(self, driver: AbstractDriver):
        self.driver = driver

    def scan(self) -> Dict[str, Any]:
        """
        Runs an accessibility scan on the current page.
        Returns the full report.
        """
        logger.info("Starting Accessibility Scan...")
        report = {}

        if isinstance(self.driver, SeleniumDriver):
            from axe_selenium_python import Axe
            axe = Axe(self.driver.driver)
            axe.inject()
            report = axe.run()
        
        elif isinstance(self.driver, PlaywrightDriver):
            from axe_playwright_python.sync_playwright import Axe
            # Axe for Playwright works on the Page object
            axe = Axe()
            # We need to access the underlying Playwright Page object
            # Assuming PlaywrightDriver exposes .page or similar
            if hasattr(self.driver, 'page'):
                report = axe.run(self.driver.page)
            else:
                logger.error("PlaywrightDriver does not expose 'page' object for Axe scan.")
                return {"error": "Driver incompatibility"}

        else:
            logger.warning("Accessibility Scan not supported for this driver type.")
            return {"error": "Unsupported driver"}

        violations = report.get("violations", [])
        if violations:
            logger.error(f"Accessibility Violations Found: {len(violations)}")
            for v in violations:
                logger.error(f"Violation: {v['id']} - {v['description']}")
        else:
            logger.info("No Accessibility Violations Found.")
            
        return report
