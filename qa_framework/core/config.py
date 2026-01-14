from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path
from typing import Optional

class FrameworkSettings(BaseSettings):
    """
    Core Configuration for the QA Framework.
    Loads from .env file or environment variables.
    """
    # General
    BASE_URL: str = Field(default="http://localhost", description="Base URL for the application under test")
    ENV: str = Field(default="dev", description="Environment (dev, qa, staging, prod)")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # UI Automation
    BROWSER: str = Field(default="chrome", description="Browser to use (chrome, firefox, edge, webkit)")
    HEADLESS: bool = Field(default=False, description="Run in headless mode")
    IMPLICIT_WAIT: int = Field(default=10, description="Implicit wait time in seconds")
    USE_PLAYWRIGHT: bool = Field(default=False, description="Use Playwright backend instead of Selenium")
    
    # Mobile Automation
    MOBILE_PLATFORM_NAME: Optional[str] = Field(default=None, description="Mobile Platform (Android, iOS)")
    MOBILE_DEVICE_NAME: Optional[str] = Field(default=None, description="Device Name (e.g. Pixel_4_API_30, iPhone 12)")
    MOBILE_APP_PATH: Optional[str] = Field(default=None, description="Path to .apk or .app file")
    MOBILE_UDID: Optional[str] = Field(default=None, description="Device UDID for real devices")
    APPIUM_SERVER_URL: str = Field(default="http://localhost:4723", description="Appium Server URL")

    # Cloud Grid (SauceLabs/BrowserStack)
    REMOTE_GRID_URL: Optional[str] = Field(default=None, description="Remote Grid URL (e.g., https://username:key@hub-cloud.browserstack.com/wd/hub)")
    
    # Security (OWASP ZAP)
    USE_ZAP_PROXY: bool = Field(default=False, description="Route traffic through ZAP Proxy")
    ZAP_BASE_URL: str = Field(default="http://localhost:8080", description="ZAP Proxy URL")
    ZAP_API_KEY: Optional[str] = Field(default=None, description="ZAP API Key")

    # Self Healing
    ENABLE_SELF_HEALING: bool = Field(default=True, description="Enable AI/Heuristic Self Healing for selectors")

    # Database
    DB_CONNECTION_STRING: Optional[str] = Field(default=None, description="Database connection string")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Singleton instance
settings = FrameworkSettings()
