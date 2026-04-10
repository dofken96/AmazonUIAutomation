from facedes.base_facade import BaseFacade


class CheckoutFacade(BaseFacade):
    def __init__(self, page):
        super().__init__(page)
        self.search_result_page = self.page_factory.search_result_page()
        self.cart_page = self.page_factory.cart_page()
        self.checkout_page = self.page_factory.checkout_page()

    def do_checkout(self):
        self.invoke(
            (
                ("Open cart page", self.search_result_page.header.open_cart_page),
                ("Proceed to checkout", self.cart_page.proceed_to_checkout),
                ("Verify checkout page loaded", self.checkout_page.check_checkout_page_loaded),
            )
        )

        

