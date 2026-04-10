from factories.page_factory import PageFactory


class HomeFacade:
    def __init__(self, page):
        self.page = page
        self.page_factory = PageFactory(page)
        


    def check_homepage_key_header_components(self):
        home_page = self.page_factory.home_page()
        home_page.open()
        home_page.verify_main_attributes_visible()