from factories.page_factory import PageFactory


class CartFacade:
    def __init__(self, page):
        self.page = page
        self.page_factory = PageFactory(page)
        self.home_page = self.page_factory.home_page()
        self.search_result_page = self.page_factory.search_result_page()
        self.cart_page = self.page_factory.cart_page()

    def remove_products_from_cart(self):
        self.search_result_page.header.open_cart_page()
        self.cart_page.get_cart_items()
        self.cart_page.remove_products_from_cart()

        self.page.reload()
        items_in_cart_after_removal = self.home_page.header.get_number_of_items_in_cart()
        assert items_in_cart_after_removal == 0
