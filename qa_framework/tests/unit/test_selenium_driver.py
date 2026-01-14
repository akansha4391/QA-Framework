import pytest
from qa_framework.core.drivers.selenium_driver import SeleniumDriver

def test_selenium_remote_grid_init(mocker):
    """Test that SeleniumDriver uses webdriver.Remote when REMOTE_GRID_URL is set."""
    # Mock settings
    mocker.patch('qa_framework.core.config.settings.REMOTE_GRID_URL', 'http://cloud-grid:4444/wd/hub')
    mocker.patch('qa_framework.core.config.settings.BROWSER', 'chrome')
    
    # Mock webdriver.Remote
    mock_remote = mocker.patch('qa_framework.core.drivers.selenium_driver.webdriver.Remote')
    mock_chrome = mocker.patch('qa_framework.core.drivers.selenium_driver.webdriver.Chrome')
    
    driver = SeleniumDriver()
    driver.start()
    
    # Verify Remote was called, not Chrome
    mock_remote.assert_called_once()
    mock_chrome.assert_not_called()
    assert driver.driver == mock_remote.return_value

def test_selenium_local_init(mocker):
    """Test that SeleniumDriver uses local webdriver when REMOTE_GRID_URL is None."""
    # Mock settings
    mocker.patch('qa_framework.core.config.settings.REMOTE_GRID_URL', None)
    mocker.patch('qa_framework.core.config.settings.BROWSER', 'chrome')
    
    # Mock webdrivers
    mock_remote = mocker.patch('qa_framework.core.drivers.selenium_driver.webdriver.Remote')
    mock_chrome = mocker.patch('qa_framework.core.drivers.selenium_driver.webdriver.Chrome')
    
    driver = SeleniumDriver()
    driver.start()
    
    # Verify Chrome was called
    mock_chrome.assert_called_once()
    mock_remote.assert_not_called()
    assert driver.driver == mock_chrome.return_value
