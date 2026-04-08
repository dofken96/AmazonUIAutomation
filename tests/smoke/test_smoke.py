import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.pdp_page import ProductDetailPage
from pages.search_result_page import SearchResultPage




def test_homepage_key_header_components(page):
    home_page = HomePage(page)
    home_page.open()
    home_page.verify_main_attributes_visible()



def test_search_header_returns_results(page):
    home_page = HomePage(page)
    search_result_page = SearchResultPage(page)
    home_page.open()
    home_page.search_a_product('laptop')
    search_result_page.validate_searched_product_name('laptop')


def test_product_search_result(localized_page):
    home_page = HomePage(localized_page)
    search_result_page = SearchResultPage(localized_page)
    pdp_page = ProductDetailPage(localized_page)

    home_page.open()
    home_page.search_a_product('wireless mouse')
    search_result_page.click_on_first_product()
    product_name = pdp_page.get_product_title_name()
    assert product_name != '', 'Product title should not be empty'



@pytest.mark.parametrize('product_numbers', [1,3])
def test_add_product_cart_pdp(localized_page, product_numbers):
    home_page = HomePage(localized_page)
    search_result_page = SearchResultPage(localized_page)
    cart_page = CartPage(localized_page)

    home_page.open()
    home_page.search_a_product('wireless mouse')

    before_count = home_page.header.get_number_of_items_in_cart()

    search_result_page.add_several_products_to_cart(product_numbers)
    after_count = home_page.header.get_number_of_items_in_cart()

    # print(f'\nItems in cart after adding: {after_count}\n')

    assert before_count < after_count

    search_result_page.header.open_cart_page()
    cart_page.get_cart_items()
    cart_page.remove_products_from_cart()

    items_in_cart_after_removal = home_page.header.get_number_of_items_in_cart()

    assert items_in_cart_after_removal == 0





@pytest.mark.parametrize('product_numbers', [3])
@pytest.mark.xfail(reason = 'Flaky test due to possible issues with the checkout page loading or cart state management. Needs investigation.')
def test_proceed_to_checkout(auth_localized_page, product_numbers):
    home_page = HomePage(auth_localized_page)
    search_result_page = SearchResultPage(auth_localized_page)
    cart_page = CartPage(auth_localized_page)
    check_out_page = CheckoutPage(auth_localized_page)

    home_page.open()
    home_page.search_a_product('wireless mouse')
    search_result_page.add_several_products_to_cart(product_numbers)
    search_result_page.header.open_cart_page()
    cart_page.proceed_to_checkout()
    check_out_page.check_checkout_page_loaded()
    cart_page.header.open_cart_page()
    cart_page.remove_products_from_cart()




