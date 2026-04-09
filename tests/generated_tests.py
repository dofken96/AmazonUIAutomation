import re

from playwright.sync_api import expect

from pages.home_page import HomePage


def _dismiss_toaster(page):
    """Remove the location/delivery toaster that can intercept clicks."""
    page.evaluate("document.querySelector('.glow-toaster')?.remove()")


def test_navigate_today_deals_top(page):
    """AMZ-0007: Navigate to Today's Deals from top nav."""
    home_page = HomePage(page)
    home_page.open()
    _dismiss_toaster(page)

    deals_link = page.get_by_role('link', name="Today's Deals")
    expect(deals_link).to_be_visible()
    deals_link.click()

    page.wait_for_load_state('domcontentloaded')
    expect(page).to_have_url(re.compile(r'.*/goldbox.*'))

    deals_container = page.locator('.discounts-react-app')
    expect(deals_container).to_be_visible()


def test_hamburger_menu_departments_list(page):
    """AMZ-0008: Open hamburger menu and verify departments list."""
    home_page = HomePage(page)
    home_page.open()
    _dismiss_toaster(page)

    hamburger = home_page.header.hamburger_menu
    expect(hamburger).to_be_visible()
    hamburger.click()

    side_nav = page.get_by_role('dialog').locator('#hmenu-content')
    expect(side_nav).to_be_visible()

    dept_section = side_nav.locator('section.category-section', has_text='Shop by Department')
    expect(dept_section).to_be_visible()

    dept_links = dept_section.locator('a.hmenu-item')
    assert dept_links.count() >= 3, f"Expected at least 3 department links, got {dept_links.count()}"
