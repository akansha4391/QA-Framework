import pytest
import os
import sys

# Ensure root dir is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from qa_framework.core.drivers.factory import DriverFactory

@pytest.fixture(scope="function")
def driver():
    """
    Fixture to initialize driver for each test.
    """
    driver_instance = DriverFactory.get_driver()
    yield driver_instance
    driver_instance.quit()
