import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import NoSuchElementException
from qa_framework.core.drivers.selenium_driver import SeleniumDriver
from qa_framework.core.healing.healer import Healer

def test_self_healing_success(mocker):
    """
    Test that SeleniumDriver attempts to heal a failed selector and retries.
    """
    # Mock Settings
    mocker.patch('qa_framework.core.config.settings.ENABLE_SELF_HEALING', True)
    
    # Mock Selenium WebDriver
    mock_driver = MagicMock()
    mock_driver.page_source = '<html><body><input id="healed_id" name="username_v2" /></body></html>'
    
    # Mock find_element to fail first, then succeed (simulated by logic, but actually we mock the calls)
    # The first call raises NoSuchElementException
    # The second call (retrying with new selector) succeeds
    mock_element = MagicMock()
    
    def side_effect(by, value):
        if value == "username_legacy": # The failed one
            raise NoSuchElementException("Boom")
        if value == "#healed_id": # The healed one
            return mock_element
        raise NoSuchElementException(f"Unexpected: {value}")
        
    mock_driver.find_element.side_effect = side_effect
    
    # Patch the driver inside SeleniumDriver
    driver_wrapper = SeleniumDriver()
    driver_wrapper.driver = mock_driver
    
    # Mock Healer to return a specific selector to ensure deterministic test
    with patch('qa_framework.core.healing.healer.Healer.heal') as mock_heal:
        mock_heal.return_value = "#healed_id"
        
        # ACT
        el = driver_wrapper.find_element("id=username_legacy")
        
        # ASSERT
        assert el == mock_element
        mock_heal.assert_called_once()
        # Ensure we called find_element twice
        assert mock_driver.find_element.call_count == 2
