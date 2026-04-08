from playwright.sync_api import expect

from pages.base_page import BasePage


class HeaderComponents(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.main_page_button = page.locator("a#nav-logo-sprites")
        self.search_box = page.get_by_role('searchbox', name='Search Amazon')
        self.language_selector = page.locator('.nav-div#icp-nav-flyout')
        self.account_and_lists_link = page.get_by_role('button', name='Account & Lists')

        self.card_link = page.locator('#nav-cart-count-container')
        self.cart_count_locator = self.card_link.locator('#nav-cart-count')

        self.hamburger_menu = page.get_by_role('button', name='All')



    def get_number_of_items_in_cart(self):
        # expect(self.cart_count_locator).to_be_visible()
        self.page.reload()
        expect(self.cart_count_locator).to_be_visible()
        return int(self.cart_count_locator.inner_text()) if self.cart_count_locator.is_visible() else 0

    def go_to_home_page(self):
        expect(self.main_page_button).to_be_visible()
        self.main_page_button.click()

    def open_cart_page(self):
        expect(self.card_link).to_be_visible()
        self.card_link.click()


