import re

from playwright.sync_api import expect, Page

from pages.base_page import BasePage


class HeaderComponents(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.main_page_button = page.locator("a#nav-logo-sprites")
        self.search_box = page.get_by_role('searchbox', name='Search Amazon')
        self.language_selector = page.locator('.nav-div#icp-nav-flyout')
        self.language_flyout = page.locator('#nav-flyout-icp')
        self.account_and_lists_link = page.get_by_role('button', name='Account & Lists')
        self.account_and_lists_nav = page.locator("#nav-link-accountList")

        self.cart_link = page.locator('#nav-cart-count-container')
        self.cart_count_locator = self.cart_link.locator('#nav-cart-count')

        self.hamburger_menu = page.get_by_role('button', name='All')
        self.deals_link = page.get_by_role('link', name="Today's Deals")
        self.customer_service_link = page.get_by_role("link", name=re.compile(r"Customer Service", re.I))
        self.gift_cards_link = page.get_by_role("link", name=re.compile(r"Gift Cards", re.I))

        self.side_nav = page.get_by_role('dialog').locator('#hmenu-content')
        self.dept_section = self.side_nav.locator('section.category-section', has_text='Shop by Department')



    def get_number_of_items_in_cart(self):
        self.page.reload()
        expect(self.cart_count_locator).to_be_visible()
        return int(self.cart_count_locator.inner_text()) if self.cart_count_locator.is_visible() else 0

    def go_to_home_page(self):
        expect(self.main_page_button).to_be_visible()
        self.main_page_button.click()

    def open_cart_page(self):
        expect(self.cart_link).to_be_visible()
        self.cart_link.click()

    def go_to_deals_page(self):
        expect(self.deals_link).to_be_visible()
        self.deals_link.click()
        self.page.wait_for_load_state('domcontentloaded')


    def navigate_to_hamburger_menu(self):
        expect(self.hamburger_menu).to_be_visible()
        self.hamburger_menu.click()

    def verify_departments_list(self):
        expect(self.side_nav).to_be_visible()
        expect(self.dept_section).to_be_visible()
        dept_links = self.dept_section.locator('a.hmenu-item')
        assert dept_links.count() >= 3, f"Expected at least 3 department links, got {dept_links.count()}"

    def open_language_region_selector(self):
        expect(self.language_selector).to_be_visible()
        self.language_selector.click()
        self.page.wait_for_load_state('domcontentloaded')

    def verify_language_region_selector_opened(self):
        if re.search(r'customer-preferences', self.page.url):
            expect(self.page).to_have_url(re.compile(r'.*customer-preferences.*', re.I))
            return

        expect(self.language_flyout).to_be_visible(timeout=15000)
        expect(
            self.language_flyout.locator('a, .icp-radio, [role="radio"]').first
        ).to_be_visible()

    def open_search_suggestions(self, partial_query: str):
        expect(self.search_box).to_be_visible()
        self.search_box.click()
        self.search_box.fill(partial_query)

    def verify_search_suggestions_visible(self, partial_query: str):
        suggestions_container = self.page.locator("#nav-flyout-searchAjax")
        first_suggestion = suggestions_container.get_by_text(
            re.compile(re.escape(partial_query), re.I)
        ).first

        expect(suggestions_container).to_be_visible(timeout=10000)
        expect(first_suggestion).to_be_visible(timeout=10000)

    def open_sign_in_page_via_account_lists(self):
        expect(self.account_and_lists_nav).to_be_visible(timeout=15000)
        self.account_and_lists_nav.click()
        self.page.wait_for_load_state('domcontentloaded')

    def open_customer_service_page(self):
        self._open_top_nav_link(self.customer_service_link, re.compile(r"Customer Service", re.I))

    def open_gift_cards_page(self):
        self._open_top_nav_link(self.gift_cards_link, re.compile(r"Gift Cards", re.I))

    def _open_top_nav_link(self, link_locator, menu_link_name):
        if link_locator.count() > 0 and link_locator.is_visible():
            link_locator.click()
        else:
            self.navigate_to_hamburger_menu()
            menu_link = self.side_nav.get_by_role("link", name=menu_link_name)
            expect(menu_link).to_be_visible(timeout=10000)
            menu_link.click()

        self.page.wait_for_load_state('domcontentloaded')


