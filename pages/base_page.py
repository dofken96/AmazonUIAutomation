from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def wait_for_page_loaded(self):
        self.page.wait_for_load_state("domcontentloaded")

    def make_screenshot(self, path):
        self.page.wait_for_load_state('networkidle')
        self.page.screenshot(path=path)

    def go_back(self):
        self.page.go_back()

    def go_forward(self):
        self.page.go_forward()

    def reload_page(self):
        self.page.reload()






