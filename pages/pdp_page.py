from playwright.sync_api import expect

from components.header_components import HeaderComponents
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponents(page)

        self.product_title = page.locator('#title')
        self.main_product_image = page.locator("#landingImage, #imgTagWrapperId img")
        self.alt_images_gallery = page.locator("#altImages, #imageBlockThumbs")
        self.main_image_container = page.locator("#main-image-container")



    def get_product_title_name(self) -> str:
        expect(self.product_title).to_be_visible()
        return self.product_title.inner_text()

    def verify_product_gallery_visible(self):
        expect(self.main_product_image).to_be_visible(timeout=15000)
        if self.alt_images_gallery.count() > 0:
            expect(self.alt_images_gallery.nth(0)).to_be_visible(timeout=15000)
        else:
            expect(self.main_image_container).to_be_visible(timeout=15000)




