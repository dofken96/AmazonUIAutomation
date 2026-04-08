from itertools import count
from tkinter import image_names

from playwright.sync_api import expect

from components.header_components import HeaderComponents
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponents(page)

        self.proceed_to_checkout_button = page.get_by_role('button', name='Proceed to checkout')
        # self.list_active_cart_items = page.locator('ul[data-name="Active Items"] [data-asin]')
        self.list_active_cart_items = page.locator('ul[data-name="Active Items"] [data-asin][role="listitem"]')




    def proceed_to_checkout(self):
        expect(self.proceed_to_checkout_button).to_be_visible()
        self.proceed_to_checkout_button.click()


    def get_cart_items(self) -> list:
        self.page.reload()
        expect(self.list_active_cart_items.last).to_be_visible()

        active_items = []
        items_count = self.list_active_cart_items.count()

        # print(f'\nFrom get_cart_items method: {items_count} items found in cart\n')

        for i in range(items_count):
            # print(self.list_active_cart_items.locator('.sc-item-product-title-cont').nth(i).inner_text().strip())
            # print("-----------------------------\n")
            active_items.append(self.list_active_cart_items.nth(i))

        return active_items






    def remove_products_from_cart(self):
        expect(self.list_active_cart_items.last).to_be_visible()
        expect(self.header.cart_count_locator).to_be_visible()

        while self.list_active_cart_items.count() > 0:

            item = self.list_active_cart_items.first

            expect(item).to_be_visible()

            before_count = int(self.header.cart_count_locator
                               .inner_text()
                               .strip())

            container_with_items = item.locator('.a-stepper-inner-container [data-a-selector="value"]')
            items_for_particular_product = int(container_with_items
                                               .inner_text()
                                               .strip())


            delete_button = item.locator('input[value="Delete"]')

            expect(item).to_be_visible()
            expect(delete_button).to_be_visible()
            delete_button.click()
            expect(container_with_items).to_be_hidden()


            expect(self.header.cart_count_locator).to_have_text(str(before_count - items_for_particular_product))
            self.page.reload()

