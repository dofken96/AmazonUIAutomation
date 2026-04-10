from facedes.base_facade import BaseFacade


class CartFacade(BaseFacade):
    def __init__(self, page):
        super().__init__(page)
        self.home_page = self.page_factory.home_page()
        self.search_result_page = self.page_factory.search_result_page()
        self.cart_page = self.page_factory.cart_page()

    def remove_products_from_cart(self):
        self.invoke(
            (
                ("Open cart page", self.search_result_page.header.open_cart_page),
                ("Get current cart items", self.cart_page.get_cart_items),
                ("Remove items from cart", self.cart_page.remove_products_from_cart),
            )
        )
        items_in_cart_after_removal = self.home_page.header.get_number_of_items_in_cart()
        assert items_in_cart_after_removal == 0
