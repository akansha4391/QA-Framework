---
sidebar_position: 4
---

# User Guide

## Configuration

Create a `.env` file in your project root:

```ini
BASE_URL="https://example.com"
BROWSER="chrome"
HEADLESS=true
USE_PLAYWRIGHT=true

# Mobile Automation
MOBILE_PLATFORM_NAME="Android"
MOBILE_DEVICE_NAME="Pixel_4"
MOBILE_APP_PATH="/path/to/app.apk"

# Cloud Grid
REMOTE_GRID_URL="https://user:key@hub-cloud.browserstack.com/wd/hub"
```

## Creating a Page Object

```python
from qa_framework.core.drivers.base_page import BasePage

class HomePage(BasePage):
    def search(self, text: str):
        # Implementation depends on the driver, but generic actions:
        self.driver.goto("/")
        # Access raw driver for specific element interactions
        # self.driver.get_driver()...
```

## Running Tests

We recommend `pytest`:

```bash
pytest tests/ --alluredir=./results
allure serve ./results
```
