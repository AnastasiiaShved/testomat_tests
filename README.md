# Testomat.io UI Test Suite

Automated end-to-end UI test suite for [testomat.io](https://testomat.io), built with **Pytest** and **Playwright**.
Covers authentication, project management, and navigation workflows using the Page Object Model pattern.

---

## Tech Stack

| Tool              | Version | Purpose                       |
|-------------------|---------|-------------------------------|
| Python            | 3.13+   | Language                      |
| pytest            | 8.4.1   | Test runner                   |
| playwright        | 1.58.0  | Browser automation            |
| pytest-playwright | 0.7.2   | Playwright–pytest integration |
| pytest-html       | 4.2.0   | HTML report generation        |
| python-dotenv     | 1.2.2   | Environment variable loading  |
| faker             | 40.11.0 | Test data generation          |
| uv                | latest  | Dependency management         |

---

## Project Structure

```
testomat_tests/
├── src/
│   └── web/
│       ├── application.py          # Central Application class (aggregates all pages)
│       ├── pages/
│       │   ├── login_page.py
│       │   ├── home_page.py
│       │   ├── projects_page.py
│       │   ├── project_page.py
│       │   └── new_projects.py
│       └── components/
│           ├── project_card.py
│           ├── project_page_header.py
│           └── side_bar.py
├── tests/
│   ├── conftest.py                 # Fixtures and browser lifecycle
│   ├── first_test.py
│   └── web/
│       ├── login_page_tests.py     # Login validation (parametrized, ~26 cases)
│       ├── projects_page_tests.py  # Projects listing and search
│       ├── project_creation_test.py
│       └── regression_tests.py     # Full regression suite
├── test_result/
│   ├── report.html                 # Generated HTML report
│   └── traces/                     # Playwright trace files
├── videos/                         # Video recordings (generated on run)
├── pyproject.toml                  # Project config, dependencies, pytest settings
└── .env                            # Credentials and URLs (not committed)
```

---

## Setup

### 1. Install uv

```bash
pip install uv
```

### 2. Create virtual environment and install dependencies

```bash
uv venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate      # Windows

uv pip install -e .
```

### 3. Install Playwright browsers

```bash
playwright install chromium
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```dotenv
BASE_URL=https://testomat.io
BASE_APP_URL=https://app.testomat.io
BASE_DOMEN=testomat.io
EMAIL=your_test_email@example.com
PASSWORD=your_test_password
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run smoke tests only
pytest -m smoke

# Run regression tests only
pytest -m regression

# Run a specific test file
pytest tests/web/login_page_tests.py

# Run with visible browser (already the default)
pytest
```

### Test output

| Artifact                 | Location                  |
|--------------------------|---------------------------|
| HTML report              | `test_result/report.html` |
| Playwright traces        | `test_result/traces/`     |
| Video recordings         | `videos/`                 |
| Screenshots (on failure) | `test_result/`            |

---

## Test Markers

| Marker       | Description                                |
|--------------|--------------------------------------------|
| `smoke`      | Quick sanity checks for core functionality |
| `regression` | Full regression test suite                 |
| `web`        | UI tests using Playwright                  |
| `slow`       | Tests with longer execution time           |

---

## Architecture

The project follows the **Page Object Model (POM)** pattern:

- **`Application`** — central hub that aggregates all page objects; tests interact with it instead of raw Playwright
  APIs
- **Pages** — one class per page (e.g., `LoginPage`, `ProjectsPage`), encapsulating locators and actions
- **Components** — reusable UI elements shared across pages (e.g., `SideBar`, `ProjectCard`)
- **Fixtures** (`conftest.py`) — manage browser lifecycle at session/function scope:
    - `config` — test credentials and URLs
    - `shared_app` — fresh page state per test, unauthenticated
    - `logged_app` — pre-authenticated Application instance (session-scoped context, function-scoped page)

### Browser configuration (defaults)

| Setting         | Value               |
|-----------------|---------------------|
| Browser         | Chromium            |
| Headless        | No (visible)        |
| Slow motion     | 700 ms              |
| Viewport        | 1320 × 980          |
| Locale          | uk-UA               |
| Timezone        | Europe/Kyiv         |
| Video recording | Enabled (all tests) |

---

## Test Coverage

| Area             | Description                                                             |
|------------------|-------------------------------------------------------------------------|
| Login            | Invalid credentials, email/password boundary values, SQL injection, XSS |
| Projects page    | Search, filtering, project count, badge validation                      |
| Project creation | New project flow, empty state, sidebar navigation                       |
| Regression       | End-to-end user workflows across the full application                   |
