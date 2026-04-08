from playwright.sync_api import expect

from config import LOGIN_PASSWORD


class CheckoutPage:
    def __init__(self, page):
        self.page = page

        self.navigation_header = page.locator('#nav-belt')
        self.home_page_button = self.navigation_header.locator('#nav-logo')
        self.cart_page_button = self.navigation_header.locator('#nav-cart')

        self.add_delivery_address_button = page.get_by_role('link', name='Add a new delivery address')
        self.order_info = page.locator('#subtotals')
        self.order_total = self.order_info.locator('.order-summary-grid')




    def check_checkout_page_loaded(self):

        expect(self.home_page_button).to_be_visible()
        expect(self.cart_page_button).to_be_visible()
        expect(self.add_delivery_address_button).to_be_visible()

        # if not expect(self.page.get_by_role("textbox", name="Password")).to_be_visible():
        #     expect(self.home_page_button).to_be_visible()
        #     expect(self.cart_page_button).to_be_visible()
        #     expect(self.add_delivery_address_button).to_be_visible()
        # else:
        #     expect(self.page.get_by_role("textbox", name="Password")).to_be_visible()
        #     self.page.get_by_role("textbox", name="Password").fill(LOGIN_PASSWORD)
        #     self.page.get_by_role("button", name="Sign in").click()
        #     expect(self.home_page_button).to_be_visible()
        #     expect(self.cart_page_button).to_be_visible()
        #     expect(self.add_delivery_address_button).to_be_visible()


    def get_order_total_price(self) -> str:
        expect(self.order_info).to_be_visible()
        return self.order_total.locator('.order-summary-line-definition').inner_text().strip()



