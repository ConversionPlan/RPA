from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
from product import open_dashboard_page, open_sandwich_menu
import time


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
        context.driver.find_element(by=By.XPATH,
                                    value="//a[contains(@href, '/receiving/')]/span[contains(text(), 'Inbound')]").click()
    except:
        ends_timer(context)
        raise


@when("Click on Manual Inbound Shipment")
def click_manual_inbound_shipment(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//span[contains(text(), 'Manual Inbound Shipment')]").click()
    except:
        ends_timer(context)
        raise


@when("Click on Change Location")
def click_change_location(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//a[contains(text(), 'Change Location')]").click()
    except:
        ends_timer(context)
        raise


@when("Search for an RPA Location")
def search_rpa_location(context):
    try:
        location_name = context.driver.find_element(by=By.XPATH, value="//input[@rel='name']")
        location_name.send_keys("[RPA]")
        location_name.send_keys(Keys.ENTER)
        time.sleep(2)

    except:
        ends_timer(context)
        raise


@when("Select a Location")
def select_location(context):
    try:
        time.sleep(1)
        context.inbounded_location = context.driver.find_element(by=By.XPATH, value="//td[@rel='name']").text
        context.driver.find_element(by=By.XPATH, value="//img[@alt='Select']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Change Seller")
def click_change_seller(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//a[contains(text(), 'Change Seller')]").click()
    except:
        ends_timer(context)
        raise


@when("Select Type Vendor")
def select_type(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//select[@rel='type']").click()
        context.driver.find_element(by=By.XPATH,
                                    value="//option[@value='VENDOR']").click()
    except:
        ends_timer(context)
        raise


@when("Search for an RPA Seller")
def search_rpa_seller(context):
    try:
        vendor_name = context.driver.find_element(by=By.XPATH, value="//input[@rel='name']")
        vendor_name.send_keys("[RPA]")
        vendor_name.send_keys(Keys.ENTER)
        time.sleep(2)
    except:
        ends_timer(context)
        raise


@when("Select a Seller")
def select_seller(context):
    try:
        time.sleep(1)
        seller_name = context.driver.find_element(by=By.XPATH, value="//td[@rel='name']")
        context.tp_name = seller_name.text
        seller_name.click()
    except:
        ends_timer(context)
        raise


@when("Click on Yes")
def click_yes(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='Yes']").click()
    except:
        ends_timer(context)
        raise


@when("Add PO Number")
def add_po_number(context):
    try:
        context.po = generate_po()
        context.driver.find_element(by=By.XPATH, value="//input[@rel='po_nbr']").send_keys(context.po)
    except:
        ends_timer(context)
        raise


@when("Click on Sold By/Ship From Tab")
def click_sold_by_tab(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='Sold By/Ship From']").click()
    except:
        ends_timer(context)
        raise


@when("Select Sold By Location as Main Address")
def select_sold_by_main_address(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[contains(@id, 'sold_by_address_uuid')]").click()
        sold_by_input = context.driver.find_element(by=By.XPATH, value="//input[@class='select2-search__field']")
        sold_by_input.send_keys("Main Address")
        sold_by_input.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Select Ship From as Ship From")
def select_ship_from(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[contains(@id, 'ship_from_address_uuid')]").click()
        sold_by_input = context.driver.find_element(by=By.XPATH, value="//input[@class='select2-search__field']")
        sold_by_input.send_keys("Ship From")
        sold_by_input.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Click on Line Items Tab")
def click_line_items_tab(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='Line Items']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Add Product - Manual Inbound Shipment")
def click_add_product_manual_inbound_shipment(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='Add Product']").click()
    except:
        ends_timer(context)
        raise


@when("Search for an RPA Product")
def search_rpa_product(context):
    try:
        product_name_input = context.driver.find_element(by=By.XPATH, value="//input[@rel='name']")
        product_name_input.send_keys("[RPA]")
        product_name_input.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Select an RPA Product")
def select_rpa_product(context):
    try:
        time.sleep(3)
        product = context.driver.find_element(by=By.XPATH, value="//td[@rel='name']")
        context.inbounded_product = product.text
        product.click()
    except:
        ends_timer(context)
        raise


@when("Add Quantity")
def add_quantity(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//input[@name='quantity']").send_keys("1")
    except:
        ends_timer(context)
        raise


@when("Click on OK - Product Selection")
def click_ok_product_selection(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//div[contains(@class, 'tt_utils_ui_dlg_modal-width-class-m')]//span[text()='OK']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Add Lot/Source")
def click_add_lot_source(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='Add Lot/Source']").click()
    except:
        ends_timer(context)
        raise


@when("Add Lot Number")
def add_lot_number(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//input[@name='lot']").send_keys(generate_x_length_number(9))
    except:
        ends_timer(context)
        raise


@when("Click on Serial Based")
def click_serial_based(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//label[text()='Serial Based']").click()
    except:
        ends_timer(context)
        raise


@when("Add Expiration Date")
def add_expiration_date(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//input[contains(@id,'expiration_date')]").send_keys(
            "12-12-2030")
    except:
        ends_timer(context)
        raise


@when("Click on OK - Lot/Source")
def click_ok_lot_source(context):
    try:
        time.sleep(2)
        context.driver.find_element(by=By.XPATH, value="(//span[text()='OK'])[3]").click()
    except:
        ends_timer(context)
        raise


@when("Click on OK - Product Information")
def click_ok_product_information(context):
    try:
        context.driver.find_element(by=By.XPATH, value="(//span[text()='OK'])[2]").click()
    except:
        ends_timer(context)
        raise


@when("Click on OK - Manual Inbound Shipment")
def click_ok_manual_inbound_shipment(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='OK']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Aggregation Tab - Inbound")
def click_aggregation_tab(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='Aggregation']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Add - Aggregation")
def click_on_add_aggregation(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='ADD']").click()
    except:
        ends_timer(context)
        raise


@when("Select Product Radio Button")
def select_product_radio_button(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//label[text()='Product']").click()
    except:
        ends_timer(context)
        raise


@when("Choose the Product")
def choose_product_aggregation(context):
    try:
        select_product = context.driver.find_element(by=By.XPATH, value="//select[@rel='product']")
        select_product.click()
        select_product.send_keys(Keys.ARROW_DOWN)
        select_product.send_keys(Keys.ENTER)

    except:
        ends_timer(context)
        raise


@when("Choose the Lot")
def choose_lot_aggregation(context):
    try:
        select_lot = context.driver.find_element(by=By.XPATH, value="//select[@rel='lot_or_source']")
        select_lot.click()
        select_lot.send_keys(Keys.ARROW_DOWN)
        select_lot.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Add the Serial Numbers")
def add_serial_numbers(context):
    try:
        serial = generate_x_length_number(22)
        context.driver.find_element(by=By.XPATH, value="//textarea[@rel='serial']").send_keys(serial)
    except:
        ends_timer(context)
        raise


@when("Click on OK - Add Aggregation")
def click_ok_aggregation(context):
    try:
        context.driver.find_element(by=By.XPATH, value="(//span[text()='OK'])[2]").click()
    except:
        ends_timer(context)
        raise


@then("Inbound should be saved")
def inbound_should_be_saved(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//select[@rel='delivery_status']").click()
        context.driver.find_element(by=By.XPATH, value="//option[@value='all']").click()
        context.driver.find_element(by=By.CLASS_NAME, value="tt_utils_ui_search-search-criterias-btns-search").click()
        time.sleep(3)
        context.driver.find_element(by=By.XPATH,
                                    value=f"//*[contains(text(),'{context.tp_name}')]")
    except:
        ends_timer(context)
        raise
