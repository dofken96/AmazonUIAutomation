
import pytest
from playwright.sync_api import sync_playwright, expect, Page
from config import BASE_URL
from scripts.auth_setup import ensure_auth_state


@pytest.fixture(scope='session')
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()



@pytest.fixture(scope='function')
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()




def change_localization(page, country_label: str) -> Page:
    page.goto(BASE_URL)

    if not page.locator("a#nav-logo-sprites").is_visible():
        continue_shopping_button = page.get_by_role('button', name='Continue shopping')
        expect(continue_shopping_button).to_be_visible()
        continue_shopping_button.click()
    else:
        expect(page.locator("a#nav-logo-sprites")).to_be_visible()

    deliver_to_button = page.locator("#nav-global-location-popover-link")
    expect(deliver_to_button).to_be_visible()
    deliver_to_button.hover()
    deliver_to_button.click()

    country_select = page.locator(".a-native-dropdown#GLUXCountryList")
    expect(country_select).to_be_visible()

    country_select.select_option(label=country_label)
    page.get_by_role("button", name="Done").click()

    return page



@pytest.fixture(scope='function')
def localized_page(browser):
    context = browser.new_context()
    page = context.new_page()

    localized_page = change_localization(page, country_label='Canada')
    yield localized_page
    context.close()


@pytest.fixture(scope='session')
def auth_state(browser):
    return ensure_auth_state(browser)



@pytest.fixture(scope='session')
def auth_localized_page(browser, auth_state):

    context = browser.new_context(storage_state= auth_state)
    page = context.new_page()

    localized_auth_page = change_localization(page, country_label='Poland')

    yield localized_auth_page

    context.close()




