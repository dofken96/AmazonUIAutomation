# Amazon UI — Smoke Test Cases

**Source:** `amazon_playwright_test_matrix.xlsx` → sheet `Test_Cases` → group `Smoke`
**Total:** 20 test cases | **Generated:** 2026-04-09

---

## Table of Contents

| ID | Title | Area | Priority |
|----|-------|------|----------|
| [AMZ-0001](#amz-0001) | Homepage loads and key header components visible | Home | P0 |
| [AMZ-0002](#amz-0002) | Search from header returns results page | Home → Search Results | P0 |
| [AMZ-0003](#amz-0003) | Open a product from search results | Search Results → PDP | P0 |
| [AMZ-0004](#amz-0004) | Add product to cart (from PDP) | PDP → Cart | P0 |
| [AMZ-0005](#amz-0005) | Open cart page | Header → Cart | P0 |
| [AMZ-0006](#amz-0006) | Proceed to checkout entry point | Cart → Checkout | P0 |
| [AMZ-0007](#amz-0007) | Navigate to Today's Deals from top nav | Home → Deals | P1 |
| [AMZ-0008](#amz-0008) | Open hamburger menu and verify departments list | Home | P1 |
| [AMZ-0009](#amz-0009) | Footer links section visible and at least one policy link works | Home → Footer | P2 |
| [AMZ-0010](#amz-0010) | Basic responsive check: mobile viewport shows mobile header | Home (Mobile) | P1 |
| [AMZ-0011](#amz-0011) | Language/Region selector entry opens | Home | P2 |
| [AMZ-0012](#amz-0012) | Search suggestions dropdown appears | Home | P2 |
| [AMZ-0013](#amz-0013) | Open sign-in page via Account & Lists | Home → Sign-in | P1 |
| [AMZ-0014](#amz-0014) | Search results sorting control is visible | Search Results | P2 |
| [AMZ-0015](#amz-0015) | Product image gallery is present on PDP | PDP | P2 |
| [AMZ-0016](#amz-0016) | Cart quantity dropdown is present for cart items | Cart | P2 |
| [AMZ-0017](#amz-0017) | Search results pagination/next control exists | Search Results | P3 |
| [AMZ-0018](#amz-0018) | Open customer service/help page from nav | Home → Help | P2 |
| [AMZ-0019](#amz-0019) | Open Gift Cards page from nav | Home → Gift Cards | P3 |
| [AMZ-0020](#amz-0020) | No severe console errors on homepage load | Home | P3 |

---

## Test Cases

---

### AMZ-0001 -- DONE

**Homepage loads and key header components visible**

| Field | Value |
|-------|-------|
| Short Name | Homepage Key Header Components |
| Area / Page | Home |
| Priority | P0 |
| Tags | home, header, critical-path |

**Preconditions / Test Data**
None.

**Steps to Reproduce**
1. Navigate to the Amazon homepage (`page.goto()`).
2. Wait for the DOM content to finish loading (`page.wait_for_load_state('domcontentloaded')`).
3. Verify the search box is visible in the header (`expect(locator).to_be_visible()`).
4. Verify the cart link/icon is visible in the header.
5. Verify the hamburger / "All" menu button is visible.

**Expected Result**
The homepage loads successfully. The search box, cart icon, and hamburger menu are all present and visible in the header.

**Playwright (Python) APIs**
`page.goto()`, `page.wait_for_load_state()`, `page.get_by_role()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk — site may display bot/captcha challenge that blocks page load.

---

### AMZ-0002 -- DONE

**Search from header returns results page**

| Field | Value |
|-------|-------|
| Short Name | Search Header Returns Results |
| Area / Page | Home → Search Results |
| Priority | P0 |
| Tags | search, navigation |

**Preconditions / Test Data**
Search term: `wireless mouse`

**Steps to Reproduce**
1. Open the Amazon homepage (`page.goto()`).
2. Locate the search input in the header (`page.get_by_role('searchbox')`).
3. Type the search query into the search box (`locator.fill('wireless mouse')`).
4. Submit the search by pressing Enter (`locator.press('Enter')`).
5. Verify the results container is visible on the page (`expect(locator).to_be_visible()`).
6. Verify the URL changes to a search results path containing the query (`expect(page).to_have_url(re.compile(r'.*s\?k=wireless.*'))`).

**Expected Result**
The search results page opens. The results list is visible and the URL reflects the submitted query.

**Playwright (Python) APIs**
`page.goto()`, `page.get_by_role()`, `locator.fill()`, `locator.press()`, `expect(page).to_have_url()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0003 -- DONE

**Open a product from search results**

| Field | Value |
|-------|-------|
| Short Name | Product Search Results |
| Area / Page | Search Results → PDP |
| Priority | P0 |
| Tags | pdp, navigation |

**Preconditions / Test Data**
Search term: `wireless mouse`

**Steps to Reproduce**
1. Open the Amazon homepage and perform a search for `wireless mouse` (steps from AMZ-0002).
2. Wait for the search results page to fully load (`page.wait_for_load_state()`).
3. Locate the first product title or product image link in the results list (`page.locator(...).first`).
4. Click the first product (`locator.click()`).
5. Wait for the Product Detail Page (PDP) to load.
6. Verify the product title element is visible on the PDP (`expect(locator).to_be_visible()`).

**Expected Result**
The Product Detail Page (PDP) opens. The product title section is displayed and not empty.

**Playwright (Python) APIs**
`page.get_by_role()`, `page.locator()`, `locator.first`, `locator.click()`, `expect(locator).to_be_visible()`, `page.wait_for_load_state()`

**Automation Notes**
Medium risk.

---

### AMZ-0004 -- DONE

**Add product to cart (from PDP)**

| Field | Value |
|-------|-------|
| Short Name | Add Product Cart PDP |
| Area / Page | PDP → Cart |
| Priority | P0 |
| Tags | cart, add-to-cart |

**Preconditions / Test Data**
Use a product known to be in stock. If the product is Out of Stock (OOS), skip the test.

**Steps to Reproduce**
1. Open a Product Detail Page (PDP) — either navigate directly or via search.
2. If the product requires a variant selection (e.g., size, color), select a valid default variant.
3. Locate the "Add to Cart" button (`page.get_by_role('button', name='Add to Cart')`).
4. Click "Add to Cart" (`locator.click()`).
5. Wait for the page or mini-cart to respond (`page.wait_for_load_state()`).
6. Verify that a cart confirmation message or mini-cart overlay is visible **OR** that the cart count in the header increases (`expect(locator).to_be_visible()`).

**Expected Result**
The item is added to the cart. A confirmation message or mini-cart UI appears, or the cart item count in the header updates to reflect the addition.

**Playwright (Python) APIs**
`page.get_by_role()`, `page.locator()`, `locator.click()`, `expect(locator).to_be_visible()`, `page.wait_for_load_state()`

**Automation Notes**
High risk — variant selection and product availability can vary; "Add to Cart" button may not be present for all products.

---

### AMZ-0005 -- DONE

**Open cart page**

| Field | Value |
|-------|-------|
| Short Name | Cart Header |
| Area / Page | Header → Cart |
| Priority | P0 |
| Tags | cart, navigation |

**Preconditions / Test Data**
At least one item must be in the cart (fulfilled by a prior test, e.g., AMZ-0004, or added during setup).

**Steps to Reproduce**
1. From any Amazon page, locate the cart icon/link in the header (`page.get_by_role('link', name=re.compile(r'Cart'))`).
2. Click the cart icon (`locator.click()`).
3. Verify the page URL changes to the cart path (e.g., `/cart`) (`expect(page).to_have_url()`).
4. Verify the cart page title ("Shopping Cart") is visible (`expect(locator).to_be_visible()`).
5. Verify the list of cart items is visible on the page.

**Expected Result**
The Cart page opens and displays the list of items that were previously added.

**Playwright (Python) APIs**
`page.get_by_role()`, `locator.click()`, `expect(page).to_have_url()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0006 -- DONE (XFAIL)

**Proceed to checkout entry point**

| Field | Value |
|-------|-------|
| Short Name | Proceed Checkout Entry Point |
| Area / Page | Cart → Checkout |
| Priority | P0 |
| Tags | checkout, auth, routing |

**Preconditions / Test Data**
- **Logged-out user:** expects redirection to sign-in page.
- **Logged-in user:** expects redirection to the first checkout step.
- At least one item must be in the cart.

**Steps to Reproduce**
1. Open the cart page (navigate to `/cart` or click cart icon in header).
2. Verify at least one item is present in the cart.
3. Locate the "Proceed to checkout" button (`page.get_by_role('button', name=re.compile(r'Proceed to checkout', re.IGNORECASE))`).
4. Click "Proceed to checkout" (`locator.click()`).
5. Wait for navigation to complete (`page.wait_for_url()`).
6. Assert the resulting URL is either the sign-in page (logged-out flow) or a checkout step page (logged-in flow) (`expect(page).to_have_url()`).

**Expected Result**
The user is routed to the sign-in page (if logged out) or to the first step of the checkout flow (if logged in).

**Playwright (Python) APIs**
`page.get_by_role()`, `locator.click()`, `page.wait_for_url()`, `expect(page).to_have_url()`

**Automation Notes**
High risk — authentication state and bot-protection mechanisms can affect routing behaviour.

---

### AMZ-0007 -- DONE

**Navigate to Today's Deals from top nav**

| Field | Value |
|-------|-------|
| Short Name | Navigate Today Deals Top |
| Area / Page | Home → Deals |
| Priority | P1 |
| Tags | nav, deals |

**Preconditions / Test Data**
None.

**Steps to Reproduce**
1. Open the Amazon homepage (`page.goto()`).
2. Locate the "Today's Deals" link in the top navigation bar (`page.get_by_role('link', name="Today's Deals")`).
3. Click the link (`locator.click()`).
4. Wait for the Deals page to load (`page.wait_for_load_state()`).
5. Verify the deals container/list is visible on the page (`expect(locator).to_be_visible()`).

**Expected Result**
The Today's Deals page opens. A deals container with deal items is present and visible.

**Playwright (Python) APIs**
`page.get_by_role()`, `locator.click()`, `page.wait_for_load_state()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0008 -- DONE

**Open hamburger menu and verify departments list**

| Field | Value |
|-------|-------|
| Short Name | Hamburger Menu Departments List |
| Area / Page | Home |
| Priority | P1 |
| Tags | menu, navigation |

**Preconditions / Test Data**
None.

**Steps to Reproduce**
1. Open the Amazon homepage (`page.goto()`).
2. Locate the hamburger / "All" menu button in the header (`page.get_by_role('button', name='All')`  or equivalent locator).
3. Click the hamburger/All button to open the side navigation panel (`locator.click()`).
4. Verify the left/side navigation panel appears and is visible (`expect(locator).to_be_visible()`).
5. Verify the navigation panel contains department links (e.g., "Electronics", "Books", "Fashion").

**Expected Result**
The side navigation panel opens and displays a list of department links.

**Playwright (Python) APIs**
`page.get_by_role()`, `locator.click()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0009 -- DONE

**Footer links section visible and at least one policy link works**

| Field | Value |
|-------|-------|
| Short Name | Footer Links Section Visible |
| Area / Page | Home → Footer |
| Priority | P2 |
| Tags | footer, navigation |

**Preconditions / Test Data**
None.

**Steps to Reproduce**
1. Open the Amazon homepage (`page.goto()`).
2. Scroll to the bottom of the page to bring the footer into view (`page.mouse.wheel(0, 10000)`).
3. Verify the footer element is visible (`expect(locator).to_be_visible()`).
4. Locate a stable policy link in the footer, e.g., "Conditions of Use" (`page.get_by_role('link', name='Conditions of Use')`).
5. Click the policy link (`locator.click()`).
6. Wait for the target page to load (`page.wait_for_load_state()`).
7. Verify the URL has changed to the policy page (`expect(page).to_have_url()`).

**Expected Result**
The footer renders correctly. Clicking a policy link navigates to the corresponding page without error.

**Playwright (Python) APIs**
`page.goto()`, `page.mouse.wheel()`, `page.get_by_role()`, `locator.click()`, `expect(page).to_have_url()`, `page.wait_for_load_state()`

**Automation Notes**
Medium risk.

---

### AMZ-0010 -- DONE

**Basic responsive check: mobile viewport shows mobile header**

| Field | Value |
|-------|-------|
| Short Name | Basic Responsive Mobile Viewport |
| Area / Page | Home (Mobile viewport) |
| Priority | P1 |
| Tags | responsive, mobile |

**Preconditions / Test Data**
Viewport dimensions: **390 × 844** (iPhone 14 equivalent).

**Steps to Reproduce**
1. Create a new browser context with a mobile viewport set to 390 × 844 (`browser.new_context(viewport={'width': 390, 'height': 844})`).
2. Open a new page from the context and navigate to the Amazon homepage (`page.goto()`).
3. Verify the mobile search input is visible (`expect(locator).to_be_visible()`).
4. Verify the mobile menu/hamburger button is visible.
5. Verify the cart icon is accessible on the mobile header.

**Expected Result**
The mobile layout renders correctly. The search input, menu button, and cart icon are all visible and accessible at the 390 × 844 viewport.

**Playwright (Python) APIs**
`browser.new_context(viewport={...})`, `page.goto()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0011 -- DONE

**Language/Region selector entry opens**

| Field | Value |
|-------|-------|
| Short Name | Language Region Selector Entry |
| Area / Page | Home |
| Priority | P2 |
| Tags | locale, modal |

**Preconditions / Test Data**
None.

**Steps to Reproduce**
1. Open the Amazon homepage (`page.goto()`).
2. Locate the language/region selector in the header (flag icon or globe icon with language text) (`page.get_by_role('link', name=re.compile(r'EN', re.IGNORECASE))` or equivalent).
3. Click the selector entry (`locator.click()`).
4. Verify the language/region selection popover or modal dialog appears and is visible (`expect(locator).to_be_visible()`).

**Expected Result**
The language/region selection UI (popover or modal) appears after clicking the selector.

**Playwright (Python) APIs**
`page.get_by_role()`, `locator.click()`, `expect(locator).to_be_visible()`

**Automation Notes**
High risk — this UI varies significantly by geographic region and may not be present in all locales.

---

### AMZ-0012 -- DONE

**Search suggestions dropdown appears**

| Field | Value |
|-------|-------|
| Short Name | Search Suggestions Dropdown Appears |
| Area / Page | Home |
| Priority | P2 |
| Tags | typeahead, search |

**Preconditions / Test Data**
Search term (partial): `iph` (first 3 characters of "iphone")

**Steps to Reproduce**
1. Open the Amazon homepage (`page.goto()`).
2. Click on the search input to focus it (`locator.click()`).
3. Type the first 3 letters of the search term, e.g., `iph` (`locator.type('iph')` with a slight delay between keystrokes to allow the typeahead to fire).
4. Wait briefly for the suggestion dropdown to populate.
5. Verify the autocomplete/suggestion dropdown list is visible below the search box (`expect(locator).to_be_visible()`).

**Expected Result**
A typeahead suggestions dropdown appears beneath the search box, showing search suggestions related to the typed characters.

**Playwright (Python) APIs**
`page.get_by_role()`, `locator.click()`, `locator.type()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0013 -- DONE

**Open sign-in page via Account & Lists**

| Field | Value |
|-------|-------|
| Short Name | Sign Account Lists |
| Area / Page | Home → Sign-in |
| Priority | P1 |
| Tags | auth, navigation |

**Preconditions / Test Data**
Session must be in a **logged-out** state.

**Steps to Reproduce**
1. Open the Amazon homepage in a logged-out session (`page.goto()`).
2. Hover over the "Account & Lists" entry in the header to reveal the dropdown (`locator.hover()`).
3. Click the "Sign in" link within the dropdown (`locator.click()`).
4. Wait for the sign-in page to load.
5. Verify the sign-in form (email/phone input field) is visible (`expect(locator).to_be_visible()`).
6. Verify the page URL includes a sign-in path (`expect(page).to_have_url(re.compile(r'.*signin.*'))`).

**Expected Result**
The Amazon sign-in page loads. The email/phone input form is displayed and the URL reflects the sign-in endpoint.

**Playwright (Python) APIs**
`page.get_by_role()`, `locator.hover()`, `locator.click()`, `expect(locator).to_be_visible()`, `expect(page).to_have_url()`

**Automation Notes**
High risk — bot/captcha protection is frequently triggered on the sign-in page.

---

### AMZ-0014 -- DONE

**Search results sorting control is visible**

| Field | Value |
|-------|-------|
| Short Name | Search Results Sorting Control |
| Area / Page | Search Results |
| Priority | P2 |
| Tags | search, sort |

**Preconditions / Test Data**
Search query: `headphones`

**Steps to Reproduce**
1. Open the Amazon homepage and perform a search for `headphones` (via search box, steps from AMZ-0002).
2. Wait for the search results page to load.
3. Locate the sort dropdown or sort control on the results page (e.g., "Sort by: Featured" dropdown) (`page.get_by_role('combobox')` or `page.locator('[id*="sort"]')`).
4. Verify the sort control is visible (`expect(locator).to_be_visible()`).

**Expected Result**
The sort control (dropdown or button group) is present and visible on the search results page.

**Playwright (Python) APIs**
`page.get_by_role()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0015 -- DONE

**Product image gallery is present on PDP**

| Field | Value |
|-------|-------|
| Short Name | Product Image Gallery Present |
| Area / Page | PDP |
| Priority | P2 |
| Tags | pdp, gallery |

**Preconditions / Test Data**
Any PDP URL — can be reached via search (AMZ-0003) or a direct product URL.

**Steps to Reproduce**
1. Open a Product Detail Page (PDP) by navigating directly or via search and clicking a product.
2. Wait for the page to fully load.
3. Verify the main (hero) product image is visible (`page.locator('#landingImage')` or equivalent, `expect(locator).to_be_visible()`).
4. Verify that image thumbnails or an image carousel element is present in the DOM and visible.
5. (Optional) Click a thumbnail image and verify the main image updates.

**Expected Result**
The main product image renders on the PDP. Image thumbnails or a carousel is visible and interactable.

**Playwright (Python) APIs**
`page.locator()`, `expect(locator).to_be_visible()`, `locator.click()`

**Automation Notes**
Medium risk.

---

### AMZ-0016

**Cart quantity dropdown is present for cart items**

| Field | Value |
|-------|-------|
| Short Name | Cart Quantity Dropdown Present |
| Area / Page | Cart |
| Priority | P2 |
| Tags | cart, dropdown |

**Preconditions / Test Data**
At least one item must be in the cart.

**Steps to Reproduce**
1. Open the cart page (navigate to `/cart` or click the cart icon).
2. Wait for the page to load and confirm at least one line item is visible.
3. Locate the first cart line item container.
4. Within the first line item, locate the quantity dropdown or quantity control (`page.locator('[name="quantity"]')` or equivalent).
5. Verify the quantity control is visible (`expect(locator).to_be_visible()`).

**Expected Result**
A quantity dropdown or input control is present and visible for the first cart line item.

**Playwright (Python) APIs**
`page.locator()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0017 -- DONE

**Search results pagination/next control exists (if multiple pages)**

| Field | Value |
|-------|-------|
| Short Name | Search Results Pagination Case1 |
| Area / Page | Search Results |
| Priority | P3 |
| Tags | search, pagination |

**Preconditions / Test Data**
Search query: `usb cable` (expected to return many results across multiple pages).

**Steps to Reproduce**
1. Open the Amazon homepage and search for `usb cable`.
2. Wait for the search results page to load.
3. Scroll toward the bottom of the results page (`page.mouse.wheel(0, 10000)`).
4. Locate the pagination control — either a "Next page" button/link or a page-number navigation bar (`page.locator('[class*="pagination"]')` or `page.get_by_role('link', name='Next')`).
5. Verify the next-page control is visible (`expect(locator).to_be_visible()`).

**Expected Result**
A "Next" page button or pagination control is visible at the bottom of the search results, allowing the user to navigate to more results.

**Playwright (Python) APIs**
`page.mouse.wheel()`, `page.locator()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0018 -- DONE

**Open customer service/help page from nav**

| Field | Value |
|-------|-------|
| Short Name | Customer Service Help Nav |
| Area / Page | Home → Help |
| Priority | P2 |
| Tags | help, navigation |

**Preconditions / Test Data**
None.

**Steps to Reproduce**
1. Open the Amazon homepage (`page.goto()`).
2. Locate the "Customer Service" link — either in the top navigation bar or in the footer (`page.get_by_role('link', name='Customer Service')`).
3. Click the "Customer Service" link (`locator.click()`).
4. Wait for the help/customer service page to load (`page.wait_for_load_state()`).
5. Verify the main heading on the help page is visible (`expect(locator).to_be_visible()`).
6. Verify the URL includes a help/customer-service path (`expect(page).to_have_url()`).

**Expected Result**
The Customer Service/Help page opens successfully. The main page heading is visible.

**Playwright (Python) APIs**
`page.get_by_role()`, `locator.click()`, `expect(locator).to_be_visible()`, `expect(page).to_have_url()`

**Automation Notes**
Medium risk.

---

### AMZ-0019 -- DONE

**Open Gift Cards page from nav**

| Field | Value |
|-------|-------|
| Short Name | Gift Cards Nav |
| Area / Page | Home → Gift Cards |
| Priority | P3 |
| Tags | gift-cards, navigation |

**Preconditions / Test Data**
None.

**Steps to Reproduce**
1. Open the Amazon homepage (`page.goto()`).
2. Locate the "Gift Cards" link in the top navigation or within the hamburger/All menu (`page.get_by_role('link', name='Gift Cards')`).
3. Click the "Gift Cards" link (`locator.click()`).
4. Wait for the Gift Cards landing page to load.
5. Verify the Gift Cards landing page main content (heading or card listings) is visible (`expect(locator).to_be_visible()`).

**Expected Result**
The Gift Cards landing page loads. Main content (heading or gift card product grid) is visible.

**Playwright (Python) APIs**
`page.get_by_role()`, `locator.click()`, `expect(locator).to_be_visible()`

**Automation Notes**
Medium risk.

---

### AMZ-0020 -- DONE

**No severe console errors on homepage load (basic)**

| Field | Value |
|-------|-------|
| Short Name | Severe Console Errors Homepage |
| Area / Page | Home |
| Priority | P3 |
| Tags | console, stability |

**Preconditions / Test Data**
None.

**Steps to Reproduce**
1. Attach a console event listener to the page **before** navigation to capture all console messages (`page.on('console', handler)`).
2. Navigate to the Amazon homepage (`page.goto()`).
3. Wait for the page to finish loading (`page.wait_for_load_state('networkidle')` or `'domcontentloaded'`).
4. Collect all captured console entries that have a type of `'error'` or contain keywords such as `SEVERE`, `Uncaught`, or `TypeError`.
5. Filter out known benign warnings (e.g., third-party ad/analytics scripts).
6. Assert that no critical/uncaught JS errors remain in the filtered list (`assert len(severe_errors) == 0`).

**Expected Result**
The homepage loads without any critical or uncaught JavaScript errors. Known benign warnings from third-party scripts are acceptable and should be excluded from the assertion.

**Playwright (Python) APIs**
`page.on('console', ...)`, `page.goto()`, `expect()`

**Automation Notes**
Medium risk — Amazon loads many third-party scripts; filter criteria for "severe" errors must be carefully defined to avoid false positives.

---

*End of Smoke Test Cases*




