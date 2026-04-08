from playwright.sync_api import Page
from playwright.sync_api import expect, Error as PlaywrightError


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def safe_goto(
            self,
            url: str,
            ready_locator=None,
            retries: int = 3,
            timeout: int = 15000,
    ):
        """
        Stable navigation helper for flaky pages like Amazon.

        ready_locator:
            locator that proves the page is actually usable
            after navigation.
        """
        last_error = None

        for attempt in range(1, retries + 1):
            try:
                self.page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=timeout,
                )

                self.wait_for_page_loaded(ready_locator=ready_locator, timeout=timeout)
                return

            except PlaywrightError as error:
                last_error = error
                error_text = str(error)

                # Retry only for navigation-related flaky cases
                if "ERR_ABORTED" not in error_text and "Timeout" not in error_text:
                    raise

                if attempt == retries:
                    raise

                print(f"[safe_goto] retry {attempt}/{retries} because of: {error}")

                # Reset page state before next attempt
                self.page.goto("about:blank")
                self.page.wait_for_timeout(1000 * attempt)

        raise last_error

    def wait_for_page_loaded(self, ready_locator=None, timeout: int = 10000):
        """
        Wait until the page is in a usable state.
        Much better for Amazon than relying on networkidle.
        """

        # Wait until DOM is parsed
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)

        # Wait until browser says document is at least interactive
        self.page.wait_for_function(
            "() => document.readyState === 'interactive' || document.readyState === 'complete'",
            timeout=timeout,
        )

        # Optional: wait for the key page element
        if ready_locator is not None:
            expect(ready_locator).to_be_visible(timeout=timeout)


    def make_screenshot(self, path):
        self.page.wait_for_load_state('networkidle')
        self.page.screenshot(path=path)

    def go_back(self):
        self.page.go_back()

    def go_forward(self):
        self.page.go_forward()

    def reload_page(self):
        self.page.reload()

    def wait_for_3_seconds(self):
        self.page.wait_for_timeout(30000)







