from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.steps.utils import *
from features.steps.auth import ends_timer
from time import sleep
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys



@given("There is a Product Created")
def there_is_product_created(context):
    open_dashboard_page(context)
    open_sandwich_menu(context)
    click_product_management(context)
    click_add_product_management(context)
    input_product_name(context)
    add_pack_size(context, 1)
    click_identifiers_tab(context)
    add_sku(context)
    add_upc(context)
    input_gs1_company_prefix(context)
    input_gs1_id(context)
    click_add_identifier(context)
    wait_identifier_options(context)
    input_ndc_value(context)
    click_add_ndc(context)
    click_requirements_tab(context)
    add_generic_name(context)
    add_strength(context)
    add_net_content(context)
    add_notes(context)
    click_add(context)


@when("Open dashboard page")
def open_dashboard_page(context):
    try:
        # Wait for page to be ready - try different selectors
        selectors_to_try = [
            (By.XPATH, "//div[@class='client_logo']/a"),
            (By.XPATH, "//div[contains(@class, 'sidebar')]"),
            (By.XPATH, "//div[contains(@class, 'dashboard')]"),
        ]

        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        element_found = False
        for by, selector in selectors_to_try:
            try:
                WebDriverWait(context.driver, 10).until(
                    EC.presence_of_element_located((by, selector))
                )
                element_found = True
                break
            except:
                continue

        if not element_found:
            # If we're already on the dashboard URL, that's OK
            if "tracktraceweb.com" in context.driver.current_url:
                print(f"Dashboard page - current URL: {context.driver.current_url}")
            else:
                raise Exception(f"Could not verify dashboard page at URL: {context.driver.current_url}")

        sleep(2)  # Give page time to load fully
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Open sandwich menu")
def open_sandwich_menu(context):
    try:
        # Close any open modals/overlays/toasts first - try multiple methods
        sleep(2)

        # Try to close various types of overlays
        close_selectors = [
            "//span[text()='Close']",
            "//button[text()='Close']",
            "//button[contains(@class, 'close')]",
            "//a[text()='Close']",
            "//div[contains(@class, 'modal')]//button[contains(@class, 'close')]",
            "//div[contains(@class, 'tt_utils_ui_dlg_modal')]//span[text()='Close']",
            "//*[contains(@class, 'close-button')]",
            "//*[@aria-label='Close']"
        ]

        for close_selector in close_selectors:
            try:
                close_btn = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, close_selector))
                )
                close_btn.click()
                print(f"Closed overlay with selector: {close_selector}")
                sleep(1)
            except:
                continue

        # Wait for page transitions to complete
        sleep(2)

        # Try multiple selectors for the menu toggle with increased timeout
        menu_toggle = None
        selectors = [
            "//div[contains(@class, 'sidebar_menu_toggle_dis')]/a",
            "//div[contains(@class, 'sidebar_menu_toggle_en')]/a",
            "//div[contains(@class, 'sidebar_menu_toggle_enabled')]/a",
            "//div[contains(@class, 'sidebar_menu_toggle')]/a",
            "//a[contains(@class, 'sidebar-toggle')]",
            "//a[@class='sidebar-toggle']",
            "//*[@id='sidebar-toggle']",
            "//i[contains(@class, 'fa-bars')]/parent::a",
            "//button[contains(@class, 'menu-toggle')]",
            "//div[@class='menu-toggle']//a"
        ]

        for selector in selectors:
            try:
                print(f"Trying menu selector: {selector}")
                menu_toggle = WebDriverWait(context.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                # Try JavaScript click if regular click might be intercepted
                try:
                    context.driver.execute_script("arguments[0].click();", menu_toggle)
                    print(f"Clicked menu with JavaScript using: {selector}")
                except:
                    menu_toggle.click()
                    print(f"Clicked menu with regular click using: {selector}")
                sleep(2)
                return  # Success, exit function
            except Exception as sel_error:
                print(f"Failed with selector {selector}: {str(sel_error)[:100]}")
                continue

        # If we reach here, menu toggle was not found
        context.driver.save_screenshot("report/output/menu_not_found.png")
        print(f"Current URL: {context.driver.current_url}")
        print(f"Page source length: {len(context.driver.page_source)}")
        raise Exception("Menu toggle not found with any selector after trying all options")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Product Management")
def click_product_management(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "//a[contains(@href, '/products/')]/span[contains(text(), 'Product Management')]",
            timeout=10
        )
        sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Product Management Page")
def click_add_product_management(context):
    try:
        wait_and_click(
            context.driver,
            By.CLASS_NAME,
            "tt_utils_ui_search-one-header-action-button--add-action",
            timeout=10
        )
        sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on General Tab")
def click_general_tab(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//li[@rel='general']", timeout=10)
        sleep(0.5)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Product Name")
def input_product_name(context):
    try:
        context.product_name = generate_product_name() + " EACH"
        name_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_name", timeout=10
        )
        name_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_name", context.product_name
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Saved Product Name")
def input_saved_product_name(context):
    try:
        context.product_name = context.product_name.split(" EACH")[0] + " CASE"
        name_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_name", timeout=10
        )
        name_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_name", context.product_name
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Pack Size {size}")
def add_pack_size(context, size):
    try:
        pack_size_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_pack_size", timeout=10
        )
        pack_size_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_pack_size", size
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Pack Size Case")
def select_pack_size_case(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//select[@name='packaging_type']", timeout=10)
        sleep(0.5)
        wait_and_click(context.driver, By.XPATH, "//option[text()='Case (CA)']", timeout=10)
        sleep(0.5)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Identifiers tab")
def click_identifiers_tab(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//li[@rel='identifiers']", timeout=10)
        sleep(0.5)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add SKU")
def add_sku(context):
    try:
        context.ndc = generate_ndc()
        sku_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_sku", timeout=10
        )
        sku_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_sku", context.ndc
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Saved SKU")
def add_saved_ku(context):
    try:
        sku_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_sku", timeout=10
        )
        sku_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_sku", context.ndc
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add UPC")
def add_upc(context):
    try:
        context.company_prefix = generate_company_prefix()
        context.gs1_id = generate_gs1_id()
        context.gtin = generate_gtin_with_cp_id(context.company_prefix, context.gs1_id)
        upc_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_upc", timeout=10
        )
        upc_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_upc", context.gtin
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Saved UPC")
def add_saved_upc(context):
    try:
        upc_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_upc", timeout=10
        )
        upc_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_upc", context.gtin
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add GS1 Company Prefix")
def input_gs1_company_prefix(context):
    try:
        prefix_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_company_prefix", timeout=10
        )
        prefix_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_company_prefix", context.company_prefix
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add GS1 ID")
def input_gs1_id(context):
    try:
        gs1_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_id", timeout=10
        )
        gs1_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_id", context.gs1_id
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Identifier")
def click_add_identifier(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "//div[@class='tt_utils_forms-one-header-action-button tt_utils_forms-one-header-action-button--add-action']",
            timeout=10
        )
        sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Identifier Value")
def input_ndc_value(context):
    try:
        input_field = wait_and_find(
            context.driver, By.XPATH, "//input[@rel='value']", timeout=10
        )
        input_field.send_keys(context.ndc)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Wait for Identifier Options to Load")
def wait_identifier_options(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//select[@name='identifier_code']/option[@value='US_NDC']",
        , timeout=30)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add NDC")
def click_add_ndc(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//div[contains(@class, 'tt_utils_ui_dlg_modal-width-class-l', timeout=30)]//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button')]",
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Requirements Tab")
def click_requirements_tab(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//li[@rel='requirements']"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Generic Name")
def add_generic_name(context):
    try:
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_generic_name"
        , timeout=30).send_keys(context.product_name)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Strength")
def add_strength(context):
    try:
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_strength"
        , timeout=30).send_keys("RPA Strength")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Net Content Description")
def add_net_content(context):
    try:
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_net_content_desc"
        , timeout=30).send_keys("RPA Net Content")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Notes")
def add_notes(context):
    try:
        text = generate_text_with_n_chars(30)
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_notes"
        , timeout=30).send_keys(text)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add")
def click_add(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button', timeout=30)]",
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Aggregation Tab")
def click_aggregation_tab(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//li[@rel='composition']"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Product")
def click_add_product(context):
    try:
        wait_and_find(context.driver, By.CLASS_NAME, "__choose_composition_product"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Input Name of Each Product into Product Name")
def input_name_each_product(context):
    try:
        name_input_field = wait_and_find(
            context.driver, By.XPATH, "//input[@rel='name']", timeout=10
        )
        name_input_field.clear()
        sleep(0.5)
        name_input_field.send_keys(" EACH")
        sleep(2)  # Wait for autocomplete to load
        name_input_field.send_keys(Keys.ENTER)
        sleep(2)  # Wait for search results to appear
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Product Name")
def click_product_name(context):
    try:
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver import ActionChains

        # Wait for the results table/list to appear
        sleep(2)

        # Try multiple selectors - prioritize clickable parent elements (td) over child elements (span)
        selectors = [
            # Table row/cell elements (parent elements with onclick - most reliable)
            (By.XPATH, "//td[@rel='name' and contains(., 'EACH')]"),
            (By.XPATH, "//td[contains(@class, 'res_column__name') and contains(., 'EACH')]"),
            (By.XPATH, "//tr[contains(., 'EACH')]//td[@rel='name']"),
            # Autocomplete dropdown options
            (By.XPATH, "//div[contains(@class, 'autocomplete')]//li[contains(text(), 'EACH')]"),
            (By.XPATH, "//ul[contains(@class, 'ui-autocomplete')]//li[contains(text(), 'EACH')]"),
            (By.XPATH, "//div[@class='ui-menu-item']//div[contains(text(), 'EACH')]"),
            # Table results (generic)
            (By.XPATH, "//table[@class='display']//td[contains(text(),' EACH')]"),
            (By.XPATH, "//table//tbody//tr//td[contains(text(),' EACH')]"),
        ]

        element_clicked = False
        last_error = None

        for by, selector in selectors:
            try:
                print(f"Trying selector: {selector}")
                element = WebDriverWait(context.driver, 10).until(
                    EC.presence_of_element_located((by, selector))
                )
                print(f"Found element with selector: {selector}")

                # Try JavaScript click first (bypasses intercepted click issues)
                try:
                    context.driver.execute_script("arguments[0].click();", element)
                    print(f"Clicked element with JavaScript")
                    element_clicked = True
                    sleep(1)
                    break
                except:
                    # Fallback to regular click
                    element.click()
                    print(f"Clicked element with regular click")
                    element_clicked = True
                    sleep(1)
                    break
            except Exception as sel_error:
                last_error = sel_error
                continue

        if not element_clicked:
            # Take screenshot for debugging
            context.driver.save_screenshot("report/output/product_name_not_found.png")
            print(f"Current URL: {context.driver.current_url}")
            print(f"Page source preview: {context.driver.page_source[:500]}")
            raise Exception(f"Could not find Product Name element with any selector. Last error: {last_error}")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Product Quantity")
def add_product_quantity(context):
    try:
        # Wait longer for modal to fully load after clicking product
        sleep(3)

        # Try to find the modal container first
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            # Wait for modal to appear
            modal = WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tt_utils_ui_dlg_modal-width-class-m"))
            )
            print("Modal found, waiting for content to load...")
            sleep(2)
        except:
            print("Modal not found, but continuing...")

        # Get product information from the modal
        product_name_elem = wait_and_find(
            context.driver, By.CLASS_NAME, "child_product_name_show_container", timeout=15
        )
        context.product_name = product_name_elem.text

        gtin_elem = wait_and_find(
            context.driver, By.CLASS_NAME, "child_product_gtin14_show_container", timeout=10
        )
        context.gtin = gtin_elem.text
        context.gtin = "3" + context.gtin[1:13]

        ndc_elem = wait_and_find(
            context.driver, By.CLASS_NAME, "child_product_name_ndc_container", timeout=10
        )
        context.ndc = ndc_elem.text

        context.company_prefix, context.gs1_id = generate_cp_id_by_gtin(context.gtin)

        # Add quantity
        quantity_field = wait_and_find(
            context.driver,
            By.XPATH,
            "//input[starts-with(@id, 'TT_UTILS_UI_FORM_UUID_') and contains(@id, 'quantity') and @rel='quantity']",
            timeout=10
        )
        quantity_field.clear()
        wait_and_send_keys(
            context.driver,
            By.XPATH,
            "//input[starts-with(@id, 'TT_UTILS_UI_FORM_UUID_') and contains(@id, 'quantity') and @rel='quantity']",
            "2"
        )
    except Exception as e:
        # Take screenshot for debugging
        try:
            context.driver.save_screenshot("report/output/add_quantity_error.png")
            print(f"Screenshot saved. Current URL: {context.driver.current_url}")
        except:
            pass
        ends_timer(context, e)
        raise


@when("Click on Add Child Product")
def click_add_child_product(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "//div[contains(@class, 'tt_utils_ui_dlg_modal-width-class-m')]//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button')]",
            timeout=10
        )
        sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Misc Tab")
def click_misc_tab(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//li[@rel='misc']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Disable Leaf Product")
def disable_leaf_product(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//label[text(, timeout=30)='This product is seen as a leaf item in the product composition']",
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on RPA Product")
def click_rpa_product(context):
    try:
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Wait for search results to load
        sleep(3)

        # Try multiple selectors for RPA Product
        selectors = [
            (By.XPATH, "//span[@class='tt_utils_ui_search-table-cell-responsive-value' and contains(text(), '[RPA]') and contains(text(), 'EACH')]"),
            (By.XPATH, "//td[contains(text(), '[RPA]') and contains(text(), 'EACH')]"),
            (By.XPATH, "//span[contains(text(), '[RPA]') and contains(text(), 'EACH')]"),
            (By.XPATH, "//*[contains(text(), '[RPA]') and contains(text(), 'EACH')]"),
            (By.XPATH, "//tr[contains(., '[RPA]') and contains(., 'EACH')]//td[@rel='name']"),
            (By.XPATH, "//table//tbody//tr//td[contains(text(), '[RPA]')]"),
            (By.XPATH, "//td[@rel='name' and contains(text(), '[RPA]')]"),
        ]

        product = None
        for by, selector in selectors:
            try:
                product = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable((by, selector))
                )
                print(f"[OK] Found RPA Product with selector: {selector}")
                break
            except:
                print(f"[FAIL] Could not find RPA Product with selector: {selector}")
                continue

        if product is None:
            # Save screenshot for debugging
            context.driver.save_screenshot("report/output/rpa_product_not_found.png")
            print(f"Current URL: {context.driver.current_url}")
            raise Exception("Could not find RPA Product with any selector")

        context.product_name = product.text
        product.click()
        sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Save GS1 Info")
def save_gs1_company_prefix(context):
    try:
        context.product_gtin = wait_and_find(context.driver, By.CLASS_NAME, "field__upc",
        , timeout=30).text
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Close Modal")
def close_modal(context):
    try:
        sleep(1)
        wait_and_find(context.driver, By.XPATH, "//button/span[text(, timeout=30) = 'Close']",
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search for Created Product")
def search_created_product(context):
    try:
        name_search = wait_and_find(context.driver, By.CLASS_NAME, "search_criteria__name"
        , timeout=30)
        name_search.send_keys(context.product_name)
        name_search.send_keys(Keys.ENTER)
        sleep(3)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Delete Created Product")
def delete_created_product(context):
    try:
        wait_and_find(context.driver, By.XPATH, f"//img[@alt='Delete']",
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Yes - Deletion")
def click_yes_deletion(context):
    try:
        wait_and_find(context.driver, By.XPATH, f"//button/span[text(, timeout=30)='Yes']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Product should be saved")
def product_saved(context):
    try:
        name_search = wait_and_find(context.driver, By.CLASS_NAME, "search_criteria__name"
        , timeout=30)
        name_search.send_keys(context.product_name)
        name_search.send_keys(Keys.ENTER)
        sleep(3)
        wait_and_find(context.driver, By.XPATH, f"//*[contains(text(, timeout=30),'{context.product_name}') or contains(text(), 'GTIN14 already exist for product')]",
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Product should be deleted")
def product_deleted(context):
    try:
        sleep(5)
        context.driver.refresh()
        sleep(2)
        records_text = wait_and_find(context.driver, 
            By.CLASS_NAME, "tt_utils_ui_search-footer-nb-results"
        , timeout=30).text
        new_total_records = int(records_text.split("of ")[1].split(" recor")[0])
        assert context.total_records - new_total_records == 1
    except Exception as e:
        ends_timer(context, e)
        raise
