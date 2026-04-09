import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class CustomerServicePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.primary_heading = page.locator("h1")
        self.secondary_heading = page.locator("h2")

    def verify_customer_service_page_loaded(self):
        expect(self.page).to_have_url(re.compile(r".*(help|customer).*", re.I), timeout=20000)
        if self.primary_heading.count() > 0:
            expect(self.primary_heading).to_be_visible(timeout=20000)
        else:
            expect(self.secondary_heading).to_be_visible(timeout=20000)
