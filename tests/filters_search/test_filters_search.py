from facedes.search_facade import SearchFacade


def test_search_query_encoded_url(page):
    """AMZ-0171: Search query is encoded in URL and decodes correctly after reload."""
    search_facade = SearchFacade(page)
    search_facade.verify_search_query_encoded_in_url("wireless headphones")


def test_search_apply_brand_filter(page):
    """AMZ-0172: Apply brand filter and verify active filter is shown."""
    search_facade = SearchFacade(page)
    search_facade.verify_brand_filter_refines_results_and_shows_active_chip("laptop")


def test_search_clear_individual_filter_by_removing_chip(page):
    """AMZ-0173: Clear individual filter by removing active chip/dismiss control."""
    search_facade = SearchFacade(page)
    search_facade.verify_remove_individual_brand_filter_by_chip("laptop")


def test_search_sort_dropdown_options_list(page):
    """AMZ-0174: Sort dropdown includes expected entries list (>= 5 options)."""
    search_facade = SearchFacade(page)
    search_facade.verify_sort_dropdown_includes_expected_entries("tablet", minimum_options=5)


def test_search_apply_free_shipping_filter(page):
    """AMZ-0175: Apply Free Shipping (or Prime) and verify badge appears in results."""
    search_facade = SearchFacade(page)
    search_facade.verify_free_shipping_filter_applies_and_badge_present("desk")


def test_search_department_category_left_nav_updates_breadcrumb(page):
    """AMZ-0176: Department left-nav selection updates breadcrumb/context."""
    search_facade = SearchFacade(page)
    search_facade.verify_department_left_nav_updates_breadcrumb("lego")


def test_search_price_slider_inputs_accept_min_max_and_enforce_numeric(page):
    """AMZ-0177: Price inputs accept numeric range and reject non-numeric values."""
    search_facade = SearchFacade(page)
    search_facade.verify_price_inputs_accept_numeric_and_reject_non_numeric("chair")


def test_search_rating_filter_four_stars_and_up(page):
    """AMZ-0178: Apply 4 Stars & Up rating filter and verify indicator/state."""
    search_facade = SearchFacade(page)
    search_facade.verify_rating_filter_four_stars_and_up_shows_indicator("headphones")


def test_search_multiple_filters_cumulative_effect_reflected_in_url_params(page):
    """AMZ-0179: Multiple filters have cumulative effect reflected in URL params."""
    search_facade = SearchFacade(page)
    search_facade.verify_multiple_filters_cumulative_effect_reflected_in_url("router")


def test_search_suggestion_click_navigates_to_results_for_suggestion_term(page):
    """AMZ-0180: Suggestion click navigates to results for clicked suggestion."""
    search_facade = SearchFacade(page)
    search_facade.verify_suggestion_click_navigates_to_results_term("airp")


def test_search_within_results_refine_query_updates_list(page):
    """AMZ-0181: Search within results refines query and updates results list/state."""
    search_facade = SearchFacade(page)
    search_facade.verify_search_within_results_refines_query_and_updates_list("camera", "dslr")


def test_search_click_see_more_on_filter_section_loads_more_options(page):
    """AMZ-0182: Click 'See more' in filter section and verify expansion."""
    search_facade = SearchFacade(page)
    search_facade.verify_click_see_more_expands_filter_options("phone case")


def test_search_apply_color_filter_updates_thumbnails_or_badges(page):
    """AMZ-0183: Apply color filter and verify active indicator/state."""
    search_facade = SearchFacade(page)
    search_facade.verify_color_filter_applies_and_indicator_visible("t shirt")


def test_search_toggle_prime_filter_on_off_updates_results_each_time(page):
    """AMZ-0184: Toggle Prime filter on/off and verify state updates each time."""
    search_facade = SearchFacade(page)
    search_facade.verify_prime_filter_toggle_on_off_updates_results("notebook")


def test_search_sorting_filter_combination_persists_across_pagination(page):
    """AMZ-0185: Sort + filter combination should persist across pagination."""
    search_facade = SearchFacade(page)
    search_facade.verify_sort_and_filter_persist_across_pagination("mouse")


def test_search_clear_all_resets_scroll_to_top_ux(page):
    """AMZ-0186: Clear all should reset filter state and scroll toward top."""
    search_facade = SearchFacade(page)
    search_facade.verify_clear_all_resets_scroll_and_filters("lamp")


def test_search_url_with_encoded_spaces_plus_and_percent20_both_work(page):
    """AMZ-0187: URL search with + and %20 space encodings should both work."""
    search_facade = SearchFacade(page)
    search_facade.verify_url_with_plus_and_percent20_both_work("wireless mouse")


def test_search_no_js_fallback_basic_navigation_works(page, browser):
    """AMZ-0188: Search fallback behavior with JavaScript disabled is non-empty/usable."""
    search_facade = SearchFacade(page)
    search_facade.verify_no_js_fallback_has_visible_body(browser)


def test_search_ensure_no_mixed_content_warnings_in_console(page):
    """AMZ-0189: Ensure no mixed-content warnings are present in console."""
    search_facade = SearchFacade(page)
    search_facade.verify_no_mixed_content_console_warnings("ssd")


def test_search_filter_state_remains_after_open_result_and_return(page):
    """AMZ-0190: Filter state remains after opening result and navigating back."""
    search_facade = SearchFacade(page)
    search_facade.verify_filter_state_remains_after_open_result_and_back("pillow")
