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
    Factory --> Mobile["Mobile Driver (Appium)"]

    API --> REST[REST Client]
    API --> GQL[GraphQL Client]

    Data --> DB[DB Manager]
    Data --> Readers[File Readers]
```

## Design Principles

1.  **Abstraction**: Test code interacts with `AbstractDriver` and `BasePage`, not directly with Selenium/Playwright.
2.  **Configuration**: All settings are managed via `pydantic-settings` and `.env` files.
3.  **Logging**: Structured logging using `structlog` ensures traceability.

## Low-Level Design (LLD)

### 1. Driver Factory Class Diagram

This diagram validates the **Factory Pattern** and **Strategy Pattern** used to switch between Selenium, Playwright, and Appium.

```mermaid
classDiagram
    class DriverFactory {
        +get_driver() AbstractDriver
    }

    class AbstractDriver {
        <<interface>>
        +start()
        +quit()
        +goto(url)
        +find_element(selector)
        +click(selector)
    }

    class SeleniumDriver {
        +driver: WebDriver
        +start()
        +find_element()
    }

    class PlaywrightDriver {
        +page: Page
        +start()
        +find_element()
    }

    class MobileDriver {
        +driver: Remote
        +start()
    }

    DriverFactory ..> AbstractDriver : Returns
    AbstractDriver <|-- SeleniumDriver : Implements
    AbstractDriver <|-- PlaywrightDriver : Implements
    AbstractDriver <|-- MobileDriver : Implements
```

### 2. Self-Healing Sequence Diagram

How the `Healer` intervenes when an element is missing.

```mermaid
sequenceDiagram
    participant Test as Test Script
    participant Driver as SeleniumDriver
    participant DOM as Browser DOM
    participant Healer as Healer Module

    Test->>Driver: find_element("#submit")
    Driver->>DOM: querySelector("#submit")
    DOM-->>Driver: NoSuchElementException

    rect rgb(255, 240, 240)
        Note right of Driver: Heuristic Healing Activated
        Driver->>Healer: heal("#submit", page_source)
        Healer->>Healer: Parse Attributes (ID, Name)
        Healer->>DOM: Scan for candidates
        Healer->>Healer: Calculate Levenshtein Score
        Healer-->>Driver: Returns "#submit_v2" (Score: 0.95)
    end

    Driver->>DOM: querySelector("#submit_v2")
    DOM-->>Driver: WebElement
    Driver-->>Test: WebElement
```

### 3. API Client Flow

How the wrapper handles logging and error checks.

```mermaid
sequenceDiagram
    participant Test as Test Script
    participant Client as APIClient
    participant Requests as Requests Lib
    participant Logger as StructLog

    Test->>Client: get("/users/1")
    Client->>Logger: Log Request (URL, Headers)
    Client->>Requests: request("GET", "/users/1")
    Requests-->>Client: Response (200 OK)
    Client->>Client: _validate_status(200)
    Client->>Logger: Log Response (Status, Duration)
    Client-->>Test: JSON Data
```

## Component Breakdown

### 1. Core Library (`qa_framework`)

The standard distribution package installed via pip. It acts as the backbone, providing shared utilities, configuration management, and base classes.

### 2. UI Automation Layer

- **Driver Factory**: A centralized point that reads the configuration and instantiates the correct driver.
- **Abstract Driver**: A Python Protocol/Interface that defines standard actions to ensure test code remains agnostic.
- **Page Object Model (POM)**: The `BasePage` class encapsulates common page interactions.

### 3. API Automation Layer

- **API Client**: Wrapper around `requests` handling session management, logging, and error verification.
- **GraphQL Client**: Extends API Client for query/mutation structures.

### 4. Data Layer

- **DB Manager**: SQLAlchemy-based manager dealing with connections and session scoping.
- **File Readers**: Utilities to parse JSON, YAML, CSV, and XLSX files.

## Execution Flow

The following describes the lifecycle of a typical test run:

1.  **Initialization Phase**
    - The test runner (Pytest) starts.
    - `conftest.py` loads the **Settings** from `.env`.
    - **Logger** is configured.
2.  **Setup Phase**
    - **Driver Factory** initializes the browser.
    - **DB Manager** creates a connection pool.
    - Test Data is loaded using **File Readers**.
3.  **Execution Phase**
    - Test Function calls a **Page Object**.
    - The **Page Object** delegates to the **Abstract Driver**.
    - The **Driver** executes on the browser.
4.  **Reporting Phase**
    - All actions are logged via `structlog`.
    - `AllureListener` attaches screenshots on failure.
5.  **Teardown Phase**
    - Browser session is closed.
    - Temporary files are cleaned up.
