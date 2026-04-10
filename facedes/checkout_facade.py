from factories.page_factory import PageFactory


class CheckoutFacade:
    def __init__(self, page):
        self.page = page
        self.page_factory = PageFactory(page)
        self.search_result_page = self.page_factory.search_result_page()
        self.cart_page = self.page_factory.cart_page()
        self.checkout_page = self.page_factory.checkout_page()

    def do_checkout(self):
        self.search_result_page.header.open_cart_page()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.check_checkout_page_loaded()

        

