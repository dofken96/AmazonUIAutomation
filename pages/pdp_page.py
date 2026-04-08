from playwright.sync_api import expect

from components.header_components import HeaderComponents
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponents(page)

        self.product_title = page.locator('#title')



    def get_product_title_name(self) -> str:
        expect(self.product_title).not_to_be_visible()
        return self.product_title.inner_text()




