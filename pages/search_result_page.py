from playwright.sync_api import expect

from pages.base_page import BasePage


class SearchResultPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.search_result_header = page.locator('.a-size-base.a-spacing-small.a-spacing-top-small.a-text-normal')
        self.search_product_name = self.search_result_header.locator('.a-color-state.a-text-bold')
        self.list_of_searched_items = page.locator('.s-main-slot.s-result-list.s-search-results.sg-row')
        # self.add_to_cart_button = page.get_by_role('button', name='Add to cart')

        self.items = page.locator('div[data-component-type="s-search-result"][data-asin]:not([data-asin=""])')



    def validate_searched_product_name(self, search_product_name: str):
        expect(self.search_product_name).to_contain_text(search_product_name)



    def add_product_first_product_from_list_to_cart(self):
        self.wait_for_page_loaded()

        first_item = self.items.nth(0)
        expect(first_item).to_be_visible()

        add_to_cart_button = first_item.get_by_role('button', name='Add to cart')

        add_to_cart_button.click()

        # counter: int = 0
        #
        # if self.items.nth(counter):
        #     add_to_cart_button.click()
        # else:
        #     while not self.items.nth(counter):
        #         counter += 1
        #     add_to_cart_button.click()






