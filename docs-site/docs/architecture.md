---
sidebar_position: 3
---

# Architecture

The framework follows a **Core Library** architecture, intended to be installed as a dependency in your test projects.

## High-Level Design

```mermaid
graph TD
    TestProject[Test Project] --> CoreLib[QA Framework Core]
    CoreLib --> UI[UI Layer]
    CoreLib --> API[API Layer]
    CoreLib --> Data[Data Layer]

    UI --> Factory[Driver Factory]
    Factory --> Selenium[Selenium Driver]
    Factory --> Playwright[Playwright Driver]
    Factory --> Mobile[Mobile Driver (Appium)]

    API --> REST[REST Client]
    API --> GQL[GraphQL Client]

    Data --> DB[DB Manager]
    Data --> Readers[File Readers]
```

## Design Principles

1.  **Abstraction**: Test code interacts with `AbstractDriver` and `BasePage`, not directly with Selenium/Playwright (unless necessary).
2.  **Configuration**: All settings are managed via `pydantic-settings` and `.env` files.
3.  **Logging**: Structured logging using `structlog` ensures traceability.

## Component Breakdown

### 1. Core Library (`qa_framework`)

The standard distribution package installed via pip. It acts as the backbone, providing shared utilities, configuration management, and base classes.

### 2. UI Automation Layer

- **Driver Factory**: A centralization point that reads the configuration (`BROWSER`, `USE_PLAYWRIGHT`, `MOBILE_PLATFORM_NAME`) and instantiates the correct driver (Selenium, Playwright, or Appium).
- **Abstract Driver**: A Python Protocol/Interface that defines standard actions (`goto`, `click`, `get_title`) to ensure test code remains agnostic of the underlying engine. Mobile actions are also adapted to this interface where applicable.
- **Page Object Model (POM)**: The `BasePage` class encapsulates common page interactions, promoting code reuse and modularity.

### 3. API Automation Layer

- **API Client**: A wrapper around the `requests` library that automatically handles:
  - Session management
  - Request/Response Logging (headers, body, duration)
  - Error status verification (raises custom `APIGatewayError`)
- **GraphQL Client**: Extends the API Client to handle query/mutation structures and variable payloads natively.

### 4. Data Layer

- **DB Manager**: A SQLAlchemy-based manager that handles database connections, session scoping, and teardown automatically.
- **File Readers**: Utilities to parse **JSON**, **YAML**, **CSV**, and **XLSX** files into native Python objects.

## Execution Flow

The following pointer list describes the lifecycle of a typical test run:

1.  **Initialization Phase**
    - The test runner (Pytest) starts.
    - `conftest.py` loads the **Settings** from `.env` via Pydantic.
    - **Logger** is configured (JSON or Console mode).
2.  **Setup Phase**
    - **Driver Factory** initializes the browser (e.g., launching Chrome Headless via Playwright).
    - **DB Manager** creates a connection pool if a database string is provided.
    - Test Data is loaded from external files (YAML/JSON) using **File Readers**.
3.  **Execution Phase**
    - Test Function calls a **Page Object** method (e.g., `login_page.login()`).
    - The **Page Object** delegates the action to the **Abstract Driver**.
    - The **Driver** executes the command on the browser instance.
    - For API tests, the **API Client** sends the HTTP request and validates the response code.
4.  **Reporting Phase**
    - All actions and API calls are logged via `structlog`.
    - On failure, the `AllureListener` captures a screenshot and attaches it to the report.
    - `Allure` generates the XML/JSON results.
5.  **Teardown Phase**
    - Browser session is closed (`driver.quit()`).
    - Database sessions are rolled back/closed.
    - Temporary files are cleaned up.
