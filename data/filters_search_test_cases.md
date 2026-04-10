# Amazon UI — Filters / Search Test Cases

**Source:** `amazon_playwright_test_matrix.xlsx` → sheet `Test_Cases` → group `Filters / Search`
**Total:** 20 test cases | **Generated:** 2026-04-09

---

## Table of Contents

| ID | Title | Area | Priority |
|----|-------|------|----------|
| [AMZ-0171](#amz-0171) | Search: verify query is encoded in URL and decodes correctly | Search Results | P2 |
| [AMZ-0172](#amz-0172) | Search: apply brand filter refines results and shows active filter chip | Search Results | P2 |
| [AMZ-0173](#amz-0173) | Search: clear individual filter by removing chip | Search Results | P2 |
| [AMZ-0174](#amz-0174) | Search: sort dropdown options list includes expected entries | Search Results | P3 |
| [AMZ-0175](#amz-0175) | Search: apply 'Free Shipping' (if present) and verify shipping badge appears | Search Results | P4 |
| [AMZ-0176](#amz-0176) | Search: department category left-nav selection updates breadcrumb | Search Results | P3 |
| [AMZ-0177](#amz-0177) | Search: price slider/inputs accept min/max and enforce numeric | Search Results | P4 |
| [AMZ-0178](#amz-0178) | Search: rating filter (4 stars & up) shows filter indicator | Search Results | P3 |
| [AMZ-0179](#amz-0179) | Search: multiple filters cumulative effect reflected in URL params | Search Results | P3 |
| [AMZ-0180](#amz-0180) | Search: suggestion click navigates to results for suggestion term | Home | P3 |
| [AMZ-0181](#amz-0181) | Search: search within results (refine query) updates list | Search Results | P3 |
| [AMZ-0182](#amz-0182) | Search: click 'See more' on filter section loads more options | Search Results | P4 |
| [AMZ-0183](#amz-0183) | Search: apply color filter updates thumbnails or badges | Search Results | P4 |
| [AMZ-0184](#amz-0184) | Search: toggle Prime filter on/off updates results each time | Search Results | P3 |
| [AMZ-0185](#amz-0185) | Search: sorting + filter combination persists across pagination | Search Results | P4 |
| [AMZ-0186](#amz-0186) | Search: clear all resets scroll to top (UX) | Search Results | P4 |
| [AMZ-0187](#amz-0187) | Search: URL with encoded spaces (+ or %20) both work | Routing/Search | P4 |
| [AMZ-0188](#amz-0188) | Search: no-JS fallback basic navigation works (disable JS) | Search Results | P5 |
| [AMZ-0189](#amz-0189) | Search: ensure no mixed-content warnings in console | Search Results | P4 |
| [AMZ-0190](#amz-0190) | Search: filter state remains after opening a result in same tab and returning | Search Results | P3 |

---

## Test Cases

---

### AMZ-0171

**Search: verify query is encoded in URL and decodes correctly**

| Field | Value |
|-------|-------|
| Short Name | Search Query Encoded URL |
| Area / Page | Search Results |
| Priority | P2 |
| Tags | search, routing |

**Preconditions / Test Data**
Search query: `wireless headphones`

**Steps to Reproduce**
1. Open the Amazon homepage and locate the main search input (`page.get_by_role('searchbox', name=...)`).
2. Enter `wireless headphones` into the search box and submit (`locator.fill()`, `locator.press('Enter')` or click the Go button).
3. Wait for the search results page to load (`page.wait_for_load_state('domcontentloaded')`).
4. Read the current URL (`page.url`) and assert the query parameter for `k` (or equivalent) contains URL-encoded characters (e.g. spaces as `+` or `%20`) — use `expect(page).to_have_url(re.compile(...))` as appropriate.
5. Reload the page (`page.reload()`).
6. After reload, locate the search input on the results page (header or inline) and verify its value matches the human-readable query `wireless headphones` (`expect(search_locator).to_have_value('wireless headphones')` or equivalent).

**Expected Result**
The search term is preserved in the URL using proper encoding; after reload, the search box shows the decoded, readable query string.

**Playwright (Python) APIs**
`page.get_by_role()`, `expect(page).to_have_url()`, `page.reload()`, `expect(locator).to_have_value()`

**Automation Notes**
Medium risk.

---

### AMZ-0172 -- DONE

**Search: apply brand filter refines results and shows active filter chip**

| Field | Value |
|-------|-------|
| Short Name | Search Apply Brand Filter |
| Area / Page | Search Results |
| Priority | P2 |
| Tags | filters |

**Preconditions / Test Data**
Search query: `laptop`

**Steps to Reproduce**
1. Navigate to Amazon and run a search for `laptop`; wait until the results grid is visible (`expect(results_container).to_be_visible()`).
2. In the left-hand filter rail (or mobile filter drawer), locate a **Brand** filter section — if no brand facet is shown for this query, **skip or soft-assert** per project policy (`pytest.skip` or mark xfail).
3. Click a brand checkbox or brand link (`locator.click()`).
4. Wait for the results to refresh (`page.wait_for_load_state('domcontentloaded')` and/or `expect` on result count or spinner disappearance).
5. Verify an **active filter** chip or pill appears near the top of results showing the selected brand (`expect(chip_locator).to_be_visible()`).
6. Optionally assert the URL or result count changed compared to the unfiltered state (store `page.url` or `locator.count()` before/after).

**Expected Result**
The brand filter applies, the UI shows the active filter, and the result set reflects the refinement.

**Playwright (Python) APIs**
`page.locator()`, `locator.click()`, `page.wait_for_load_state()`, `expect(locator).to_be_visible()`

**Automation Notes**
High risk — brand facets and chip markup vary by category and A/B tests.

---

### AMZ-0173 -- DONE

**Search: clear individual filter by removing chip**

| Field | Value |
|-------|-------|
| Short Name | Search Clear Individual Filter |
| Area / Page | Search Results |
| Priority | P2 |
| Tags | filters, state |

**Preconditions / Test Data**
Start from search query `laptop` with **at least one** filter already applied (perform steps from AMZ-0172 first in the same session, or navigate to a URL that includes filter params).

**Steps to Reproduce**
1. Open search results for `laptop` and apply one filter so an active filter chip appears (e.g. brand).
2. Locate the chip’s dismiss control — typically an **×** or “Close” on the chip (`page.get_by_role('button', name=re.compile(r'close|remove', re.I))` scoped to the chip row).
3. Click the dismiss control (`locator.click()`).
4. Wait for the results list to update.
5. Verify the chip for that filter is gone (`expect(chip).to_be_hidden()` or `expect(chip).not_to_be_visible()`).
6. Verify results broaden again (URL params updated, or result titles/count differ from filtered-only state).

**Expected Result**
Removing one chip clears only that filter; results refresh to match the remaining filters and query.

**Playwright (Python) APIs**
`page.locator()`, `locator.click()`, `page.wait_for_load_state()`, `expect(locator).to_be_hidden()`

**Automation Notes**
High risk — chip selectors and animation timing vary.

---

### AMZ-0174 -- DONE

**Search: sort dropdown options list includes expected entries**

| Field | Value |
|-------|-------|
| Short Name | Search Sort Dropdown Options |
| Area / Page | Search Results |
| Priority | P3 |
| Tags | search, ui |

**Preconditions / Test Data**
Search query: `tablet`

**Steps to Reproduce**
1. Search for `tablet` and wait for results.
2. Locate the **Sort by** control (dropdown or button) — often labeled “Featured”, “Price: Low to High”, etc. (`page.locator('[aria-label*="Sort"]')` or similar).
3. Open the sort control (`locator.click()`).
4. Capture the list of visible options (dropdown menu, listbox, or flyout).
5. Assert the list includes **at least five** recognizable sort modes (e.g. price ascending/descending, avg. customer review, newest arrivals — exact labels depend on locale). Use `expect(option_locator.nth(i)).to_have_text(...)` or collect text with `all_inner_texts()`.

**Expected Result**
The sort control exposes a reasonable set of sort options (minimum five distinct modes as per matrix).

**Playwright (Python) APIs**
`page.locator()`, `locator.click()`, `expect(locator).to_be_visible()`, `expect(locator).to_have_text()`

**Automation Notes**
High risk — labels and DOM differ by marketplace and device.

---

### AMZ-0175 -- DONE

**Search: apply 'Free Shipping' (if present) and verify shipping badge appears**

| Field | Value |
|-------|-------|
| Short Name | Search Apply Free Shipping |
| Area / Page | Search Results |
| Priority | P4 |
| Tags | filters, data-driven |

**Preconditions / Test Data**
Search query: `desk`

**Steps to Reproduce**
1. Search for `desk` and wait for results.
2. In the filter rail, look for **Free Shipping** (or “Prime” / eligible shipping) — **if the control is not present**, document skip or soft-pass per team rules.
3. Enable the Free Shipping filter (`locator.click()`).
4. Wait for results to refresh (`page.wait_for_load_state()`).
5. Inspect the first several result cards for a **FREE Shipping** or Prime-eligible badge (`expect(result.locator('text=/FREE Shipping|Prime/i')).to_be_visible()` on at least one card, if inventory allows).

**Expected Result**
With the filter on, at least some results show shipping eligibility consistent with the filter; URL or facets reflect the selection.

**Playwright (Python) APIs**
`page.locator()`, `locator.click()`, `page.wait_for_load_state()`, `expect(locator).to_be_visible()`

**Automation Notes**
High risk — filter naming and badges vary; inventory may show zero eligible items.

---

### AMZ-0176 -- DONE

**Search: department category left-nav selection updates breadcrumb**

| Field | Value |
|-------|-------|
| Short Name | Search Department Category Left |
| Area / Page | Search Results |
| Priority | P3 |
| Tags | filters, navigation |

**Preconditions / Test Data**
Search query: `lego`

**Steps to Reproduce**
1. Search for `lego` and wait for the results page.
2. Note the current breadcrumb or category heading text (if visible) for baseline.
3. In the **left navigation** department/category tree, click a subcategory (e.g. “Building Sets”) — use a stable `get_by_role('link', name=...)` or text match.
4. Wait for navigation or in-place update (`page.wait_for_load_state()`).
5. Verify the breadcrumb trail or results heading updates to include the selected department (`expect(breadcrumb_locator).to_contain_text(...)`).

**Expected Result**
Category refinement updates the user-visible context (breadcrumb and/or heading) to match the selection.

**Playwright (Python) APIs**
`page.locator()`, `locator.click()`, `page.wait_for_load_state()`, `expect(locator).to_have_text()`

**Automation Notes**
High risk — left nav structure differs on mobile vs desktop.

---

### AMZ-0177 -- DONE

**Search: price slider/inputs accept min/max and enforce numeric**

| Field | Value |
|-------|-------|
| Short Name | Search Price Slider Inputs |
| Area / Page | Search Results |
| Priority | P4 |
| Tags | filters, forms |

**Preconditions / Test Data**
Search query: `chair`

**Steps to Reproduce**
1. Search for `chair` and open the **Price** filter section if collapsed.
2. Locate min and/or max price inputs (or slider endpoints).
3. Enter **non-numeric** characters (e.g. `abc`) into min or max (`locator.fill('abc')`).
4. Attempt to apply or blur the field — verify the UI **rejects, clears, or sanitizes** input (`expect(locator).to_have_value('')` or validation message visible).
5. Enter a **valid numeric range** (e.g. min `50`, max `200`) and apply (`locator.press('Enter')` or click Apply).
6. Verify the inputs retain numeric values and results or URL reflect the range (`expect(locator).to_have_value(...)`).

**Expected Result**
Non-numeric input is not accepted as a filter; valid numeric ranges apply correctly.

**Playwright (Python) APIs**
`page.locator()`, `locator.fill()`, `locator.press()`, `expect(locator).to_have_value()`

**Automation Notes**
High risk — some UIs use sliders only; mobile layouts differ.

---

### AMZ-0178 -- DONE

**Search: rating filter (4 stars & up) shows filter indicator**

| Field | Value |
|-------|-------|
| Short Name | Search Rating Filter 4 |
| Area / Page | Search Results |
| Priority | P3 |
| Tags | filters |

**Preconditions / Test Data**
Search query: `headphones`

**Steps to Reproduce**
1. Search for `headphones`.
2. In filters, locate **4 Stars & Up** (or “4+ stars”) — `page.get_by_text('4 Stars', exact=False)` or label near star icons.
3. Click to apply (`locator.click()`).
4. Wait for refresh.
5. Verify an active filter chip or facet shows the rating constraint (`expect(chip).to_be_visible()`).
6. Optionally spot-check that star ratings on visible results are ≥4 (sampling first N items).

**Expected Result**
The rating filter is applied and visibly indicated; results refresh.

**Playwright (Python) APIs**
`page.get_by_text()`, `locator.click()`, `page.wait_for_load_state()`, `expect(locator).to_be_visible()`

**Automation Notes**
High risk.

---

### AMZ-0179 -- DONE

**Search: multiple filters cumulative effect reflected in URL params**

| Field | Value |
|-------|-------|
| Short Name | Search Multiple Filters Cumulative |
| Area / Page | Search Results |
| Priority | P3 |
| Tags | filters, routing |

**Preconditions / Test Data**
Search query: `router`

**Steps to Reproduce**
1. Search for `router` and capture baseline URL.
2. Apply **two distinct filters** (e.g. brand + Prime, or price + rating) using clicks in the filter rail.
3. After each application, wait for `page.wait_for_load_state()` or network settle.
4. Read `page.url` and assert the query string contains **multiple** distinct filter-related parameters (e.g. `rh=` facets, or multiple `p_` keys — exact pattern depends on locale).
5. Use `expect(page).to_have_url(re.compile(...))` to allow flexible ordering.

**Expected Result**
Combined filter state is encoded in the URL so the page is shareable/bookmarkable with the same constraints.

**Playwright (Python) APIs**
`page.wait_for_url()`, `expect(page).to_have_url()`

**Automation Notes**
High risk — URL facet encoding is implementation-specific.

---

### AMZ-0180 -- DONE

**Search: suggestion click navigates to results for suggestion term**

| Field | Value |
|-------|-------|
| Short Name | Search Suggestion Click Navigates |
| Area / Page | Home |
| Priority | P3 |
| Tags | typeahead |

**Preconditions / Test Data**
Typeahead prefix: `airp` (expect suggestions like “airpods”, “airplane”, etc.)

**Steps to Reproduce**
1. Open the homepage (`page.goto(BASE_URL)`).
2. Focus the search box (`locator.click()`).
3. Type `airp` slowly or use `locator.press_sequentially()` to allow suggestions to load.
4. Wait for the suggestions dropdown (`expect(suggestion_panel).to_be_visible()`).
5. Click the **first or a stable** suggestion row (`locator.click()`).
6. Wait for navigation (`page.wait_for_url(...)`).
7. Assert the resulting URL’s `k=` (or equivalent) matches the clicked suggestion term (`expect(page).to_have_url(re.compile(...))`).
8. Verify the results heading or search box reflects that term.

**Expected Result**
Choosing a suggestion navigates to search results for that suggestion’s query string.

**Playwright (Python) APIs**
`page.get_by_role()`, `page.locator()`, `locator.click()`, `expect(page).to_have_url()`

**Automation Notes**
High risk — suggestion text and order vary.

---

### AMZ-0181 -- DONE

**Search: search within results (refine query) updates list**

| Field | Value |
|-------|-------|
| Short Name | Search Search Results Refine |
| Area / Page | Search Results |
| Priority | P3 |
| Tags | search, state |

**Preconditions / Test Data**
Initial query: `camera` — then refine to: `dslr`

**Steps to Reproduce**
1. Search for `camera` and wait for results.
2. Note a baseline — e.g. first result title snippet or result count.
3. Clear and replace the query in the **header search** (or inline search on SERP) with `dslr` (`locator.fill('dslr')`, `locator.press('Enter')`).
4. Wait for the new results page.
5. Verify the results container updates — titles or ASINs differ from the `camera`-only baseline (`expect(results).not_to_contain_text` is fragile; prefer URL `k=dslr` and visible product titles containing “DSLR” where applicable).

**Expected Result**
Refining the query replaces stale results with a list matching the new term.

**Playwright (Python) APIs**
`page.get_by_role()`, `locator.fill()`, `locator.press()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0182 -- DONE

**Search: click 'See more' on filter section loads more options**

| Field | Value |
|-------|-------|
| Short Name | Search Click See More |
| Area / Page | Search Results |
| Priority | P4 |
| Tags | filters, ui |

**Preconditions / Test Data**
Search query: `phone case`

**Steps to Reproduce**
1. Search for `phone case`.
2. Find a filter group with truncated options (Brand, Color, etc.) that exposes **See more** or **See More** (`page.get_by_role('button', name=re.compile(r'see more', re.I))`).
3. Note the number of visible filter options before expansion.
4. Click **See more**.
5. Verify additional options appear (`expect(new_option).to_be_visible()`) and the control may change to **See less**.

**Expected Result**
The filter section expands to show more values; the UI remains scrollable and usable.

**Playwright (Python) APIs**
`page.locator()`, `locator.click()`, `expect(locator).to_be_visible()`

**Automation Notes**
High risk — not all categories show “See more”.

---

### AMZ-0183 -- DONE

**Search: apply color filter updates thumbnails or badges**

| Field | Value |
|-------|-------|
| Short Name | Search Apply Color Filter |
| Area / Page | Search Results |
| Priority | P4 |
| Tags | filters |

**Preconditions / Test Data**
Search query: `t shirt`

**Steps to Reproduce**
1. Search for `t shirt`.
2. Open the **Color** facet if present (skip if missing).
3. Select a color swatch or label (e.g. “Black”) (`locator.click()`).
4. Wait for refresh.
5. Verify an active filter chip shows the color (`expect(chip).to_contain_text('Black')` or similar).
6. Spot-check result titles or variant lines for color keywords where the UI exposes them.

**Expected Result**
Color selection applies, is shown in active filters, and result cards reflect the variant where applicable.

**Playwright (Python) APIs**
`page.locator()`, `locator.click()`, `page.wait_for_load_state()`, `expect(locator).to_be_visible()`

**Automation Notes**
High risk — apparel faceting varies.

---

### AMZ-0184 -- DONE

**Search: toggle Prime filter on/off updates results each time**

| Field | Value |
|-------|-------|
| Short Name | Search Toggle Prime Filter |
| Area / Page | Search Results |
| Priority | P3 |
| Tags | filters, state |

**Preconditions / Test Data**
Search query: `book`

**Steps to Reproduce**
1. Search for `book`.
2. Locate the **Prime** checkbox or toggle in filters (`page.get_by_label('Prime')` or text match).
3. Turn Prime **on** (`click()`); wait for reload.
4. Capture URL or first-page result characteristics.
5. Turn Prime **off** (`click()` again); wait for reload.
6. Verify the filter state and results differ between on/off (chip present/absent, URL params, or result set).

**Expected Result**
Prime can be toggled twice; each toggle triggers a refresh and consistent UI state.

**Playwright (Python) APIs**
`page.locator()`, `locator.click()`, `page.wait_for_load_state()`, `expect(locator).to_be_visible()`

**Automation Notes**
High risk — Prime placement differs by locale.

---

### AMZ-0185 -- DONE

**Search: sorting + filter combination persists across pagination**

| Field | Value |
|-------|-------|
| Short Name | Search Sorting Filter Combination |
| Area / Page | Search Results |
| Priority | P4 |
| Tags | filters, pagination |

**Preconditions / Test Data**
Search query: `mouse`

**Steps to Reproduce**
1. Search for `mouse`.
2. Apply **one** non-sort filter (e.g. brand or price) and set **sort** to a non-default option (e.g. “Price: Low to High”).
3. Wait for results to stabilize; store `page.url`.
4. Scroll to pagination and click **Next** (or page 2) (`locator.click()`).
5. Wait for `page.wait_for_url()` or network idle.
6. Verify sort order control still shows the selected sort and the active filter chip(s) remain (`expect(...).to_be_visible()`).
7. Optionally assert URL still contains both sort and filter facets.

**Expected Result**
Pagination does not drop sort or filter state unexpectedly.

**Playwright (Python) APIs**
`page.locator()`, `locator.click()`, `page.wait_for_url()`, `expect(locator).to_be_visible()`

**Automation Notes**
High risk — infinite scroll vs numbered pages.

---

### AMZ-0186 -- DONE

**Search: clear all resets scroll to top (UX)**

| Field | Value |
|-------|-------|
| Short Name | Search Clear All Resets |
| Area / Page | Search Results |
| Priority | P4 |
| Tags | filters, ux |

**Preconditions / Test Data**
Search query: `lamp`

**Steps to Reproduce**
1. Search for `lamp`.
2. Scroll down the results page (`page.mouse.wheel(0, 2000)` or `locator.scroll_into_view()` on a lower result).
3. Apply any filter so chips appear.
4. Click **Clear all** on the active filters row (`page.get_by_role('button', name=re.compile(r'clear all', re.I))`).
5. After refresh, read scroll position via `page.evaluate('() => window.scrollY')`.
6. Assert scroll is near **top** (e.g. `scrollY < 200`) and filters are cleared (`expect(chip_row).not_to_be_visible()` or chip count zero).

**Expected Result**
Clearing filters resets facet state and returns the viewport toward the top of the results experience.

**Playwright (Python) APIs**
`page.mouse.wheel()`, `page.locator()`, `locator.click()`, `page.evaluate()`, `expect()`

**Automation Notes**
High risk — “Clear all” label and scroll behavior vary.

---

### AMZ-0187 -- DONE

**Search: URL with encoded spaces (+ or %20) both work**

| Field | Value |
|-------|-------|
| Short Name | Search URL Encoded Spaces |
| Area / Page | Routing/Search |
| Priority | P4 |
| Tags | routing, search |

**Preconditions / Test Data**
Two URL variants for the same logical query (use site base URL + path).

**Steps to Reproduce**
1. Build full URL A: `{BASE}/s?k=wireless+mouse` (plus encoding for space).
2. `page.goto(url_a)` and wait for `domcontentloaded`.
3. Verify the main results container is visible (`expect(results).to_be_visible()`).
4. Build full URL B: `{BASE}/s?k=wireless%20mouse`.
5. `page.goto(url_b)` and wait for load.
6. Assert results are still shown and the effective search term is `wireless mouse` (search box value or H1).

**Expected Result**
Both common space encodings load search results correctly without error.

**Playwright (Python) APIs**
`page.goto()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk — ensure `BASE_URL` includes correct domain.

---

### AMZ-0188 -- DONE

**Search: no-JS fallback basic navigation works (disable JS)**

| Field | Value |
|-------|-------|
| Short Name | Search Fallback Basic Navigation |
| Area / Page | Search Results |
| Priority | P5 |
| Tags | negative, robustness |

**Preconditions / Test Data**
Controlled environment; use a dedicated browser context with JavaScript disabled.

**Steps to Reproduce**
1. Create `browser.new_context(java_script_enabled=False)`.
2. Open a new page in that context.
3. Navigate to a search URL e.g. `/s?k=ssd` (`page.goto()`).
4. Verify **something** sensible renders: static HTML product list, message about enabling JavaScript, or category links — use `expect(page.locator('body')).to_contain_text(...)` with allowed patterns.
5. Do not assume full parity with JS-on experience.

**Expected Result**
Without JS, the site fails in a defined, non-destructive way (content or explicit notice), not a blank error page.

**Playwright (Python) APIs**
`browser.new_context(java_script_enabled=False)`, `page.goto()`, `expect(locator).to_be_visible()`

**Automation Notes**
Low priority exploratory; Amazon may block or heavily degrade without JS.

---

### AMZ-0189 -- DONE

**Search: ensure no mixed-content warnings in console**

| Field | Value |
|-------|-------|
| Short Name | Search Mixed Content Warnings |
| Area / Page | Search Results |
| Priority | P4 |
| Tags | security, console |

**Preconditions / Test Data**
Search query: `ssd`

**Steps to Reproduce**
1. Attach `page.on('console', handler)` to collect `msg.type == 'error'` and text.
2. Optionally attach `page.on('pageerror', handler)` for uncaught exceptions.
3. Navigate to homepage then search for `ssd` (or `goto` SERP directly).
4. Wait for results to settle.
5. Filter collected messages for **mixed content** wording (`mixed-content`, `insecure`, `HTTP content on HTTPS`).
6. Assert none match (`assert not mixed_content_errors`).

**Expected Result**
No mixed-content security errors appear in the console during the search flow.

**Playwright (Python) APIs**
`page.on('console'), page.goto(), expect()`

**Automation Notes**
Medium risk — third-party ads may add noise; filter carefully.

---

### AMZ-0190 -- DONE

**Search: filter state remains after opening a result in same tab and returning**

| Field | Value |
|-------|-------|
| Short Name | Search Filter State Remains |
| Area / Page | Search Results |
| Priority | P3 |
| Tags | state, filters |

**Preconditions / Test Data**
Search query: `pillow`

**Steps to Reproduce**
1. Search for `pillow`.
2. Apply **one** durable filter (e.g. brand or Prime) and confirm chip + URL.
3. Click the first product title to open PDP **in the same tab** (`locator.click()`).
4. Wait for PDP load.
5. Use browser **Back** (`page.go_back()`).
6. Wait for SERP to load again.
7. Verify the same filter chip(s) are still present and URL still contains facet params (`expect(chip).to_be_visible()`).

**Expected Result**
History navigation restores the filtered SERP, not a clean search.

**Playwright (Python) APIs**
`page.go_back()`, `expect(locator).to_be_visible()`

**Automation Notes**
High risk — bfcache and SPA behavior can differ.

---

*End of Filters / Search Test Cases*
