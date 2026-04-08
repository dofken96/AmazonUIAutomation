import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, expect, Page, Browser

from config import BASE_URL, LOGIN_EMAIL, LOGIN_PASSWORD
AUTH_FILE = Path("AmazonUI/scripts/.auth/dou_user.json")


def login_amazon(page: Page):
    page.goto(BASE_URL)

    page.get_by_role("link", name="Hello, sign in Account & Lists").click()
    page.get_by_role("textbox", name="Enter mobile number or email").click()
    page.get_by_role("textbox", name="Enter mobile number or email").fill(LOGIN_EMAIL)
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill(LOGIN_PASSWORD)
    page.get_by_role("button", name="Sign in").click()

    expect(page.locator("#nav-link-accountList-nav-line-1")).not_to_have_text("Hello, sign in")


def create_auth_state(browser: Browser) -> None:
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    context = browser.new_context()
    page = context.new_page()
    login_amazon(page)
    context.storage_state(path=str(AUTH_FILE))
    context.close()



def auth_file_has_unexpired_cookie(path: Path, min_ttl_seconds: int = 300) -> bool:
    if not path.exists():
        return False

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False

    now = time.time()

    return any(
        cookie.get("expires", 0) > now + min_ttl_seconds
        for cookie in data.get("cookies", [])
    )


def saved_state_still_logs_in(browser: Browser) -> bool:

    if not AUTH_FILE.exists():
        return False

    context = browser.new_context(storage_state=str(AUTH_FILE))

    page = context.new_page()

    try:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        header_text = page.locator("#nav-link-accountList-nav-line-1").inner_text().strip()
        return header_text != "Hello, sign in"

    except Exception:
        return False

    finally:
        context.close()


def ensure_auth_state(browser: Browser) -> str:

    needs_refresh = (
        not auth_file_has_unexpired_cookie(AUTH_FILE)
        or not saved_state_still_logs_in(browser)
    )

    if needs_refresh:
        create_auth_state(browser)

    return str(AUTH_FILE)



