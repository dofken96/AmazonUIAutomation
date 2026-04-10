from facedes.base_facade import BaseFacade


class HomeFacade(BaseFacade):
    def __init__(self, page):
        super().__init__(page)
        self.home_page = self.page_factory.home_page()
        self.deals_page = self.page_factory.deals_page()
        self.sign_in_page = self.page_factory.sign_in_page()
        self.customer_service_page = self.page_factory.customer_service_page()
        self.gift_cards_page = self.page_factory.gift_cards_page()


    def check_homepage_key_header_components(self):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Verify key header components", self.home_page.verify_main_attributes_visible),
            )
        )

    def navigate_to_today_deals(self):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Open Today's Deals from header", self.home_page.header.go_to_deals_page),
                ("Verify deals page is loaded", self.deals_page.verify_deals_page_loaded),
            )
        )

    def verify_hamburger_departments_list(self):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Open hamburger menu", self.home_page.header.navigate_to_hamburger_menu),
                ("Verify departments list", self.home_page.header.verify_departments_list),
            )
        )

    def verify_footer_policy_link(self):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Verify footer section is visible", self.home_page.footer.verify_footer_visible),
                ("Verify policy link navigation works", self.home_page.footer.verify_policy_link_works),
            )
        )

    def verify_mobile_header(self):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Verify mobile header key elements", self.home_page.verify_main_attributes_visible),
            )
        )

    def verify_language_region_selector(self):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Open language/region selector", self.home_page.header.open_language_region_selector),
                ("Verify language/region selector opened", self.home_page.header.verify_language_region_selector_opened),
            )
        )

    def verify_search_suggestions(self, partial_query: str):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Type partial query to trigger suggestions", lambda: self.home_page.header.open_search_suggestions(partial_query)),
                ("Verify suggestions are visible", lambda: self.home_page.header.verify_search_suggestions_visible(partial_query)),
            )
        )

    def open_sign_in_via_account_lists(self):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Open sign-in from Account & Lists", self.home_page.header.open_sign_in_page_via_account_lists),
                ("Verify sign-in page loaded", self.sign_in_page.verify_sign_in_page_loaded),
            )
        )

    def open_customer_service_page(self):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Open customer service from navigation", self.home_page.header.open_customer_service_page),
                ("Verify customer service page loaded", self.customer_service_page.verify_customer_service_page_loaded),
            )
        )

    def open_gift_cards_page(self):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Open gift cards from navigation", self.home_page.header.open_gift_cards_page),
                ("Verify gift cards page loaded", self.gift_cards_page.verify_gift_cards_page_loaded),
            )
        )

    def verify_no_severe_console_errors(self):
        self.invoke((("Verify no severe console errors on homepage", self.home_page.verify_no_severe_console_errors),))
