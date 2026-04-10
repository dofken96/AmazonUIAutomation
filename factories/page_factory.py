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


    def home_page(self):
        return HomePage(self.page)
        
    def search_result_page(self):
        return SearchResultPage(self.page)

    def pdp_page(self):
        return ProductDetailPage(self.page)

    def cart_page(self):
        return CartPage(self.page)

    def checkout_page(self):
        return CheckoutPage(self.page)

    def customer_service_page(self):
        return CustomerServicePage(self.page)
    
    def deals_page(self):
        return DealsPage(self.page)

    def gift_cards_page(self):
        return GiftCardsPage(self.page)
    
    def sign_in_page(self):
        return SignInPage(self.page)
    

