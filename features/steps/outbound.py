from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
import time

@when("Return to dashboard page")
def return_dashboard_page(context):
    try:
        context.driver.get("https://demopharmacoltd.qa-test.tracktraceweb.com/")
    except:
        ends_timer(context)
        raise

@when("Click on Create sales order by picking")
def click_create_so_by_picking(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//label[text()='Create sales order by picking']").click()
    except:
        ends_timer(context)
        raise


@when("Select Type Customer")
def select_type_customer(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//select[@rel='type']").click()
        context.driver.find_element(by=By.XPATH,
                                    value="//option[@value='VENDOR']").click()
    except:
        ends_timer(context)
        raise


@when("Search for an RPA Customer")
def search_rpa_customer(context):
    try:
        vendor_name = context.driver.find_element(by=By.XPATH, value="//input[@rel='name']")
        vendor_name.send_keys("[RPA]")
        vendor_name.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Select a Customer")
def select_customer(context):
    try:
        time.sleep(1)
        context.driver.find_element(by=By.XPATH, value="//td[@rel='name']").click()
    except:
        ends_timer(context)
        raise


@when("Search for Location with Inbound")
def search_location_inbound(context):
    try:
        location_name = context.driver.find_element(by=By.XPATH, value="//input[@rel='name']")
        location_name.send_keys(context.inbounded_location)
        location_name.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise

@when("Add SO Number")
def add_so_number(context):
    try:
        context.po = generate_po()
        context.driver.find_element(by=By.XPATH, value="//input[@rel='po_nbr']").send_keys(context.po)
    except:
        ends_timer(context)
        raise


@when("Click on Bought By/Ship To Tab")
def click_bought_by_tab(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='Bought By/Ship To']").click()
    except:
        ends_timer(context)
        raise


@when("Select Bought By Location as Main Address")
def select_bought_by_main_address(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[contains(@id, 'billing_address_uuid')]").click()
        sold_by_input = context.driver.find_element(by=By.XPATH, value="//input[@class='select2-search__field']")
        sold_by_input.send_keys("Main Address")
        sold_by_input.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Select Ship To as Ship To")
def select_ship_to(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[contains(@id, 'ship_to_address_uuid')]").click()
        sold_by_input = context.driver.find_element(by=By.XPATH, value="//input[@class='select2-search__field']")
        sold_by_input.send_keys("Ship To")
        sold_by_input.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Click on Picking Tab")
def click_picking_tab(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='Picking']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Inventory Lookup")
def click_inventory_lookup(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//a[text()='Inventory Lookup']").click()
    except:
        ends_timer(context)
        raise


@when("Select Shown Product")
def select_shown_product(context):
    try:
        pass
    except:
        ends_timer(context)
        raise


@when("Select Shown Serial")
def select_shown_serial(context):
    try:
        pass
    except:
        ends_timer(context)
        raise


@when("Click on Add Selection")
def click_add_selection(context):
    try:
        pass
    except:
        ends_timer(context)
        raise


@when("Click on Shipped - Status")
def click_shipped_status(context):
    try:
        pass
    except:
        ends_timer(context)
        raise


@when("Click on Shipped - Dashboard")
def click_shipped_dashboard(context):
    try:
        pass
    except:
        ends_timer(context)
        raise


@then("Outbound should be saved")
def outbound_saved(context):
    try:
        pass
    except:
        ends_timer(context)
        raise