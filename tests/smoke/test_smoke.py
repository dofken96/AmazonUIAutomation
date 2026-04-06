"""Homepage loads and key header components visible"""
from pages.home_page import HomePage
from pages.search_result_page import SearchResultPage

"""
"1. Navigate to the homepage.
2. Wait for DOM content loaded.
3. Verify search box is visible.
4. Verify cart link/icon is visible.
5. Verify hamburger/All menu is visible."


page.goto(), page.wait_for_load_state(), page.get_by_role(), expect(locator).to_be_visible()


"""


def test_homepage_key_header_components(page):

    home_page = HomePage(page)
    home_page.open()
    home_page.verify_main_attributes_visible()


"""
"1. Open homepage.
2. Type query into search box.
3. Submit search (Enter).
4. Verify results container appears and URL changes to a search path."

"""

def test_search_header_returns_results(page):
    home_page = HomePage(page)
    search_result_page = SearchResultPage(page)
    home_page.open()
    home_page.search_a_product('laptop')
    search_result_page.validate_searched_product_name('laptop')


def test_add_product_cart_pdp(localized_page):
    home_page = HomePage(localized_page)
    search_result_page = SearchResultPage(localized_page)

    home_page.open()
    home_page.search_a_product('wireless mouse')

    before_count = home_page.header.get_number_of_items_in_cart()

    search_result_page.add_product_first_product_from_list_to_cart()
    after_count = home_page.header.get_number_of_items_in_cart()

    assert before_count < after_count




