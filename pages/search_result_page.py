import re
import pytest
from playwright.sync_api import expect

from components.header_components import HeaderComponents
from pages.base_page import BasePage


class SearchResultPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponents(page)

        self.search_result_header = page.locator('.a-size-base.a-spacing-small.a-spacing-top-small.a-text-normal')
        self.search_product_name = self.search_result_header.locator('.a-color-state.a-text-bold')
        self.list_of_searched_items = page.locator('.s-main-slot.s-result-list.s-search-results.sg-row')
        self.sort_combobox = page.get_by_role("combobox", name=re.compile(r"sort by", re.I))
        self.sort_prompt = page.locator("span.a-dropdown-prompt")
        self.next_page_link = page.locator("a.s-pagination-next, a[aria-label*='Go to next page']")
        self.pagination_container = page.locator(".s-pagination-container")

        # self.items = page.locator('div[data-component-type="s-search-result"][data-asin]:not([data-asin=""])')
        self.items = page.locator('div[role="listitem"]')
        self.active_filters_container = page.locator(
            "div[data-csa-c-type='widget'][data-csa-c-slot-id*='refinements']"
        )



    def validate_searched_product_name(self, search_product_name: str):
        expect(self.search_product_name).to_contain_text(search_product_name)


    def add_first_product_from_list_to_cart(self):
        self.wait_for_page_loaded()

        first_item = self.items.nth(0)
        expect(first_item).to_be_visible()

        add_to_cart_button = first_item.get_by_role('button', name='Add to cart')

        add_to_cart_button.click()

        stepper_controls = first_item.locator('.a-stepper-controls')
        expect(stepper_controls).to_be_visible()




    def click_on_first_product(self):
        self.wait_for_page_loaded()

        first_item = self.items.nth(0)
        expect(first_item).to_be_visible()
        header = first_item.locator("a h2")
        header.click()

    def add_several_products_to_cart(self, number_of_products: int):
        expect(self.items.last).to_be_visible()
        added_products = 0
        candidate_index = 0
        max_candidates = max(number_of_products * 6, number_of_products + 5)

        while added_products < number_of_products and candidate_index < max_candidates:
            self.page.reload()
            expect(self.header.cart_count_locator).to_be_visible()
            before_number = self.header.get_number_of_items_in_cart()

            item = self.items.nth(candidate_index)
            candidate_index += 1

            if not item.is_visible():
                continue

            item.scroll_into_view_if_needed()
            add_to_cart_button = item.get_by_role('button', name='Add to cart')

            if add_to_cart_button.count() == 0:
                continue

            try:
                add_to_cart_button.click(timeout=5000)
            except Exception:
                continue

            self.page.wait_for_timeout(1500)
            after_number = self.header.get_number_of_items_in_cart()

            if after_number > before_number:
                added_products += 1

        assert added_products >= number_of_products, (
            f"Could not add requested number of products. "
            f"Requested={number_of_products}, Added={added_products}"
        )

    def verify_sort_control_visible(self):
        self.wait_for_page_loaded()

        if self.sort_combobox.count() > 0:
            expect(self.sort_combobox).to_be_visible()
            return

        expect(self.sort_prompt).to_be_visible()

    def verify_pagination_next_control_visible(self):
        self.wait_for_page_loaded()
        self.page.mouse.wheel(0, 12000)

        if self.next_page_link.count() > 0:
            expect(self.next_page_link).to_be_visible(timeout=15000)
            return

        expect(self.pagination_container).to_be_visible(timeout=15000)

    def verify_sort_options_count_at_least(self, minimum_options: int = 5):
        self.wait_for_page_loaded()

        if self.sort_combobox.count() > 0 and self.sort_combobox.first.is_visible():
            options = self.sort_combobox.first.locator("option")
            if options.count() >= minimum_options:
                return

        trigger = self.sort_prompt if self.sort_prompt.count() > 0 else self.sort_combobox.first
        if trigger.count() == 0:
            pytest.skip("Sort control is not available on this SERP variant.")

        trigger.click(timeout=7000)
        dropdown_options = self.page.locator(
            "li.a-dropdown-item, "
            "ul.a-nostyle.a-list-link li, "
            "[role='listbox'] [role='option']"
        )
        expect(dropdown_options.first).to_be_visible(timeout=10000)

        option_texts = [
            text.strip()
            for text in dropdown_options.all_inner_texts()
            if text and text.strip()
        ]
        unique_options = list(dict.fromkeys(option_texts))
        assert len(unique_options) >= minimum_options, (
            f"Expected at least {minimum_options} sort options, got {len(unique_options)}: {unique_options}"
        )

    def apply_free_shipping_or_prime_filter(self) -> str | None:
        """Apply Free Shipping (preferred) or Prime filter when available."""
        self.wait_for_page_loaded()
        refinements = self.page.locator("#s-refinements").first
        if refinements.count() == 0:
            return None

        shipping_candidates = refinements.locator(
            "a[href*='rh=']:has-text('Free Shipping'), "
            "a[href*='rh=']:has-text('FREE Shipping'), "
            "a[href*='rh=']:has-text('Prime'), "
            "label:has-text('Free Shipping'), "
            "label:has-text('Prime')"
        )

        candidate_count = shipping_candidates.count()
        if candidate_count == 0:
            return None

        for index in range(min(candidate_count, 8)):
            option = shipping_candidates.nth(index)
            if not option.is_visible():
                continue

            option_text = (option.inner_text() or "").strip()
            if not option_text:
                continue

            clickable = option
            if option.evaluate("el => el.tagName.toLowerCase()") not in {"a", "button", "label"}:
                clickable = option.locator(
                    "xpath=ancestor-or-self::*[self::a or self::button or self::label][1]"
                ).first
            if clickable.count() == 0:
                continue

            before_url = self.page.url
            clickable.click(timeout=7000)
            self.page.wait_for_load_state("domcontentloaded")
            self.verify_results_visible()

            if self.page.url != before_url or self.page.locator(
                "span.a-color-state, a[aria-current='page']"
            ).filter(has_text=re.compile(r"free shipping|prime", re.I)).count() > 0:
                return option_text

        return None

    def verify_shipping_badge_present_in_top_results(self, sample_size: int = 8):
        self.verify_results_visible()
        max_items = min(self.items.count(), sample_size)
        found_badge = False
        for index in range(max_items):
            card = self.items.nth(index)
            if not card.is_visible():
                continue
            card_text = (card.inner_text() or "").strip()
            if re.search(r"free shipping|prime", card_text, re.I):
                found_badge = True
                break
        assert found_badge, "No Free Shipping/Prime badge text found in top search results."

    def apply_department_filter_from_left_nav(self) -> str | None:
        """Apply first available department/category link from left refinements."""
        self.wait_for_page_loaded()
        refinements = self.page.locator("#s-refinements").first
        if refinements.count() == 0:
            return None

        dept_section = refinements.locator(
            "#departments, div[aria-label*='Department'], div[id*='departments']"
        ).first
        if dept_section.count() == 0:
            dept_section = refinements.locator(
                "xpath=.//*[self::span or self::h2][contains(translate(normalize-space(.), "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'department')]"
                "/ancestor::*[self::div or self::section][1]"
            ).first
        if dept_section.count() == 0:
            return None

        candidates = dept_section.locator("a[href*='rh='], a[href*='i%3A'], a[href*='i=']")
        for index in range(min(candidates.count(), 12)):
            link = candidates.nth(index)
            if not link.is_visible():
                continue
            label = (link.inner_text() or "").strip()
            if not label or label.lower() in {"see more", "show more", "department", "departments"}:
                continue

            before_url = self.page.url
            before_header = (self.search_result_header.inner_text() or "").strip()
            link.click(timeout=7000)
            self.page.wait_for_load_state("domcontentloaded")
            self.verify_results_visible()

            after_header = (self.search_result_header.inner_text() or "").strip()
            if self.page.url != before_url or after_header != before_header:
                return label

        return None

    def verify_breadcrumb_or_heading_updated_for_department(self, department_name: str) -> bool:
        breadcrumb = self.page.locator(
            "li.a-breadcrumb span, "
            "a.a-link-normal.a-color-tertiary, "
            "span.a-color-state"
        ).filter(has_text=re.compile(re.escape(department_name), re.I)).first
        if breadcrumb.count() > 0 and breadcrumb.is_visible():
            return True

        header_text = (self.search_result_header.inner_text() or "").strip()
        return bool(re.search(re.escape(department_name), header_text, re.I))

    def verify_results_visible(self):
        expect(self.items.first).to_be_visible(timeout=20000)

    def apply_first_available_brand_filter(self) -> str | None:
        """Apply any visible brand filter from the left rail and return its label."""
        self.wait_for_page_loaded()
        brand_section = self.page.locator(
            "div[role='group'][aria-label*='Brand'], "
            "#brandsRefinements, "
            "div[id*='p_89/'], "
            "li[id*='p_123/']"
        ).first

        if brand_section.count() == 0:
            # fallback to section by heading text
            brand_section = self.page.locator(
                "xpath=//*[self::h2 or self::span][contains(translate(normalize-space(.), "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'brand')]"
                "/ancestor::*[self::div or self::section][1]"
            ).first

        if brand_section.count() == 0:
            return None

        brand_candidates = brand_section.locator("li[aria-label]:has(a), a[href*='rh=']")

        candidate_count = brand_candidates.count()
        if candidate_count == 0:
            return None

        selected_label = ""
        for index in range(min(candidate_count, 12)):
            option = brand_candidates.nth(index)
            if not option.is_visible():
                continue

            clickable = option
            if "a" not in (option.evaluate("el => el.tagName.toLowerCase()")):
                nested_link = option.locator("a[href*='rh=']").first
                if nested_link.count() == 0:
                    continue
                clickable = nested_link

            option_text = (option.get_attribute("aria-label") or clickable.inner_text() or "").strip()
            option_text = re.sub(r"\s+\(\d+\)$", "", option_text).strip()
            if not option_text or option_text.lower() in {"brand", "brands", "see more", "sponsored"}:
                continue

            before_url = self.page.url
            clickable.click(timeout=7000)
            self.page.wait_for_load_state("domcontentloaded")
            self.verify_results_visible()
            if self.page.url != before_url or self.has_active_filter_visible_for_brand(option_text):
                selected_label = option_text
                break

        return selected_label or None

    def verify_active_filter_visible_for_brand(self, brand_name: str):
        """Verify active filter chip/label row includes selected brand."""
        chip_like = self.page.locator(
            "span.a-color-state, "
            "a[aria-current='page'], "
            "li[aria-current='true']"
        ).filter(has_text=re.compile(re.escape(brand_name), re.I)).first
        expect(chip_like).to_be_visible(timeout=15000)

    def has_active_filter_visible_for_brand(self, brand_name: str) -> bool:
        chip_like = self.page.locator(
            "span.a-color-state, "
            "a[aria-current='page'], "
            "li[aria-current='true']"
        ).filter(has_text=re.compile(re.escape(brand_name), re.I)).first
        return chip_like.count() > 0 and chip_like.is_visible()

    def clear_active_filter_for_brand(self, brand_name: str):
        """Try to clear a selected brand via chip dismiss control (AMZ-0173)."""
        chip_like = self.page.locator(
            "span.a-color-state, "
            "a[aria-current='page'], "
            "li[aria-current='true']"
        ).filter(has_text=re.compile(re.escape(brand_name), re.I)).first
        dismiss_inside_chip = chip_like.locator(
            "xpath=ancestor::*[self::li or self::span or self::div][1]//*[self::a or self::button]"
        ).filter(has_text=re.compile(r"clear|remove|close|x", re.I)).first

        dismiss_control = dismiss_inside_chip
        if dismiss_control.count() == 0:
            brand_section = self.page.locator(
                "div[role='group'][aria-label*='Brand'], "
                "#brandsRefinements, "
                "div[id*='p_89/'], "
                "li[id*='p_123/']"
            ).first
            dismiss_control = brand_section.locator(
                "a, button"
            ).filter(has_text=re.compile(r"clear|remove", re.I)).first

        if dismiss_control.count() == 0:
            dismiss_control = self.page.locator(
                "a[aria-label*='Clear'], button[aria-label*='Clear'], "
                "a[aria-label*='Remove'], button[aria-label*='Remove']"
            ).filter(has_text=re.compile(re.escape(brand_name), re.I)).first

        if dismiss_control.count() == 0:
            dismiss_control = self.page.locator(
                "a, button"
            ).filter(has_text=re.compile(r"clear all|clear filters", re.I)).first

        if dismiss_control.count() > 0:
            dismiss_control.click(timeout=10000)
        else:
            # Fallback for SERP variants without a visible chip dismiss button:
            # click the selected brand filter option again to toggle it off.
            brand_section = self.page.locator(
                "div[role='group'][aria-label*='Brand'], "
                "#brandsRefinements, "
                "div[id*='p_89/'], "
                "li[id*='p_123/']"
            ).first
            toggle_control = brand_section.locator(
                "a, button, label, span"
            ).filter(has_text=re.compile(re.escape(brand_name), re.I)).first
            assert toggle_control.count() > 0, (
                f"Could not find a control to clear selected brand filter {brand_name!r}."
            )
            toggle_control.click(timeout=10000)

        self.page.wait_for_load_state("domcontentloaded")
        self.verify_results_visible()

    def verify_active_filter_not_visible_for_brand(self, brand_name: str):
        chip_like = self.page.locator(
            "span.a-color-state, "
            "a[aria-current='page'], "
            "li[aria-current='true']"
        ).filter(has_text=re.compile(re.escape(brand_name), re.I)).first
        expect(chip_like).not_to_be_visible(timeout=15000)

    def verify_price_inputs_numeric_and_apply_range(self, min_price: int, max_price: int) -> bool:
        """Validate price min/max inputs sanitize non-numeric values and accept numeric range."""
        self.wait_for_page_loaded()
        min_input = self.page.locator(
            "input#low-price, input[name='low-price'], input[aria-label*='Min'], input[placeholder*='Min']"
        ).first
        max_input = self.page.locator(
            "input#high-price, input[name='high-price'], input[aria-label*='Max'], input[placeholder*='Max']"
        ).first

        if min_input.count() == 0 or max_input.count() == 0:
            return False
        if not min_input.is_visible() or not max_input.is_visible():
            return False

        min_input.fill("abc")
        min_input.press("Tab")
        sanitized = (min_input.input_value() or "").strip()
        assert sanitized == "" or sanitized.isdigit(), (
            f"Expected non-numeric price input to be sanitized, got {sanitized!r}"
        )

        before_url = self.page.url
        min_input.fill(str(min_price))
        max_input.fill(str(max_price))

        form = min_input.locator("xpath=ancestor::form[1]")
        apply_btn = form.locator(
            "input[type='submit'], button[type='submit'], button:has-text('Go')"
        ).first if form.count() > 0 else self.page.locator(
            "input[type='submit'], button[type='submit'], button:has-text('Go')"
        ).first

        if apply_btn.count() > 0 and apply_btn.is_visible():
            apply_btn.click(timeout=7000)
        else:
            max_input.press("Enter")

        self.page.wait_for_load_state("domcontentloaded")
        self.verify_results_visible()

        min_after = (min_input.input_value() or "").strip() if min_input.count() > 0 else ""
        max_after = (max_input.input_value() or "").strip() if max_input.count() > 0 else ""
        values_ok = (
            (min_after == "" or min_after.isdigit()) and (max_after == "" or max_after.isdigit())
        )
        assert values_ok, f"Price inputs contain invalid values after apply: min={min_after!r}, max={max_after!r}"

        state_changed = self.page.url != before_url or "p_36" in self.page.url or "price-range" in self.page.url
        assert state_changed, "Expected URL/search state to change after applying numeric price range."
        return True

    def apply_rating_filter_four_stars_and_up(self) -> str | None:
        """Apply 4+ stars rating filter when present."""
        self.wait_for_page_loaded()
        refinements = self.page.locator("#s-refinements").first
        if refinements.count() == 0:
            return None

        rating_options = refinements.locator(
            "a[href*='p_72']:has-text('4 Stars'), "
            "a[href*='p_72']:has-text('4 stars'), "
            "a[href*='p_72']:has-text('Up'), "
            "a[href*='rh=']:has-text('4 Stars'), "
            "a[href*='rh=']:has-text('4 stars')"
        )
        if rating_options.count() == 0:
            return None

        for index in range(min(rating_options.count(), 6)):
            option = rating_options.nth(index)
            if not option.is_visible():
                continue
            label = (option.inner_text() or "").strip()
            before_url = self.page.url
            option.click(timeout=7000)
            self.page.wait_for_load_state("domcontentloaded")
            self.verify_results_visible()
            if self.page.url != before_url or self.has_rating_filter_indicator():
                return label or "4 Stars & Up"
        return None

    def has_rating_filter_indicator(self) -> bool:
        indicator = self.page.locator(
            "span.a-color-state, a[aria-current='page'], li[aria-current='true']"
        ).filter(has_text=re.compile(r"4\s*stars?|4\s*&\s*up|4\+\s*stars?", re.I)).first
        return indicator.count() > 0 and indicator.is_visible()

    def apply_color_filter(self) -> str | None:
        self.wait_for_page_loaded()
        refinements = self.page.locator("#s-refinements").first
        if refinements.count() == 0:
            return None

        color_section = refinements.locator(
            "#p_n_feature_thirty_browse-bin, #colorsRefinements, div[aria-label*='Color']"
        ).first
        if color_section.count() == 0:
            color_section = refinements.locator(
                "xpath=.//*[self::span or self::h2][contains(translate(normalize-space(.), "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'color')]"
                "/ancestor::*[self::div or self::section][1]"
            ).first
        if color_section.count() == 0:
            return None

        options = color_section.locator("a[href*='rh='], li[aria-label]:has(a), span.a-color-base")
        for index in range(min(options.count(), 12)):
            option = options.nth(index)
            if not option.is_visible():
                continue
            label = (option.get_attribute("aria-label") or option.inner_text() or "").strip()
            label = re.sub(r"\s+\(\d+\)$", "", label).strip()
            if not label or label.lower() in {"color", "colors", "see more"}:
                continue

            clickable = option
            if option.evaluate("el => el.tagName.toLowerCase()") not in {"a", "button", "label"}:
                clickable = option.locator("xpath=ancestor-or-self::*[self::a or self::button or self::label][1]").first
            if clickable.count() == 0:
                continue

            before_url = self.page.url
            clickable.click(timeout=7000)
            self.page.wait_for_load_state("domcontentloaded")
            self.verify_results_visible()
            if self.page.url != before_url or self.has_filter_indicator_text(label):
                return label
        return None

    def has_filter_indicator_text(self, text_value: str) -> bool:
        indicator = self.page.locator(
            "span.a-color-state, a[aria-current='page'], li[aria-current='true']"
        ).filter(has_text=re.compile(re.escape(text_value), re.I)).first
        return indicator.count() > 0 and indicator.is_visible()

    def apply_prime_filter(self) -> bool:
        self.wait_for_page_loaded()
        refinements = self.page.locator("#s-refinements").first
        if refinements.count() == 0:
            return False
        prime_control = refinements.locator(
            "a[href*='p_85']:has-text('Prime'), label:has-text('Prime'), a[href*='rh=']:has-text('Prime')"
        ).first
        if prime_control.count() == 0 or not prime_control.is_visible():
            return False
        before_url = self.page.url
        prime_control.click(timeout=7000)
        self.page.wait_for_load_state("domcontentloaded")
        self.verify_results_visible()
        return self.page.url != before_url or self.has_filter_indicator_text("Prime")

    def clear_all_filters_if_available(self) -> bool:
        clear_all = self.page.locator(
            "a:has-text('Clear all'), button:has-text('Clear all'), a:has-text('Clear Filters')"
        ).first
        if clear_all.count() == 0 or not clear_all.is_visible():
            return False
        clear_all.click(timeout=7000)
        self.page.wait_for_load_state("domcontentloaded")
        self.verify_results_visible()
        return True

    def has_any_active_filter_indicator(self) -> bool:
        indicators = self.page.locator("span.a-color-state, a[aria-current='page'], li[aria-current='true']")
        return indicators.count() > 0 and indicators.first.is_visible()

    def open_sort_dropdown_and_select_non_default(self) -> str | None:
        self.wait_for_page_loaded()
        if self.sort_combobox.count() > 0 and self.sort_combobox.first.is_visible():
            options = self.sort_combobox.first.locator("option")
            for idx in range(1, min(options.count(), 6)):
                value = options.nth(idx).get_attribute("value")
                text = (options.nth(idx).inner_text() or "").strip()
                if not value or not text:
                    continue
                self.sort_combobox.first.select_option(value=value)
                self.page.wait_for_load_state("domcontentloaded")
                self.verify_results_visible()
                return text
            return None

        trigger = self.sort_prompt.first if self.sort_prompt.count() > 0 else self.page.locator("span.a-dropdown-prompt").first
        if trigger.count() == 0 or not trigger.is_visible():
            return None
        trigger.click(timeout=7000)
        options = self.page.locator("li.a-dropdown-item a")
        if options.count() < 2:
            return None
        chosen = options.nth(1)
        text = (chosen.inner_text() or "").strip()
        chosen.click(timeout=7000)
        self.page.wait_for_load_state("domcontentloaded")
        self.verify_results_visible()
        return text or None

    def go_to_next_pagination_page(self) -> bool:
        self.page.mouse.wheel(0, 12000)
        next_link = self.page.locator("a.s-pagination-next:not(.s-pagination-disabled), a[aria-label*='Go to next page']")
        if next_link.count() == 0 or not next_link.first.is_visible():
            return False
        before_url = self.page.url
        next_link.first.click(timeout=7000)
        self.page.wait_for_load_state("domcontentloaded")
        self.verify_results_visible()
        return self.page.url != before_url

    def expand_filter_section_with_see_more(self) -> bool:
        """Click 'See more' in any filter section and verify options increase/expand."""
        self.wait_for_page_loaded()
        refinements = self.page.locator("#s-refinements").first
        if refinements.count() == 0:
            return False

        see_more_controls = refinements.locator(
            "a:has-text('See more'), button:has-text('See more'), "
            "a:has-text('See More'), button:has-text('See More')"
        )
        if see_more_controls.count() == 0:
            return False

        for index in range(min(see_more_controls.count(), 8)):
            control = see_more_controls.nth(index)
            if not control.is_visible():
                continue

            section = control.locator("xpath=ancestor::*[self::div or self::section or self::ul][1]")
            options_before = section.locator("li, a").count() if section.count() > 0 else 0
            control.click(timeout=7000)
            self.page.wait_for_timeout(800)

            options_after = section.locator("li, a").count() if section.count() > 0 else 0
            see_less_visible = section.locator(
                "a:has-text('See less'), button:has-text('See less'), "
                "a:has-text('See Less'), button:has-text('See Less')"
            ).count() > 0 if section.count() > 0 else False
            if options_after > options_before or see_less_visible:
                return True

        return False









