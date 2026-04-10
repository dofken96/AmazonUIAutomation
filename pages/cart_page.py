from playwright.sync_api import expect

from components.header_components import HeaderComponents
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponents(page)

        self.proceed_to_checkout_button = page.get_by_role('button', name='Proceed to checkout')
        self.list_active_cart_items = page.locator('ul[data-name="Active Items"] [data-asin][role="listitem"]')

    def proceed_to_checkout(self):
        expect(self.proceed_to_checkout_button).to_be_visible()
        self.proceed_to_checkout_button.click()


    def get_cart_items(self) -> list:
        self.page.reload()
        expect(self.list_active_cart_items.last).to_be_visible()
        active_items = []
        items_count = self.list_active_cart_items.count()
        for i in range(items_count):
            active_items.append(self.list_active_cart_items.nth(i))

        return active_items


    def remove_products_from_cart(self):
        self.page.wait_for_load_state("domcontentloaded")
        delete_buttons = self.page.locator("input[value='Delete']")
        max_attempts = 30
        attempts = 0

        while delete_buttons.count() > 0 and attempts < max_attempts:
            delete_buttons.first.click()
            self.page.wait_for_timeout(1500)
            attempts += 1

        self.page.reload()

