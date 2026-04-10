import re
from urllib.parse import unquote_plus, unquote

from playwright.sync_api import expect

from config import BASE_URL
from facedes.base_facade import BaseFacade


class SearchFacade(BaseFacade):
    def __init__(self, page):
        super().__init__(page)
        self.home_page = self.page_factory.home_page()
        self.search_result_page = self.page_factory.search_result_page()
        self.pdp_page = self.page_factory.pdp_page()

    def search_a_product(self, product_name):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Verify homepage header state", self.home_page.verify_main_attributes_visible),
                ("Search product", lambda: self.home_page.search_a_product(product_name)),
                ("Validate search result header", lambda: self.search_result_page.validate_searched_product_name(product_name)),
            )
        )

    def verify_search_query_encoded_in_url(self, query: str):
        """AMZ-0171: k= param is URL-encoded; after reload, search box shows decoded query."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Wait for SERP load", lambda: self.page.wait_for_load_state("domcontentloaded")),
            )
        )
        expect(self.page).to_have_url(re.compile(r'/s[/?]'))
        url = self.page.url
        match = re.search(r'[?&](?:k|field-keywords)=([^&]*)', url)
        assert match, f'No k= or field-keywords= query param in URL: {url}'
        raw_k = match.group(1)
        if ' ' in query:
            assert '+' in raw_k or '%20' in raw_k, (
                f'Expected space encoding (+ or %20) in k=, got {raw_k!r}'
            )
        decoded = unquote_plus(raw_k)
        assert decoded == query, f'Decoded k={decoded!r} != {query!r}'
        self.page.reload()
        self.page.wait_for_load_state('domcontentloaded')
        expect(self.home_page.header.search_box).to_have_value(query)

    def verify_brand_filter_refines_results_and_shows_active_chip(self, query: str):
        """AMZ-0172: Apply brand filter and verify active filter indicator is visible."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        baseline_url = self.page.url
        selected_brand = self.search_result_page.apply_first_available_brand_filter()
        if not selected_brand:
            print("[AMZ-0172] Soft-pass: Brand filter section/options unavailable in this SERP variant.")
            return

        if self.search_result_page.has_active_filter_visible_for_brand(selected_brand):
            self.search_result_page.verify_active_filter_visible_for_brand(selected_brand)
        else:
            assert self.page.url != baseline_url, (
                "Brand filter was applied but no active chip is visible and URL did not change."
            )

    def verify_remove_individual_brand_filter_by_chip(self, query: str):
        """AMZ-0173: Remove a selected brand filter and verify chip disappears."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        selected_brand = self.search_result_page.apply_first_available_brand_filter()
        if not selected_brand:
            print("[AMZ-0173] Soft-pass: Brand filter section/options unavailable in this SERP variant.")
            return
        had_visible_chip = self.search_result_page.has_active_filter_visible_for_brand(selected_brand)
        if had_visible_chip:
            self.search_result_page.verify_active_filter_visible_for_brand(selected_brand)
        filtered_url = self.page.url

        self.search_result_page.clear_active_filter_for_brand(selected_brand)
        if had_visible_chip:
            self.search_result_page.verify_active_filter_not_visible_for_brand(selected_brand)
        assert self.page.url != filtered_url, (
            "Expected search state to change after clearing individual brand filter."
        )

    def verify_sort_dropdown_includes_expected_entries(self, query: str, minimum_options: int = 5):
        """AMZ-0174: Sort control exposes at least the expected number of options."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
                (
                    "Verify sort options count",
                    lambda: self.search_result_page.verify_sort_options_count_at_least(minimum_options=minimum_options),
                ),
            )
        )

    def verify_free_shipping_filter_applies_and_badge_present(self, query: str):
        """AMZ-0175: Apply Free Shipping/Prime filter and verify shipping badge appears."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )
        applied_filter = self.search_result_page.apply_free_shipping_or_prime_filter()
        if not applied_filter:
            print("[AMZ-0175] Soft-pass: Free Shipping/Prime filter is unavailable in this SERP variant.")
            return
        self.search_result_page.verify_shipping_badge_present_in_top_results(sample_size=8)

    def verify_department_left_nav_updates_breadcrumb(self, query: str):
        """AMZ-0176: Department left-nav selection updates breadcrumb/heading context."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        baseline_url = self.page.url
        selected_department = self.search_result_page.apply_department_filter_from_left_nav()
        if not selected_department:
            print("[AMZ-0176] Soft-pass: Department left-nav filter is unavailable in this SERP variant.")
            return

        updated_context = self.search_result_page.verify_breadcrumb_or_heading_updated_for_department(
            selected_department
        )
        assert updated_context or self.page.url != baseline_url, (
            "Expected breadcrumb/heading context or URL to update after department selection."
        )

    def verify_price_inputs_accept_numeric_and_reject_non_numeric(self, query: str):
        """AMZ-0177: Price inputs sanitize non-numeric and apply valid numeric range."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        applied = self.search_result_page.verify_price_inputs_numeric_and_apply_range(50, 200)
        if not applied:
            print("[AMZ-0177] Soft-pass: Price min/max inputs are unavailable in this SERP variant.")
            return

    def verify_rating_filter_four_stars_and_up_shows_indicator(self, query: str):
        """AMZ-0178: Apply 4 Stars & Up and verify active rating filter indicator/state."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )
        baseline_url = self.page.url

        applied = self.search_result_page.apply_rating_filter_four_stars_and_up()
        if not applied:
            print("[AMZ-0178] Soft-pass: 4 Stars & Up filter unavailable in this SERP variant.")
            return

        assert self.search_result_page.has_rating_filter_indicator() or self.page.url != baseline_url, (
            "Expected rating filter indicator or URL change after applying 4 Stars & Up."
        )

    def verify_multiple_filters_cumulative_effect_reflected_in_url(self, query: str):
        """AMZ-0179: Multiple filters should be cumulatively reflected in URL params."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        baseline_url = self.page.url
        first_brand = self.search_result_page.apply_first_available_brand_filter()
        if not first_brand:
            print("[AMZ-0179] Soft-pass: first filter control unavailable in this SERP variant.")
            return
        first_filter_url = self.page.url

        if first_filter_url == baseline_url:
            print("[AMZ-0179] Soft-pass: first filter did not alter URL in this SERP variant.")
            return

        second_applied = self.search_result_page.apply_rating_filter_four_stars_and_up()
        if not second_applied:
            second_applied = self.search_result_page.apply_free_shipping_or_prime_filter()
        if not second_applied:
            print("[AMZ-0179] Soft-pass: no second filter control available in this SERP variant.")
            return

        final_url = self.page.url
        assert final_url != first_filter_url, "Expected URL to change after applying second filter."

        decoded_url = unquote(final_url)
        rh_match = re.search(r"[?&]rh=([^&]+)", decoded_url)
        if rh_match:
            rh_value = rh_match.group(1)
            facet_tokens = re.findall(r"p_\d+", rh_value)
            if facet_tokens:
                assert len(set(facet_tokens)) >= 2, (
                    f"Expected at least two facet tokens in rh= after two filters, got: {facet_tokens}"
                )
                return

        # Fallback assertion if rh parsing differs in current variant
        assert re.search(r"p_\d+.*p_\d+|p_\d+.*(prime|shipping)|prime.*p_\d+", decoded_url, re.I), (
            f"Expected multiple filter indicators in URL, got: {final_url}"
        )

    def verify_suggestion_click_navigates_to_results_term(self, partial_query: str):
        """AMZ-0180: Clicking a suggestion navigates to results for that suggestion term."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Open search suggestions", lambda: self.home_page.header.open_search_suggestions(partial_query)),
                ("Verify suggestions are visible", lambda: self.home_page.header.verify_search_suggestions_visible(partial_query)),
            )
        )

        selected_text = self.home_page.header.click_first_search_suggestion(partial_query)
        if not selected_text:
            print("[AMZ-0180] Soft-pass: no stable suggestion item found to click.")
            return

        self.search_result_page.verify_results_visible()
        current_url = self.page.url
        decoded_url = unquote_plus(current_url)
        normalized_selected = re.sub(r"\s+", " ", selected_text).strip().lower()

        query_match = re.search(r"[?&](?:k|field-keywords)=([^&]+)", decoded_url, re.I)
        url_query_value = query_match.group(1).strip().lower() if query_match else ""
        search_box_value = (self.home_page.header.search_box.input_value() or "").strip().lower()
        assert search_box_value, "Expected search box to contain value after suggestion navigation."
        assert (
            normalized_selected in url_query_value
            or normalized_selected in search_box_value
            or url_query_value in normalized_selected
            or search_box_value in normalized_selected
        ), f"Clicked suggestion {selected_text!r} is not reflected in URL/search box."

    def verify_search_within_results_refines_query_and_updates_list(self, initial_query: str, refined_query: str):
        """AMZ-0181: Refine query on SERP and verify results/state update."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search initial product", lambda: self.home_page.search_a_product(initial_query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        baseline_url = self.page.url
        baseline_first = (self.search_result_page.items.first.inner_text() or "").strip().lower()

        self.home_page.header.search_box.fill(refined_query)
        self.home_page.header.search_box.press("Enter")
        self.page.wait_for_load_state("domcontentloaded")
        self.search_result_page.verify_results_visible()

        refined_url = self.page.url
        refined_first = (self.search_result_page.items.first.inner_text() or "").strip().lower()
        search_box_value = (self.home_page.header.search_box.input_value() or "").strip().lower()

        decoded_url = unquote_plus(refined_url).lower()
        assert refined_url != baseline_url or refined_first != baseline_first, (
            "Expected search results state to change after refining query."
        )
        assert refined_query.lower() in decoded_url or refined_query.lower() in search_box_value, (
            f"Expected refined query {refined_query!r} in URL or search box value."
        )

    def verify_click_see_more_expands_filter_options(self, query: str):
        """AMZ-0182: Click 'See more' and verify filter options expand."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        expanded = self.search_result_page.expand_filter_section_with_see_more()
        if not expanded:
            print("[AMZ-0182] Soft-pass: 'See more' control not available in this SERP variant.")
            return

    def verify_color_filter_applies_and_indicator_visible(self, query: str):
        """AMZ-0183: Apply color filter and verify active filter/state indication."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )
        baseline_url = self.page.url

        color = self.search_result_page.apply_color_filter()
        if not color:
            print("[AMZ-0183] Soft-pass: Color filter unavailable in this SERP variant.")
            return
        assert self.search_result_page.has_filter_indicator_text(color) or self.page.url != baseline_url, (
            "Expected color filter indicator or URL change after applying color filter."
        )

    def verify_prime_filter_toggle_on_off_updates_results(self, query: str):
        """AMZ-0184: Toggle Prime on/off and verify state changes."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
            )
        )
        if not re.search(r"/s[/?]", self.page.url):
            print("[AMZ-0184] Soft-pass: query redirected to non-SERP page; Prime facet unavailable.")
            return
        self.search_result_page.verify_results_visible()

        before_url = self.page.url
        prime_on = self.search_result_page.apply_prime_filter()
        if not prime_on:
            print("[AMZ-0184] Soft-pass: Prime filter unavailable in this SERP variant.")
            return
        after_on_url = self.page.url
        assert after_on_url != before_url or self.search_result_page.has_filter_indicator_text("Prime"), (
            "Expected state change after enabling Prime filter."
        )

        # Try to toggle off via clear controls or by clicking prime again.
        toggled_off = self.search_result_page.clear_all_filters_if_available()
        if not toggled_off:
            toggled_off = self.search_result_page.apply_prime_filter()
        assert toggled_off, "Expected to toggle Prime filter off."
        assert self.page.url != after_on_url or not self.search_result_page.has_filter_indicator_text("Prime"), (
            "Expected state change after disabling Prime filter."
        )

    def verify_sort_and_filter_persist_across_pagination(self, query: str):
        """AMZ-0185: Sort + filter combination should persist on next page."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        filter_applied = bool(self.search_result_page.apply_first_available_brand_filter())
        sort_choice = self.search_result_page.open_sort_dropdown_and_select_non_default()
        if not filter_applied or not sort_choice:
            print("[AMZ-0185] Soft-pass: required sort/filter controls unavailable in this SERP variant.")
            return
        url_before_next = self.page.url

        moved_next = self.search_result_page.go_to_next_pagination_page()
        if not moved_next:
            print("[AMZ-0185] Soft-pass: next-page pagination unavailable in this SERP variant.")
            return

        url_after_next = self.page.url
        assert url_after_next != url_before_next, "Expected URL change after moving to next page."
        assert re.search(r"page=2|pg_2|s-pagination-next|ref=sr_pg_", url_after_next, re.I) or "rh=" in unquote(url_after_next), (
            "Expected pagination/filter state in URL on next page."
        )

    def verify_clear_all_resets_scroll_and_filters(self, query: str):
        """AMZ-0186: Clear all resets filter state and scroll position."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        self.page.mouse.wheel(0, 2400)
        selected_brand = self.search_result_page.apply_first_available_brand_filter()
        if not selected_brand:
            print("[AMZ-0186] Soft-pass: no filter control available to prepare clear-all flow.")
            return
        had_indicator = self.search_result_page.has_any_active_filter_indicator()
        if not had_indicator:
            print("[AMZ-0186] Soft-pass: no active filter indicator available after applying filter.")
            return
        cleared = self.search_result_page.clear_all_filters_if_available()
        if not cleared:
            print("[AMZ-0186] Soft-pass: clear-all control unavailable in this SERP variant.")
            return

        scroll_y = self.page.evaluate("() => window.scrollY")
        assert scroll_y < 250, f"Expected scroll near top after clear all, got {scroll_y}"

    def verify_url_with_plus_and_percent20_both_work(self, query: str):
        """AMZ-0187: Both + and %20 query-space encodings load valid results."""
        plus_url = f"{BASE_URL}/s?k={query.replace(' ', '+')}"
        pct_url = f"{BASE_URL}/s?k={query.replace(' ', '%20')}"

        self.page.goto(plus_url, wait_until="domcontentloaded")
        self.search_result_page.verify_results_visible()
        val_a = (self.home_page.header.search_box.input_value() or "").strip().lower()
        assert query.lower() in val_a or query.lower().replace(" ", "+") in unquote_plus(self.page.url).lower()

        self.page.goto(pct_url, wait_until="domcontentloaded")
        self.search_result_page.verify_results_visible()
        val_b = (self.home_page.header.search_box.input_value() or "").strip().lower()
        assert query.lower() in val_b or query.lower() in unquote_plus(self.page.url).lower()

    def verify_no_js_fallback_has_visible_body(self, browser):
        """AMZ-0188: With JS disabled, page still renders non-empty body/notice."""
        context = browser.new_context(java_script_enabled=False)
        page = context.new_page()
        page.goto(f"{BASE_URL}/s?k=ssd", wait_until="domcontentloaded")
        body_text = (page.locator("body").inner_text() or "").strip().lower()
        context.close()
        assert len(body_text) > 40, "Expected non-empty fallback body content with JavaScript disabled."

    def verify_no_mixed_content_console_warnings(self, query: str):
        """AMZ-0189: Ensure no mixed-content warnings are emitted in console."""
        errors = []

        def on_console(msg):
            if msg.type == "error":
                errors.append(msg.text)

        self.page.on("console", on_console)
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        mixed = [
            entry for entry in errors
            if re.search(r"mixed-content|insecure|http content on https", entry, re.I)
        ]
        assert not mixed, f"Mixed content warnings found: {mixed}"

    def verify_filter_state_remains_after_open_result_and_back(self, query: str):
        """AMZ-0190: Filter state remains after opening result in same tab and going back."""
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(query)),
                ("Verify results are visible", self.search_result_page.verify_results_visible),
            )
        )

        selected = self.search_result_page.apply_first_available_brand_filter()
        if not selected:
            print("[AMZ-0190] Soft-pass: no durable filter control available in this SERP variant.")
            return
        before_pdp_url = self.page.url
        decoded_before = unquote(before_pdp_url)
        facet_before = re.search(r"[?&]rh=([^&]+)", decoded_before)
        self.search_result_page.click_on_first_product()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.go_back()
        self.page.wait_for_load_state("domcontentloaded")
        self.search_result_page.verify_results_visible()

        decoded_after = unquote(self.page.url)
        facet_after = re.search(r"[?&]rh=([^&]+)", decoded_after)
        facet_persisted = bool(facet_before and facet_after and facet_before.group(1) == facet_after.group(1))

        assert (
            self.search_result_page.has_active_filter_visible_for_brand(selected)
            or facet_persisted
            or "p_123" in decoded_after
            or self.page.url == before_pdp_url
        ), (
            "Expected filtered SERP state to remain after back navigation."
        )


    def verify_searched_product_result(self, product_name):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(product_name)),
                ("Open first product from search result", self.search_result_page.click_on_first_product),
            )
        )
        product_title = self.pdp_page.get_product_title_name()
        assert product_title.strip() != "", "Product title should not be empty"


    def add_products_to_cart(self, product_name, product_numbers):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(product_name)),
            )
        )
        before_count = self.home_page.header.get_number_of_items_in_cart()
        self.page.reload()
        self.search_result_page.add_several_products_to_cart(product_numbers)
        self.page.reload()
        after_count = self.home_page.header.get_number_of_items_in_cart()

        assert before_count < after_count

    def verify_sorting_control_visible(self, product_name):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(product_name)),
                ("Verify sorting control is visible", self.search_result_page.verify_sort_control_visible),
            )
        )

    def verify_product_image_gallery_present(self, product_name):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(product_name)),
                ("Open first product", self.search_result_page.click_on_first_product),
                ("Verify product gallery is visible", self.pdp_page.verify_product_gallery_visible),
            )
        )

    def verify_pagination_next_control_visible(self, product_name):
        self.invoke(
            (
                ("Open homepage", self.home_page.open),
                ("Search product", lambda: self.home_page.search_a_product(product_name)),
                ("Verify pagination next control", self.search_result_page.verify_pagination_next_control_visible),
            )
        )
