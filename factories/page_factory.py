from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.customer_service_page import CustomerServicePage
from pages.deals_page import DealsPage
from pages.gift_cards_page import GiftCardsPage
from pages.home_page import HomePage
from pages.pdp_page import ProductDetailPage
from pages.search_result_page import SearchResultPage
from pages.sign_in_page import SignInPage


class PageFactory:
    def __init__(self, page):
        self.page = page
        self._cache = {}


    def home_page(self):
        return self._get("home_page", HomePage)
        
    def search_result_page(self):
        return self._get("search_result_page", SearchResultPage)

    def pdp_page(self):
        return self._get("pdp_page", ProductDetailPage)

    def cart_page(self):
        return self._get("cart_page", CartPage)

    def checkout_page(self):
        return self._get("checkout_page", CheckoutPage)

    def customer_service_page(self):
        return self._get("customer_service_page", CustomerServicePage)
    
    def deals_page(self):
        return self._get("deals_page", DealsPage)

    def gift_cards_page(self):
        return self._get("gift_cards_page", GiftCardsPage)
    
    def sign_in_page(self):
        return self._get("sign_in_page", SignInPage)

    def _get(self, key, page_class):
        if key not in self._cache:
            self._cache[key] = page_class(self.page)
        return self._cache[key]

