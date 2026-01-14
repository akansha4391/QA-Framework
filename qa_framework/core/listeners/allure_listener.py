import allure
from qa_framework.core.drivers.abstract_driver import AbstractDriver

class AllureListener:
    """
    Helper methods for Allure Reporting.
    """
    @staticmethod
    def attach_screenshot(driver: AbstractDriver, name: str = "Screenshot"):
        """
        Attaches a screenshot to the Allure report.
        """
        try:
            # We need to get the binary data
            if hasattr(driver, 'get_driver'):
                inner_driver = driver.get_driver()
                # Selenium
                if hasattr(inner_driver, 'get_screenshot_as_png'):
                    allure.attach(
                        inner_driver.get_screenshot_as_png(),
                        name=name,
                        attachment_type=allure.attachment_type.PNG
                    )
                # Playwright
                elif hasattr(inner_driver, 'screenshot'):
                    allure.attach(
                        inner_driver.screenshot(),
                        name=name,
                        attachment_type=allure.attachment_type.PNG
                    )
        except Exception as e:
            print(f"Failed to attach screenshot: {e}")
