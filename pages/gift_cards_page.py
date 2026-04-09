import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class GiftCardsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.main_heading = page.locator("h1")
        self.content_container = page.locator("#gw-desktop-herotator, #gcx-gf-section")
        self.gift_cards_text = page.get_by_text(re.compile(r"Gift Cards", re.I))

    def verify_gift_cards_page_loaded(self):
        expect(self.page).to_have_url(re.compile(r".*(gift|gift-cards).*", re.I), timeout=20000)
        if self.main_heading.count() > 0:
            expect(self.main_heading).to_be_visible(timeout=20000)
        elif self.gift_cards_text.count() > 0:
            expect(self.gift_cards_text.nth(0)).to_be_visible(timeout=20000)
        else:
            expect(self.content_container.nth(0)).to_be_visible(timeout=20000)
