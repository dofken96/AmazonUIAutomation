from playwright.sync_api import expect

from components.header_components import HeaderComponents
from config import BASE_URL
from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponents(page)



    def open(self):
        self.page.goto(BASE_URL)
        self.wait_for_page_loaded()


    def verify_main_attributes_visible(self):
        expect(self.header.search_box).to_be_visible()
        expect(self.header.card_link).to_be_visible()
        expect(self.header.hamburger_menu).to_be_visible()


    def search_a_product(self, product_name):
        self.header.search_box.fill(product_name)
        self.header.search_box.press("Enter")

    def validate_url(self, url: str):
        expect(self.page).to_have_url(url)