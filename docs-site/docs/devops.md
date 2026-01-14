---
sidebar_position: 5
---

# DevOps & CI/CD

The framework is designed for seamless integration into modern DevOps pipelines.

## Containerization (Docker)

We provide a **Dockerfile** based on the official Playwright Python image. This ensures a consistent environment for test execution, eliminating "it works on my machine" issues.

### Running with Docker Compose

An out-of-the-box `docker-compose.yml` is included.

```bash
# Start the container in detached mode
docker compose up -d

# Execute tests inside the container
docker compose exec test-runner pytest

# Spin down
docker compose down
```

## CI/CD Pipeline (GitHub Actions)

A template workflow is available in `.github/workflows/ci.yml`.

### Triggers

- **Push** to `main` or `develop`
- **Pull Request**

### Stages

1.  **Checkout Code**
2.  **Setup Python 3.10**
3.  **Install Dependencies** (`pip install -e .[dev]`)
4.  **Linting** (`flake8`)
5.  **Unit Tests** (`pytest qa_framework/tests/unit`)
6.  **Upload Artifacts** (JUnit XML reports)
7.  **UI Tests** (Headless execution)

### Cloud Grid Integration

This framework supports **BrowserStack** and **SauceLabs** natively. To run tests on the cloud during CI, simply set the `REMOTE_GRID_URL` secret.

```yaml
# In GitHub Secrets
REMOTE_GRID_URL="https://user:key@hub-cloud.browserstack.com/wd/hub"
```
