from factories.page_factory import PageFactory


class SearchFacade:
    def __init__(self, page):
        self.page = page
        self.page_factory = PageFactory(page)
        self.home_page = self.page_factory.home_page()
        self.search_result_page = self.page_factory.search_result_page()
        self.pdp_page = self.page_factory.pdp_page()

    def search_a_product(self, product_name):
        self.home_page.open()
        self.home_page.verify_main_attributes_visible()
        self.home_page.search_a_product(product_name)
        self.search_result_page.validate_searched_product_name(product_name)


    def verify_searched_product_result(self, product_name):
        self.home_page.open()
        self.home_page.search_a_product(product_name)
        self.search_result_page.click_on_first_product()
        product_title = self.pdp_page.get_product_title_name()
        assert product_title.strip() != "", "Product title should not be empty"


    def add_products_to_cart(self, product_name, product_numbers):
        self.home_page.open()
        self.home_page.search_a_product(product_name)

        before_count = self.home_page.header.get_number_of_items_in_cart()
        self.page.reload()
        self.search_result_page.add_several_products_to_cart(product_numbers)
        self.page.reload()
        after_count = self.home_page.header.get_number_of_items_in_cart()

        assert before_count < after_count

    def verify_sorting_control_visible(self, product_name):
        self.home_page.open()
        self.home_page.search_a_product(product_name)
        self.search_result_page.verify_sort_control_visible()

    def verify_product_image_gallery_present(self, product_name):
        self.home_page.open()
        self.home_page.search_a_product(product_name)
        self.search_result_page.click_on_first_product()
        self.pdp_page.verify_product_gallery_visible()

    def verify_pagination_next_control_visible(self, product_name):
        self.home_page.open()
        self.home_page.search_a_product(product_name)
        self.search_result_page.verify_pagination_next_control_visible()
