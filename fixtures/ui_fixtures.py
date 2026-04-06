import re

import pytest
from playwright.sync_api import sync_playwright, expect
from config import BASE_URL

@pytest.fixture(scope='session')
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope='session')
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope='session')
def localized_page(browser):
    page = browser.new_page()
    page.goto(BASE_URL)

    page.get_by_role('button', name='Deliver to Ukraine').click()

    country_select = page.locator("select#GLUXCountryList")
    expect(country_select).to_be_visible()
    country_select.select_option(label="Poland")

    page.get_by_role("button", name="Done").click()

    yield page

    page.close()
