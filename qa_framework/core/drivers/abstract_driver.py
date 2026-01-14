from abc import ABC, abstractmethod
from typing import Any

class AbstractDriver(ABC):
    """
    Abstract interface for UI Drivers (Selenium/Playwright).
    Does not enforce a specific inner driver type.
    """

    @abstractmethod
    def start(self) -> None:
        """Starts the driver session."""
        pass

    @abstractmethod
    def quit(self) -> None:
        """Terminates the driver session."""
        pass

    @abstractmethod
    def goto(self, url: str) -> None:
        """Navigates to the specified URL."""
        pass

    @abstractmethod
    def get_title(self) -> str:
        """Returns the page title."""
        pass
    
    @abstractmethod
    def get_driver(self) -> Any:
        """Returns the underlying driver object (WebDriver or Page)."""
        pass
    
    @abstractmethod
    def screenshot(self, path: str) -> str:
        """Takes a screenshot and saves it to the path."""
        pass
