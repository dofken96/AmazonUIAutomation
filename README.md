# Amazon UI Automation

Python + Playwright + Pytest test automation framework for Amazon UI validation.

## Overview

This repository contains an end-to-end smoke suite for key Amazon user journeys:

- Header and homepage visibility checks.
- Search and search results validation.
- Product detail page (PDP) navigation and gallery checks.
- Add-to-cart and checkout flow.
- Deals, footer, language/region, and account entry points.
- Customer Service and Gift Cards navigation.
- Basic mobile viewport validation.
- Console-error smoke validation.

Smoke tracking and case-level status live in `data/smoke_test_cases.md`.

## Architecture

The framework uses layered test design:

1. **Page Objects** (`pages/`, `components/`)
   - Encapsulate selectors, actions, and assertions.
2. **Factory** (`factories/page_factory.py`)
   - Provides cached page-object instances per test page context.
3. **Facades** (`facedes/`)
   - Orchestrate multi-step flows and reduce duplication in tests.
4. **Tests** (`tests/smoke/test_smoke.py`)
   - Thin scenario definitions that call facades.

This structure keeps tests readable and centralizes maintenance when UI behavior changes.

## Project Structure

```text
AmazonUI/
  components/              # Shared UI components (header/footer)
  data/                    # Smoke matrix and tracking files
  facedes/                 # Flow facades (home/search/cart/checkout)
  factories/               # Page object factory
  fixtures/                # Pytest fixtures and browser/context setup
  pages/                   # Page Objects
  scripts/                 # Auth/session helper scripts
  tests/
    smoke/                 # Main smoke suite
  utils/                   # Support utilities
  config.py                # Env-based configuration
  conftest.py              # Global pytest plugin registration
  pytest.ini               # Pytest configuration
```

## Prerequisites

- Python 3.13 (current project runtime).
- Virtual environment (`.venv`).
- Playwright browsers installed (Chromium used here).
- Valid test credentials for checkout/sign-in flows.

## Environment Configuration

Create `.env` in project root:

```env
BASE_URL=https://www.amazon.com/
LOGIN_EMAIL=your_test_email
LOGIN_PASSWORD=your_test_password
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
```

If `requirements.txt` is missing in your branch, install manually:

```powershell
pip install playwright pytest pytest-playwright python-dotenv
```

## Run Tests

Run smoke suite:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\smoke\test_smoke.py -q
```

Run full project tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Collect-only sanity check:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\smoke\test_smoke.py --collect-only -q
```

## Current Status

- Smoke suite currently collects **19 tests**.
- Checkout smoke (`test_proceed_to_checkout`) is active (not xfail) and includes sign-in redirect handling.
- Current validated baseline: full smoke run passes.

## Notes on Stability

- Amazon UI is dynamic by locale, account state, experiments, and anti-bot behavior.
- Tests use resilient locators and flow-level retries where needed.
- Auth-dependent flows rely on `scripts/.auth` state + `.env` credentials.
