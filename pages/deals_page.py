

from playwright.sync_api import expect
from components.header_components import HeaderComponents
from pages.base_page import BasePage


class DealsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponents(page)
# 
        self.deals_container = page.locator('.discounts-react-app')


    def verify_deals_page_loaded(self):
        expect(self.deals_container).to_be_visible()