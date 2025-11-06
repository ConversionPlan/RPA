from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from features.steps.utils import *
from features.steps.auth import ends_timer
from product import open_dashboard_page, open_sandwich_menu
import time
import os
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys



@given("There is an Inbound done")
def do_inbound(context):
    open_dashboard_page(context)
    open_sandwich_menu(context)
    click_inbound(context)
    click_manual_inbound_shipment(context)
    click_change_location(context)
    search_rpa_location(context)
    select_location(context)
    click_change_seller(context)
    select_type(context)
    search_rpa_seller(context)
    select_seller(context)
    click_yes(context)
    add_po_number(context)
    click_sold_by_tab(context)
    select_sold_by_main_address(context)
    select_ship_from(context)
    click_line_items_tab(context)
    click_add_product_manual_inbound_shipment(context)
    search_rpa_product(context)
    select_rpa_product(context)
    add_quantity(context)
    click_ok_product_selection(context)
    click_add_lot_source(context)
    add_lot_number(context)
    click_serial_based(context)
    add_expiration_date(context)
    click_ok_lot_source(context)
    click_ok_product_information(context)
    click_aggregation_tab(context)
    click_on_add_aggregation(context)
    select_product_radio_button(context)
    choose_product_aggregation(context)
    choose_lot_aggregation(context)
    add_serial_numbers(context)
    click_ok_aggregation(context)
    click_ok_manual_inbound_shipment(context)


@when("Click on Inbound")
def click_inbound(context):
    try:
        inbound_button = wait_and_find(context.driver, By.XPATH, "//a[contains(@href, '/receiving/')]/span[contains(text(), 'Inbound')]",
            timeout=30
        )
        wait = WebDriverWait(context.driver, timeout=20)
        wait.until(lambda d: inbound_button.is_displayed())
        inbound_button.click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Manual Inbound Shipment")
def click_manual_inbound_shipment(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[contains(text(), 'Manual Inbound Shipment')]", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Change Location")
def click_change_location(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//a[contains(text(), 'Change Location')]", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search for an RPA Location")
def search_rpa_location(context):
    try:
        location_name = wait_and_find(context.driver, By.XPATH, "//input[@rel='name']"
        , timeout=30)
        location_name.send_keys("[RPA]")
        location_name.send_keys(Keys.ENTER)
        time.sleep(2)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select a Location")
def select_location(context):
    try:
        time.sleep(1)
        context.inbounded_location = wait_and_find(context.driver, By.XPATH, "//td[@rel='name']"
        , timeout=30).text
        wait_and_find(context.driver, By.XPATH, "//img[@alt='Select']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Change Seller")
def click_change_seller(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//a[contains(text(), 'Change Seller')]", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Type Vendor")
def select_type(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//select[@rel='type']", timeout=30).click()
        wait_and_find(context.driver, By.XPATH, "//option[@value='VENDOR']"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search for an RPA Seller")
def search_rpa_seller(context):
    try:
        vendor_name = wait_and_find(context.driver, By.XPATH, "//input[@rel='name']"
        , timeout=30)
        vendor_name.send_keys("[RPA]")
        vendor_name.send_keys(Keys.ENTER)
        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select a Seller")
def select_seller(context):
    try:
        time.sleep(1)
        seller_name = wait_and_find(context.driver, By.XPATH, "//td[@rel='name']"
        , timeout=30)
        context.tp_name = seller_name.text
        seller_name.click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Yes")
def click_yes(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text()='Yes']", timeout=30).click()
    except:
        pass


@when("Add PO Number")
def add_po_number(context):
    try:
        context.po = generate_po()
        wait_and_find(context.driver, By.XPATH, "//input[@rel='po_nbr']"
        , timeout=30).send_keys(context.po)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Sold By/Ship From Tab")
def click_sold_by_tab(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text()='Sold By/Ship From']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Sold By Location as Main Address")
def select_sold_by_main_address(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[contains(@id, 'sold_by_address_uuid')]",
            timeout=30
        ).click()
        sold_by_input = wait_and_find(context.driver, By.XPATH, "//input[@class='select2-search__field']",
            timeout=30)
        sold_by_input.send_keys("Main Address")
        sold_by_input.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Ship From as Ship From")
def select_ship_from(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[contains(@id, 'ship_from_address_uuid')]",
            timeout=30
        ).click()
        sold_by_input = wait_and_find(context.driver, By.XPATH, "//input[@class='select2-search__field']",
            timeout=30)
        sold_by_input.send_keys("Ship From")
        sold_by_input.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Line Items Tab")
def click_line_items_tab(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text()='Line Items']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Product - Manual Inbound Shipment")
def click_add_product_manual_inbound_shipment(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text()='Add Product']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search for an RPA Product")
def search_rpa_product(context):
    try:
        product_name_input = wait_and_find(context.driver, By.XPATH, "//input[@rel='name']"
        , timeout=30)
        product_name_input.send_keys("[RPA]")
        product_name_input.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select an Each RPA Product")
def select_rpa_product(context):
    try:
        # Aguardar produto EACH aparecer na lista
        product = wait_and_find(
            context.driver,
            By.XPATH,
            "//td[@rel='name' and contains(text(), 'EACH') and not(contains(text(), 'Able Ahead'))]",
            timeout=20
        )
        context.inbounded_product = product.text
        print(f"[INFO] Produto selecionado: {context.inbounded_product}")

        # Clicar no produto com retry
        wait_and_click(
            context.driver,
            By.XPATH,
            "//td[@rel='name' and contains(text(), 'EACH') and not(contains(text(), 'Able Ahead'))]"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select an Case RPA Product")
def select_case_rpa_product(context):
    try:
        # Aguardar produto CASE aparecer na lista
        product = wait_and_find(
            context.driver,
            By.XPATH,
            "//td[@rel='name' and contains(text(), 'CASE')]",
            timeout=20
        )
        context.inbounded_product = product.text
        print(f"[INFO] Produto selecionado: {context.inbounded_product}")

        # Clicar no produto com retry
        wait_and_click(
            context.driver,
            By.XPATH,
            "//td[@rel='name' and contains(text(), 'CASE')]"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Magnifying Glass")
def click_magnifying_glass(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "//div[@class='tt_utils_forms-action-icon tt_utils_forms-action-icon-status-enabled']/img[@alt='View']"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Quantity")
def add_quantity(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//input[@name='quantity']"
        , timeout=30).send_keys("1")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Product Selection")
def click_ok_product_selection(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//div[contains(@class, 'tt_utils_ui_dlg_modal-width-class-m')]//span[text()='OK']",
            timeout=30
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Lot/Source")
def click_add_lot_source(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text()='Add Lot/Source']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Lot Number")
def add_lot_number(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//input[@name='lot']"
        , timeout=30).send_keys(generate_x_length_number(9))
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Serial Based")
def click_serial_based(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//label[text()='Serial Based']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Expiration Date")
def add_expiration_date(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//input[contains(@id,'expiration_date')]",
            timeout=30
        ).send_keys("12-12-2030")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search for All Delivery Status")
def search_all_delivery_status(context):
    try:
        delivery_status = wait_and_find(context.driver, By.XPATH, "//select[@rel='delivery_status']"
        , timeout=30)
        delivery_status.click()
        delivery_status.send_keys(Keys.ARROW_UP)
        delivery_status.send_keys(Keys.ENTER)
        wait_and_find(context.driver, By.CLASS_NAME, "tt_utils_ui_search-search-criterias-btns-search"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Lot/Source")
def click_ok_lot_source(context):
    try:
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "(//span[text()='OK'])[3]", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Product Information")
def click_ok_product_information(context):
    try:
        wait_and_find(context.driver, By.XPATH, "(//span[text()='OK'])[2]", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Manual Inbound Shipment")
def click_ok_manual_inbound_shipment(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text()='OK']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Aggregation Tab - Inbound")
def click_aggregation_tab(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text()='Aggregation']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Aggregation")
def click_on_add_aggregation(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text()='ADD']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Case Aggregation")
def click_on_add_case_aggregation(context):
    try:
        wait_and_find(context.driver, By.XPATH, "(//span[text()='ADD'])[2]", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Product Radio Button")
def select_product_radio_button(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//label[text()='Product']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Choose the Product")
def choose_product_aggregation(context):
    try:
        select_product = wait_and_find(context.driver, By.XPATH, "//select[@rel='product']"
        , timeout=30)
        select_product.click()
        select_product.send_keys(Keys.ARROW_DOWN)
        select_product.send_keys(Keys.ENTER)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Choose the Lot")
def choose_lot_aggregation(context):
    try:
        select_lot = wait_and_find(context.driver, By.XPATH, "//select[@rel='lot_or_source']"
        , timeout=30)
        select_lot.click()
        select_lot.send_keys(Keys.ARROW_DOWN)
        select_lot.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add the Serial Numbers")
def add_serial_numbers(context):
    try:
        serial = generate_x_length_number(22)
        wait_and_find(context.driver, By.XPATH, "//textarea[@rel='serial']"
        , timeout=30).send_keys(serial)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Two Serial Numbers")
def add_serial_numbers(context):
    try:
        serial_1 = generate_x_length_number(22)
        serial_2 = generate_x_length_number(22)
        wait_and_find(context.driver, By.XPATH, "//textarea[@rel='serial']"
        , timeout=30).send_keys(f"{serial_1}\n{serial_2}")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Add Aggregation")
def click_ok_aggregation(context):
    try:
        wait_and_find(context.driver, By.XPATH, "(//span[text()='OK'])[2]"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Close - Add Aggregation")
def click_close_aggregation(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text()='Close']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Utilities")
def click_utilities(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//a[@href='/utilities/']"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Manual EPCIS (XML) / X12 EDI (XML) File Upload")
def click_manual_epcis(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//label[text()='Manual EPCIS (XML) / X12 EDI (XML) File Upload']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Upload EPCIS file")
def upload_epcis_file(context):
    try:
        file_input = wait_and_find(context.driver, By.XPATH, "//input[@type='file']", timeout=30)
        current_path = os.getcwd()
        file_path = os.path.join(current_path, "epcis_file.xml")
        file_input.send_keys(file_path)
        time.sleep(3)
        wait_and_find(context.driver, By.XPATH, "//span[text()='OK']", timeout=30).click()
        time.sleep(3)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Manual File Inbound should be saved")
def file_inbound_should_be_saved(context):
    try:
        pass
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Inbound should be saved")
def inbound_should_be_saved(context):
    try:
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "//select[@rel='delivery_status']"
        , timeout=30).click()
        wait_and_find(context.driver, By.XPATH, "//option[@value='all']", timeout=30).click()
        wait_and_find(context.driver, By.CLASS_NAME, "tt_utils_ui_search-search-criterias-btns-search"
        , timeout=30).click()
        time.sleep(3)
        wait_and_find(context.driver, By.XPATH, f"//*[contains(text(),'{context.tp_name}')]", timeout=30)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Inbound should be deleted")
def inbound_should_be_deleted(context):
    try:
        time.sleep(5)
        context.driver.refresh()
        time.sleep(2)
        search_all_delivery_status(context)
        time.sleep(2)
        records_text = wait_and_find(context.driver, 
            By.CLASS_NAME, "tt_utils_ui_search-footer-nb-results"
        , timeout=30).text
        new_total_records = int(records_text.split("of ")[1].split(" recor")[0])
        assert context.total_records - new_total_records == 1
    except Exception as e:
        ends_timer(context, e)
        raise
