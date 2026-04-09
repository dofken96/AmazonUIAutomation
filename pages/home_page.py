from playwright.sync_api import expect

from components.header_components import HeaderComponents
from config import BASE_URL
from pages.base_page import BasePage
from playwright.sync_api import Error as PlaywrightError


class HomePage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponents(page)




    def open(self):
        self.safe_goto(
            url=BASE_URL,
            ready_locator=self.header.search_box,
            retries=3,
            timeout=15000,
        )


    def verify_main_attributes_visible(self):
        expect(self.header.search_box).to_be_visible()
        expect(self.header.cart_link).to_be_visible()
        expect(self.header.hamburger_menu).to_be_visible()


    def search_a_product(self, product_name):
        self.header.search_box.fill(product_name)
        self.header.search_box.press("Enter")

    def validate_url(self, url: str):
        expect(self.page).to_have_url(url)


    def dismiss_toaster(self):
        """Remove the location/delivery toaster that can intercept clicks."""
        self.page.evaluate("document.querySelector('.glow-toaster')?.remove()")
        