


import re
from playwright.sync_api import expect
from pages.base_page import BasePage


class FooterComponents(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.footer = page.locator('#navFooter')
        self.conditions_link = self.footer.get_by_role('link', name='Conditions of Use')


    def verify_footer_visible(self):
        self.footer.scroll_into_view_if_needed()
        expect(self.footer).to_be_visible()

    
    def verify_policy_link_works(self):
        expect(self.conditions_link).to_be_visible()
        self.conditions_link.click()
        self.page.wait_for_load_state('domcontentloaded')
        expect(self.page).to_have_url(re.compile(r'.*(conditions|customer).*', re.IGNORECASE))