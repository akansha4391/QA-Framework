---
sidebar_position: 4
---

# Sample Projects

The framework includes sample projects demonstrating 5 different testing flavors using **SauceDemo.com**.

## 1. Standard Pytest (POM)

The default enterprise standard. Uses Page Object Model and Pytest.

- **Location**: \`examples/poc_saucedemo\`
- **Key Features**: strict POM, Data-Driven, Hybrid Driver.
- **Run Command**:
  \`\`\`bash
  pytest examples/poc_saucedemo/tests
  \`\`\`

## 2. Behavior Driven Development (BDD)

Uses **Cucumber/Gherkin** syntax for collaboration with Product Owners.

- **Location**: \`examples/saucedemo_bdd\`
- **Key Features**: \`.feature\` files, Step Definitions.
- **Run Command**:
  \`\`\`bash
  pytest examples/saucedemo_bdd/tests
  \`\`\`

## 3. Robot Framework

Uses Keyword Driven Testing for low-code automation.

- **Location**: \`examples/saucedemo_robot\`
- **Key Features**: \`.robot\` files, Custom Python Library.
- **Run Command**:
  \`\`\`bash
  # Ensure pythonpath includes the root
  export PYTHONPATH=$PYTHONPATH:.
  robot examples/saucedemo_robot/tests/login.robot
  \`\`\`

## 4. Test Driven Development (TDD)

Focuses on writing tests before implementation.
_Note: In the context of this framework, TDD uses the same structure as the Standard Pytest example._

- **Location**: \`examples/poc_saucedemo\` (Same as Standard)
- **Workflow**:
  1. Write a failing test in \`tests/ui/new_feature.py\`.
  2. Run it (Red).
  3. Implement Page Object methods (Green).
  4. Refactor.

## 5. With Playwright (Direct)

The framework defaults to Playwright. Use the Standard POM example but explicitly configure the browser engine.

- **Location**: \`examples/poc_saucedemo\`
- **Configuration**:
  - Set \`USE_PLAYWRIGHT=true\` in \`.env\`.
  - Set \`BROWSER=chromium\`.
- **Run Command**:
  \`\`\`bash
  BROWSER=firefox pytest examples/poc_saucedemo/tests
  \`\`\`
