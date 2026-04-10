import pytest

from facedes.cart_facade import CartFacade
from facedes.checkout_facade import CheckoutFacade
from facedes.home_facade import HomeFacade
from facedes.search_facade import SearchFacade



def test_homepage_key_header_components(page):
    home_facade = HomeFacade(page)
    home_facade.check_homepage_key_header_components()


def test_search_header_returns_results(page):
    search_facade = SearchFacade(page)
    search_facade.search_a_product('laptop')


def test_product_search_result(localized_page):
    search_facade = SearchFacade(localized_page)
    search_facade.verify_searched_product_result('wireless mouse')


@pytest.mark.parametrize('product_numbers', [1,3])
def test_add_product_cart_pdp(auth_localized_page, product_numbers):
    search_facade = SearchFacade(auth_localized_page)
    cart_facade = CartFacade(auth_localized_page)

    search_facade.add_products_to_cart('wireless mouse', product_numbers)
    cart_facade.remove_products_from_cart()
    


@pytest.mark.parametrize('product_numbers', [3])
def test_proceed_to_checkout(auth_localized_page, product_numbers):
    search_facade = SearchFacade(auth_localized_page)
    checkout_facade = CheckoutFacade(auth_localized_page)
    cart_facade = CartFacade(auth_localized_page)

    search_facade.add_products_to_cart('wireless mouse', product_numbers)
    checkout_facade.do_checkout()
    cart_facade.remove_products_from_cart()



def test_navigate_today_deals_top(localized_page):
    """AMZ-0007: Navigate to Today's Deals from top nav."""
    home_facade = HomeFacade(localized_page)
    home_facade.navigate_to_today_deals()



def test_hamburger_menu_departments_list(page):
    """AMZ-0008: Open hamburger menu and verify departments list."""
    home_facade = HomeFacade(page)
    home_facade.verify_hamburger_departments_list()


def test_footer_policy_link_works(page):
    """AMZ-0009: Footer links section visible and policy link works."""
    home_facade = HomeFacade(page)
    home_facade.verify_footer_policy_link()


def test_mobile_viewport_header(mobile_page):
    """AMZ-0010: Mobile viewport shows search, menu, and cart in header."""
    home_facade = HomeFacade(mobile_page)
    home_facade.verify_mobile_header()


def test_language_region_selector_opens(page):
    """AMZ-0011: Language/Region selector opens flyout or language preferences page."""
    home_facade = HomeFacade(page)
    home_facade.verify_language_region_selector()


def test_search_suggestions_dropdown_appears(page):
    """AMZ-0012: Search suggestions dropdown appears after typing partial query."""
    home_facade = HomeFacade(page)
    home_facade.verify_search_suggestions("iph")


def test_open_sign_in_page_via_account_lists(page):
    """AMZ-0013: Open sign-in page via Account & Lists."""
    home_facade = HomeFacade(page)
    home_facade.open_sign_in_via_account_lists()


def test_search_results_sorting_control_visible(page):
    """AMZ-0014: Search results sorting control is visible."""
    search_facade = SearchFacade(page)
    search_facade.verify_sorting_control_visible("headphones")


def test_product_image_gallery_present(localized_page):
    """AMZ-0015: Product image gallery is present on PDP."""
    search_facade = SearchFacade(localized_page)
    search_facade.verify_product_image_gallery_present("wireless mouse")


def test_search_results_pagination_next_control_visible(page):
    """AMZ-0017: Search results pagination/next control exists."""
    search_facade = SearchFacade(page)
    search_facade.verify_pagination_next_control_visible("usb cable")


def test_open_customer_service_page_from_nav(page):
    """AMZ-0018: Open customer service/help page from nav."""
    home_facade = HomeFacade(page)
    home_facade.open_customer_service_page()


def test_open_gift_cards_page_from_nav(page):
    """AMZ-0019: Open Gift Cards page from nav."""
    home_facade = HomeFacade(page)
    home_facade.open_gift_cards_page()


def test_no_severe_console_errors_homepage(page):
    """AMZ-0020: No severe console errors on homepage load."""
    home_facade = HomeFacade(page)
    home_facade.verify_no_severe_console_errors()

    


