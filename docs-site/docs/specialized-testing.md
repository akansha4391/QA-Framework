---
sidebar_position: 6
---

# Specialized Testing

To ensure Enterprise-grade quality, the framework goes beyond functional testing with specialized layers.

## 1. Accessibility (A11y) Testing ♿

We use **Axe-core** to automatically detect WCAG 2.1 violations.

### Configuration

Ensure `axe-core-python` (Selenium) or `axe-playwright-python` (Playwright) is installed.

### Usage

```python
from qa_framework.core.a11y.manager import AccessibilityManager

def test_a11y(self):
    self.driver.goto("https://example.com")
    report = AccessibilityManager(self.driver).scan()
    assert len(report['violations']) == 0
```

## 2. Visual Regression Testing 🎨

We use **Snapshot Testing** to catch visual bugs (CSS breaks, layout shifts).

### Configuration

Ensure `Pillow` is installed.

### Usage

```python
from qa_framework.core.visual.manager import VisualManager

def test_visual(self):
    visual = VisualManager(self.driver)
    # 1st Run: Creates baseline in tests/visual/baselines
    # 2nd Run: Compares against baseline
    assert visual.compare("homepage_snapshot")
```

- **Baselines**: Stored in `tests/visual/baselines`. Commit these to Git.
- **Failures**: Differences saved in `tests/visual/failures`.

## 3. Security Testing (DAST) 🔒

We integrate with **OWASP ZAP** to proxy traffic and scan for vulnerabilities.

### Configuration

1.  Run ZAP (e.g., Docker).
2.  Update `.env`:
    ```bash
    USE_ZAP_PROXY=true
    ZAP_BASE_URL=http://localhost:8080
    ```

### Usage

```python
from qa_framework.core.security.zap_manager import ZapManager

def test_security_scan():
    zap = ZapManager()
    # Crawl
    zap.spider("https://target.com")
    # Check Alerts
    alerts = zap.get_alerts("https://target.com", risk_level='High')
    assert len(alerts) == 0
```

## 4. Self-Healing Automation 🩹

The framework uses heuristics to recover from `NoSuchElementException`.

### Configuration

```bash
# .env
ENABLE_SELF_HEALING=true
```

### How it works

1.  If a selector (e.g., `#submit-btn`) fails.
2.  The **Healer** parses the current DOM.
3.  It looks for elements with similar attributes (Levenshtein distance).
4.  If a match is found (>80% confidence), it clicks the new element and logs a **WARNING**.
