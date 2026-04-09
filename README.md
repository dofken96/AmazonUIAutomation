# Amazon UI Automation

UI test automation framework for Amazon flows, built with Python, Playwright, and Pytest using a Page Object Model (POM) architecture.

## What This Project Covers

This repository automates core user journeys on Amazon, including:

- Homepage validation (critical header elements).
- Product search and search-result checks.
- Product detail page (PDP) navigation.
- Add-to-cart and cart cleanup scenarios.
- Checkout entry flow (currently marked as `xfail` due to known flakiness).
- Top navigation checks (Today's Deals, hamburger menu).
- Footer and language/region interaction checks.
- Basic mobile viewport smoke coverage.

The framework is designed to be extendable for larger regression suites while keeping smoke tests fast and readable.

## Tech Stack

- Python 3.13 (project currently runs in a local `.venv`).
- `playwright` for browser automation.
- `pytest` as the test runner.
- `pytest-playwright` for Playwright integration with pytest.
- `python-dotenv` for environment-based configuration.

## Project Structure

```text
AmazonUI/
  components/              # Reusable UI components (header, footer)
  data/                    # Test matrix and smoke case definitions
  fixtures/                # Pytest fixtures (browser/page/context setup)
  pages/                   # Page Objects (Home, Cart, PDP, Deals, etc.)
  scripts/                 # Helper scripts (auth state bootstrap)
  tests/
    smoke/                 # Main smoke suite
    generated_tests.py     # Generated/experimental tests
  utils/                   # Utility helpers
  config.py                # Env-driven runtime config
  conftest.py              # Global pytest plugin wiring
  pytest.ini               # Pytest config (currently minimal)
```

## Architecture and Conventions

- Page Object Model:
  - `pages/` holds page-level actions and assertions.
  - `components/` holds shared page fragments (for example header/footer).
- Fixtures:
  - `fixtures/ui_fixtures.py` creates browser contexts for desktop, mobile, localized, and authenticated sessions.
- Environment-based config:
  - `config.py` loads values from `.env`.
- Navigation robustness:
  - `BasePage.safe_goto()` retries flaky Amazon navigations for better stability.

## Prerequisites

- Windows, macOS, or Linux with Python 3.10+ (3.13 used in this project).
- Node.js available (recommended for Playwright tooling and MCP workflows).
- A valid internet connection to access target Amazon environment.

## Environment Variables

Create a `.env` file in the project root with:

```env
BASE_URL=https://www.amazon.com/
LOGIN_EMAIL=your_test_email
LOGIN_PASSWORD=your_test_password
```

Notes:

- Use non-production test credentials whenever possible.
- Auth-related flows rely on these values to create/reuse storage state in `scripts/.auth/`.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Install Playwright browser binaries.

Example (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install playwright pytest pytest-playwright python-dotenv
python -m playwright install chromium
```

## Running Tests

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Run smoke suite only:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\smoke\test_smoke.py -q
```

Collect-only (sanity check):

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

## Current Smoke Suite Status

- The smoke suite currently includes 11 collected tests in `tests/smoke/test_smoke.py`.
- Checkout flow test is intentionally marked with `@pytest.mark.xfail` due to known instability in checkout/cart/auth state transitions.
- Detailed planned smoke matrix is documented in `data/smoke_test_cases.md`.

## Using Playwright MCP Alongside This Project

Playwright MCP is useful for rapid selector discovery and flow exploration before codifying tests:

1. Explore/validate UI behavior with MCP in a live browser session.
2. Convert stable selectors into page objects under `pages/` or `components/`.
3. Add scenario coverage in `tests/smoke/` (or future `tests/regression/`).
4. Execute with pytest and stabilize flaky steps.

This approach keeps test code maintainable while speeding up authoring/debug cycles.

## Known Risks and Stability Notes

- Amazon UI can vary by locale, experiments, and anti-bot checks.
- Flakiness can appear around localization popovers, add-to-cart timing, and checkout redirects.
- Prefer role-based and resilient locators, and keep assertions focused on business-critical outcomes.

## Next Improvements (Suggested)

1. Add `requirements.txt` or `pyproject.toml` for reproducible dependency management.
2. Configure `pytest.ini` markers (`smoke`, `regression`, `auth`) and default options.
3. Add CI execution with artifact capture (screenshots, traces, videos).
4. Expand suite from smoke to regression using the test matrix in `data/`.
