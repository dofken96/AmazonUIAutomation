import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class SignInPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.primary_email_input = page.locator("#ap_email")
        self.fallback_email_input = page.locator("input[name='email']")

    def verify_sign_in_page_loaded(self):
        expect(self.page).to_have_url(re.compile(r".*(ap/signin|signin).*", re.I), timeout=15000)
        if self.primary_email_input.count() > 0:
            expect(self.primary_email_input).to_be_visible(timeout=15000)
        else:
            expect(self.fallback_email_input).to_be_visible(timeout=15000)
