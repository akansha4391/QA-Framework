import os
import pytest
from qa_framework.core.config import FrameworkSettings

def test_settings_load_defaults(mocker):
    """Test that default values are loaded when no env vars are present."""
    # Mock environment to be empty
    mocker.patch.dict(os.environ, {}, clear=True)
    
    settings = FrameworkSettings()
    assert settings.LOG_LEVEL == "INFO"
    assert settings.HEADLESS is False # It is False by default in the file I just saw


def test_settings_load_env_vars(mocker):
    """Test that environment variables override defaults."""
    mocker.patch.dict(os.environ, {
        "BASE_URL": "https://staging.example.com",
        "BROWSER": "firefox",
        "HEADLESS": "false"
    })
    
    settings = FrameworkSettings()
    assert str(settings.BASE_URL) == "https://staging.example.com"
    assert settings.BROWSER == "firefox"
    assert settings.HEADLESS is False
