from playwright.sync_api import expect, Page

from pages.base_page import BasePage


class HeaderComponents(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.main_page_button = page.locator("a#nav-logo-sprites")
        self.search_box = page.get_by_role('searchbox', name='Search Amazon')
        self.language_selector = page.locator('.nav-div#icp-nav-flyout')
        self.account_and_lists_link = page.get_by_role('button', name='Account & Lists')

        self.cart_link = page.locator('#nav-cart-count-container')
        self.cart_count_locator = self.cart_link.locator('#nav-cart-count')

        self.hamburger_menu = page.get_by_role('button', name='All')
        self.deals_link = page.get_by_role('link', name="Today's Deals")

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


