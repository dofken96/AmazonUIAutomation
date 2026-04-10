from factories.page_factory import PageFactory


class CheckoutFacade:
    def __init__(self, page):
        self.page = page
        self.page_factory = PageFactory(page)


    def do_checkout(self, page):
        search_result_page = self.page_factory.search_result_page()
        cart_page = self.page_factory.cart_page()
        checkout_page = self.page_factory.checkout_page()

        search_result_page.header.open_cart_page()
        cart_page.proceed_to_checkout()
        checkout_page.check_checkout_page_loaded()

        

