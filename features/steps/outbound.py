from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
from features.steps.inbound import (
    do_inbound,
    click_yes,
    click_change_location,
    select_location,
)
from features.steps.trading_partner import click_save_tp
import time


@given("There is an Outbound Created")
def there_is_outbound_created(context):
    try:
        do_inbound(context)
        return_dashboard_page(context)
        click_create_so_by_picking(context)
        select_type_customer(context)
        search_rpa_customer(context)
        select_customer(context)
        click_yes(context)
        click_change_location(context)
        search_location_inbound(context)
        select_location(context)
        add_so_number(context)
        click_bought_by_tab(context)
        select_bought_by_main_address(context)
        select_ship_to(context)
        click_picking_tab(context)
        click_inventory_lookup(context)
        select_shown_product(context)
        select_shown_serial(context)
        click_add_selection(context)
        time.sleep(2)
        click_save_tp(context)
        click_shipped_status(context)
        click_save_confirm_products(context)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Return to dashboard page")
def return_dashboard_page(context):
    try:
        context.driver.get("https://demopharmacoltd.qa-test.tracktraceweb.com/")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Outbound")
def click_outbound(context):
    try:
        context.driver.find_element(
            By.XPATH, "//a[@href='/shipments/outbound_shipments/']/span"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Delete Created Outbound")
def delete_created_outbound(context):
    try:
        context.driver.find_element(By.XPATH, "//img[@alt='Delete']").click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Create sales order by picking")
def click_create_so_by_picking(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//label[text()='Create sales order by picking']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Type Customer")
def select_type_customer(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//select[@rel='type']").click()
        context.driver.find_element(
            by=By.XPATH, value="//option[@value='CUSTOMER']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search for an RPA Customer")
def search_rpa_customer(context):
    try:
        vendor_name = context.driver.find_element(
            by=By.XPATH, value="//input[@rel='name']"
        )
        vendor_name.send_keys("[RPA]")
        vendor_name.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select a Customer")
def select_customer(context):
    try:
        time.sleep(1)
        trading_partner = context.driver.find_element(
            by=By.XPATH, value="//td[@rel='name']"
        )
        context.tp_name = trading_partner.text
        trading_partner.click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search for Location with Inbound")
def search_location_inbound(context):
    try:
        location_name = context.driver.find_element(
            by=By.XPATH, value="//input[@rel='name']"
        )
        location_name.send_keys(context.inbounded_location)
        location_name.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add SO Number")
def add_so_number(context):
    try:
        context.po = generate_po()
        context.driver.find_element(
            by=By.XPATH, value="//input[@rel='po_nbr']"
        ).send_keys(context.po)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Bought By/Ship To Tab")
def click_bought_by_tab(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//span[text()='Bought By/Ship To']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Bought By Location as Main Address")
def select_bought_by_main_address(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//span[contains(@id, 'billing_address_uuid')]"
        ).click()
        sold_by_input = context.driver.find_element(
            by=By.XPATH, value="//input[@class='select2-search__field']"
        )
        sold_by_input.send_keys("Main Address")
        sold_by_input.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Ship To as Ship To")
def select_ship_to(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//span[contains(@id, 'ship_to_address_uuid')]"
        ).click()
        sold_by_input = context.driver.find_element(
            by=By.XPATH, value="//input[@class='select2-search__field']"
        )
        sold_by_input.send_keys("Ship To")
        sold_by_input.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Picking Tab")
def click_picking_tab(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//span[text()='Picking']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Inventory Lookup")
def click_inventory_lookup(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//a[text()='Inventory Lookup']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Shown Product")
def select_shown_product(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//img[@alt='Add to picking']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Shown Serial")
def select_shown_serial(context):
    try:
        context.driver.find_element(by=By.ID, value="_tt_checkbox_field_0").click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Selection")
def click_add_selection(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//span[text()='Add Selection']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Shipped - Status")
def click_shipped_status(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//input[@value='SHIPPED']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save - Confirm Products Quantity")
def click_save_confirm_products(context):
    try:
        context.driver.find_element(
            by=By.XPATH,
            value="(//button[contains(@class,'tt_utils_ui_dlg_modal-default-enabled-button')]/span[text()='Save'])[2]",
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Shipped - Dashboard")
def click_shipped_dashboard(context):
    try:
        time.sleep(2)
        context.driver.find_element(
            by=By.XPATH, value="//label[text()='Shipped']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Outbound should be saved")
def outbound_saved(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value=f"//*[contains(text(),'{context.tp_name}')]"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Outbound should be deleted")
def outbound_deleted(context):
    try:
        time.sleep(5)
        records_text = context.driver.find_element(
            By.CLASS_NAME, "tt_utils_ui_search-footer-nb-results"
        ).text
        new_total_records = int(records_text.split("of ")[1].split(" recor")[0])
        assert context.total_records - new_total_records == 1
    except Exception as e:
        ends_timer(context, e)
        raise
