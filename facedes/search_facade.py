from components.header_components import HeaderComponents
from factories.page_factory import PageFactory
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.pdp_page import ProductDetailPage
from pages.search_result_page import SearchResultPage


class SearchFacade:
    def __init__(self, page):
        self.page = page
        self.page_factory = PageFactory(page)


    def search_a_product(self, product_name):

        home_page = self.page_factory.home_page()
        search_result_page = self.page_factory.search_result_page()

        home_page.open()
        home_page.verify_main_attributes_visible()
        home_page.search_a_product(product_name)
        search_result_page.validate_searched_product_name(product_name)


    def verify_searched_product_result(self, product_name):
        home_page = self.page_factory.home_page()
        search_result_page = self.page_factory.search_result_page()
        pdp_page = self.page_factory.pdp_page()


        home_page.open()
        home_page.search_a_product(product_name)
        search_result_page.click_on_first_product()
        pdp_page.get_product_title_name()
        assert product_name != '', 'Product title should not be empty'


    def add_products_to_cart(self, product_name, product_numbers, page):
        home_page = self.page_factory.home_page()
        search_result_page = self.page_factory.search_result_page()

        home_page.open()
        home_page.search_a_product(product_name)

        before_count = home_page.header.get_number_of_items_in_cart()
        page.reload()
        search_result_page.add_several_products_to_cart(product_numbers)
        page.reload()
        after_count = home_page.header.get_number_of_items_in_cart()

        assert before_count < after_count