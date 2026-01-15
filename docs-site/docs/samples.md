---
sidebar_position: 4
---

# Sample Projects & Flavors

The QA Framework is designed to be **Methodology Agnostic**. It supports various testing styles out-of-the-box. We provide reference implementations for **SauceDemo** in 5 different flavors.

## 1. Standard Pytest (POM) 🏗️

This is the **Recommended Enterprise Standard**. It balances code reusability (Page Object Model) with developer velocity (Pytest).

- **Target Audience**: SDETs, Python Developers.
- **Path**: \`examples/poc_saucedemo\`
- **Key Concepts**:
  - **Page Object Model (POM)**: UI selectors and actions are encapsulated in \`pages/\`.
  - **Fixtures**: Setup/Teardown is handled in \`conftest.py\`.
- **How it works**: Tests just call high-level methods like \`login_page.login()\`. Assertions are standard Python \`assert\`.

## 2. Behavior Driven Development (BDD) 🥒

This flavor uses **Gherkin** syntax (\`Given/When/Then\`) to create "Executable Specifications". It bridges the gap between Product Owners and QA.

- **Target Audience**: Agile Teams, Product Owners, Business Analysts.
- **Path**: \`examples/saucedemo_bdd\`
- **Structure**:
  - \`tests/features/grade.feature\`: The requirements file (Plain English).
  - \`tests/step_defs/test_grade_steps.py\`: The Python "glue code" that executes the steps.
- **Benefits**: Living documentation. If the spec changes, the test fails.

## 3. Robot Framework 🤖

A **Keyword-Driven** approach. It allows creating high-level keywords like \`Login To App\` that abstraction complex logic.

- **Target Audience**: Enterprise QA Teams, Manual Testers transitioning to Automation.
- **Path**: \`examples/saucedemo_robot\`
- **Structure**:
  - \`tests/login.robot\`: Test cases written in Robot's tabular format.
  - \`keywords/SauceKeywords.py\`: Python library backing the keywords.
- **Benefits**: Very readable logs/reports. Low-code entry barrier for writing tests.

## 4. Test Driven Development (TDD) 🔴🟢

TDD is a **Process**, not a specific tool. However, our Standard Pytest flavor is optimized for it.

- **Workflow**:
  1.  **Red**: Write a test for a feature that doesn't exist yet (e.g., \`test_checkout_complete\`). Run it -> Fails.
  2.  **Green**: Implement the minimal code in the Page Object to make the test pass.
  3.  **Refactor**: Clean up the code.
- **Why use it?**: Ensures high test coverage and cleaner, testable design.

## 5. Playwright Flavor 🎭

The framework supports multiple drivers. By default, it might use Selenium, but switching to Playwright is a simple configuration change.

- **Configuration**:
  Set \`USE_PLAYWRIGHT=true\` in your \`.env\` file.
- **Benefits**:
  - Faster execution.
  - Auto-waiting (less flaky tests).
  - Powerful tracing and debugging.
- **Note**: All the above flavors (Standard, BDD, Robot) can _also_ run on Playwright. It is orthogonal to the methodology.
