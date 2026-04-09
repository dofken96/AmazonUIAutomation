import re
from playwright.sync_api import expect

from components.header_components import HeaderComponents
from pages.base_page import BasePage


class SearchResultPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponents(page)

        self.search_result_header = page.locator('.a-size-base.a-spacing-small.a-spacing-top-small.a-text-normal')
        self.search_product_name = self.search_result_header.locator('.a-color-state.a-text-bold')
        self.list_of_searched_items = page.locator('.s-main-slot.s-result-list.s-search-results.sg-row')
        self.sort_combobox = page.get_by_role("combobox", name=re.compile(r"sort by", re.I))
        self.sort_prompt = page.locator("span.a-dropdown-prompt")
        self.next_page_link = page.locator("a.s-pagination-next, a[aria-label*='Go to next page']")
        self.pagination_container = page.locator(".s-pagination-container")

        # self.items = page.locator('div[data-component-type="s-search-result"][data-asin]:not([data-asin=""])')
        self.items = page.locator('div[role="listitem"]')



    def validate_searched_product_name(self, search_product_name: str):
        expect(self.search_product_name).to_contain_text(search_product_name)


    def add_first_product_from_list_to_cart(self):
        self.wait_for_page_loaded()

        first_item = self.items.nth(0)
        expect(first_item).to_be_visible()

        add_to_cart_button = first_item.get_by_role('button', name='Add to cart')

        add_to_cart_button.click()

        stepper_controls = first_item.locator('.a-stepper-controls')
        expect(stepper_controls).to_be_visible()




    def click_on_first_product(self):
        self.wait_for_page_loaded()

        first_item = self.items.nth(0)
        expect(first_item).to_be_visible()
        header = first_item.locator("a h2")
        header.click()

    def add_several_products_to_cart(self, number_of_products: int):
        expect(self.items.last).to_be_visible()

        for i in range(number_of_products):

            self.page.reload()
            expect(self.header.cart_count_locator).to_be_visible()
            before_number = self.header.get_number_of_items_in_cart()

            item = self.items.nth(i)
            expect(item).to_be_visible()
            item.scroll_into_view_if_needed()
            add_to_cart_button = item.get_by_role('button', name='Add to cart')
            add_to_cart_button.click()

            expect(self.header.cart_count_locator).to_have_text(str(before_number + 1))

            after = self.header.get_number_of_items_in_cart()

            assert after == before_number + 1

    def verify_sort_control_visible(self):
        self.wait_for_page_loaded()

        if self.sort_combobox.count() > 0:
            expect(self.sort_combobox).to_be_visible()
            return

        expect(self.sort_prompt).to_be_visible()

    def verify_pagination_next_control_visible(self):
        self.wait_for_page_loaded()
        self.page.mouse.wheel(0, 12000)

        if self.next_page_link.count() > 0:
            expect(self.next_page_link).to_be_visible(timeout=15000)
            return

        expect(self.pagination_container).to_be_visible(timeout=15000)









