import os
import sys

# Add the project root to sys.path to run without installing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qa_framework.core.drivers.factory import DriverFactory
from qa_framework.core.config import settings
from qa_framework.core.logger import get_logger

logger = get_logger("demo")

def run_demo():
    logger.info("Starting Demo")
    
    # Override settings for demo
    settings.BROWSER = "chrome"
    settings.HEADLESS = True
    settings.USE_PLAYWRIGHT = True 

    try:
        driver = DriverFactory.get_driver()
        logger.info("Driver Initialized")
        
        driver.goto("https://www.google.com")
        title = driver.get_title()
        logger.info(f"Page Title: {title}")
        
        driver.quit()
        logger.info("Demo Completed Successfully")
    except Exception as e:
        logger.error(f"Demo Failed: {e}")
        # Explicitly quit if failed
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    run_demo()
