---
sidebar_position: 2
---

# Installation

## Prerequisites

- Python 3.10 or higher
- pip (Python Package Installer)

## Installation Steps

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/your-org/qa-framework.git
    cd qa-framework
    ```

2.  **Create a Virtual Environment**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the Framework**

    ```bash
    pip install -e .
    ```

4.  **Install Playwright Browsers** (if using Playwright)
    ```bash
    playwright install
    ```

## Verification

Run the demo script to verify the installation:

```bash
python examples/demo.py
```
