from playwright.sync_api import expect

from config import LOGIN_EMAIL, LOGIN_PASSWORD


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
        self.complete_sign_in_if_redirected()

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

    def complete_sign_in_if_redirected(self):
        self.page.wait_for_load_state("domcontentloaded")

        is_sign_in_url = "ap/signin" in self.page.url
        email_input = self.page.locator("#ap_email")
        password_input = self.page.locator("#ap_password")

        if not is_sign_in_url and not email_input.count() and not password_input.count():
            return

        if email_input.count() and email_input.is_visible():
            if not LOGIN_EMAIL:
                raise AssertionError("LOGIN_EMAIL is required to continue checkout sign-in flow.")
            email_input.fill(LOGIN_EMAIL)
            continue_button = self.page.locator("#continue")
            expect(continue_button).to_be_visible(timeout=10000)
            continue_button.click()
            self.page.wait_for_load_state("domcontentloaded")

        if password_input.count() and password_input.is_visible():
            if not LOGIN_PASSWORD:
                raise AssertionError("LOGIN_PASSWORD is required to continue checkout sign-in flow.")
            password_input.fill(LOGIN_PASSWORD)
            sign_in_button = self.page.locator("#signInSubmit")
            expect(sign_in_button).to_be_visible(timeout=10000)
            sign_in_button.click()
            self.page.wait_for_load_state("domcontentloaded")



