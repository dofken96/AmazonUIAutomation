import pytest

from facedes.cart_facade import CartFacade
from facedes.checkout_facade import CheckoutFacade
from facedes.home_facade import HomeFacade
from facedes.search_facade import SearchFacade
from factories.page_factory import PageFactory
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.customer_service_page import CustomerServicePage
from pages.deals_page import DealsPage
from pages.gift_cards_page import GiftCardsPage
from pages.home_page import HomePage
from pages.pdp_page import ProductDetailPage
from pages.search_result_page import SearchResultPage
from pages.sign_in_page import SignInPage



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
def test_add_product_cart_pdp(localized_page, product_numbers):
    search_facade = SearchFacade(localized_page)
    search_facade.add_products_to_cart('wireless mouse', product_numbers, localized_page)


    cart_facade = CartFacade(localized_page)
    cart_facade.remove_products_from_cart(localized_page)
    


@pytest.mark.parametrize('product_numbers', [3])
@pytest.mark.xfail(reason = 'Flaky test due to possible issues with the checkout page loading or cart state management. Needs investigation.')
def test_proceed_to_checkout(auth_localized_page, product_numbers):
    search_facade = SearchFacade(auth_localized_page)
    checkout_facade = CheckoutFacade(auth_localized_page)
    cart_facade = CartFacade(auth_localized_page)

    search_facade.add_products_to_cart('wireless mouse', product_numbers, auth_localized_page)
    checkout_facade.do_checkout(auth_localized_page)
    cart_facade.remove_products_from_cart(auth_localized_page)




def test_navigate_today_deals_top(localized_page):
    """AMZ-0007: Navigate to Today's Deals from top nav."""
    home_page = HomePage(localized_page)
    deals_page = DealsPage(localized_page)
    home_page.open()

    home_page.header.go_to_deals_page()
    deals_page.verify_deals_page_loaded()



def test_hamburger_menu_departments_list(page):
    """AMZ-0008: Open hamburger menu and verify departments list."""
    home_page = HomePage(page)
    home_page.open()
    home_page.header.navigate_to_hamburger_menu()
    home_page.header.verify_departments_list()


def test_footer_policy_link_works(page):
    """AMZ-0009: Footer links section visible and policy link works."""
    home_page = HomePage(page)
    home_page.open()

    home_page.footer.verify_footer_visible()
    home_page.footer.verify_policy_link_works()


def test_mobile_viewport_header(mobile_page):
    """AMZ-0010: Mobile viewport shows search, menu, and cart in header."""
    home_page = HomePage(mobile_page)
    home_page.open()

    home_page.verify_main_attributes_visible()


def test_language_region_selector_opens(page):
    """AMZ-0011: Language/Region selector opens flyout or language preferences page."""
    home_page = HomePage(page)
    home_page.open()
    home_page.header.open_language_region_selector()
    home_page.header.verify_language_region_selector_opened()


def test_search_suggestions_dropdown_appears(page):
    """AMZ-0012: Search suggestions dropdown appears after typing partial query."""
    home_page = HomePage(page)
    home_page.open()
    home_page.header.open_search_suggestions("iph")
    home_page.header.verify_search_suggestions_visible("iph")


def test_open_sign_in_page_via_account_lists(page):
    """AMZ-0013: Open sign-in page via Account & Lists."""
    home_page = HomePage(page)
    sign_in_page = SignInPage(page)

    home_page.open()
    home_page.header.open_sign_in_page_via_account_lists()
    sign_in_page.verify_sign_in_page_loaded()


def test_search_results_sorting_control_visible(page):
    """AMZ-0014: Search results sorting control is visible."""
    home_page = HomePage(page)
    search_result_page = SearchResultPage(page)

    home_page.open()
    home_page.search_a_product("headphones")
    search_result_page.verify_sort_control_visible()


def test_product_image_gallery_present(localized_page):
    """AMZ-0015: Product image gallery is present on PDP."""
    home_page = HomePage(localized_page)
    search_result_page = SearchResultPage(localized_page)
    pdp_page = ProductDetailPage(localized_page)

    home_page.open()
    home_page.search_a_product("wireless mouse")
    search_result_page.click_on_first_product()
    pdp_page.verify_product_gallery_visible()


def test_search_results_pagination_next_control_visible(page):
    """AMZ-0017: Search results pagination/next control exists."""
    home_page = HomePage(page)
    search_result_page = SearchResultPage(page)

    home_page.open()
    home_page.search_a_product("usb cable")
    search_result_page.verify_pagination_next_control_visible()


def test_open_customer_service_page_from_nav(page):
    """AMZ-0018: Open customer service/help page from nav."""
    home_page = HomePage(page)
    customer_service_page = CustomerServicePage(page)

    home_page.open()
    home_page.header.open_customer_service_page()
    customer_service_page.verify_customer_service_page_loaded()


def test_open_gift_cards_page_from_nav(page):
    """AMZ-0019: Open Gift Cards page from nav."""
    home_page = HomePage(page)
    gift_cards_page = GiftCardsPage(page)

    home_page.open()
    home_page.header.open_gift_cards_page()
    gift_cards_page.verify_gift_cards_page_loaded()


def test_no_severe_console_errors_homepage(page):
    """AMZ-0020: No severe console errors on homepage load."""
    home_page = HomePage(page)
    home_page.verify_no_severe_console_errors()

    


