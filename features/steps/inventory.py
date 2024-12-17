from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
import time


@when("Click on Inventory button")
def click_inventory_button(context):
    try:
        context.driver.find_element(
            by=By.CLASS_NAME, value="inventory_block_small_wholeseller"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Click on Item Transfer")
def click_item_transfer(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//label[text()='Item Transfer']"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Click on New Item Transfer")
def click_new_item_transfer(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//span[text()='New Item Transfer']"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Change Current Location")
def change_current_location(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//a[text()='Change Location']"
        ).click()
        name_input = context.driver.find_element(
            by=By.XPATH, value="//input[@rel='name']"
        )
        name_input.send_keys(context.inbounded_location)
        name_input.send_keys(Keys.ENTER)
        time.sleep(2)
        context.driver.find_element(by=By.XPATH, value="//td[@rel='name']").click()
    except:
        ends_timer(context)
        raise


@when("Change New Location")
def change_new_location(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="(//a[text()='Change Location'])[2]"
        ).click()
        name_input = context.driver.find_element(
            by=By.XPATH, value="//input[@rel='name']"
        )
        name_input.send_keys("[RPA]")
        name_input.send_keys(Keys.ENTER)
        time.sleep(2)
        new_location = context.driver.find_element(
            by=By.XPATH,
            value=f"//td[@rel='name' and text()!='{context.inbounded_location}']",
        )
        context.new_location = new_location.text
        new_location.click()
    except:
        ends_timer(context)
        raise


@when("Set Reason")
def set_reason(context):
    try:
        select_reason = context.driver.find_element(
            by=By.XPATH, value="//select[contains(@id, '_reason_type_preset')]"
        )
        select_reason.click()
        select_reason.send_keys(Keys.ARROW_DOWN)
        select_reason.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Set Inventory Adjustment Reason")
def set_reason(context):
    try:
        select_reason = context.driver.find_element(
            by=By.XPATH, value="//select[contains(@id, '_reason_uuid')]"
        )
        select_reason.click()
        select_reason.send_keys(Keys.ARROW_DOWN)
        select_reason.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Add Reference")
def add_reference(context):
    try:
        ref = generate_ref_number()
        context.driver.find_element(
            by=By.XPATH, value="//input[contains(@id, '_reference_nbr')]"
        ).send_keys(ref)
    except:
        ends_timer(context)
        raise


@when("Click on Items Tab")
def click_items(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//li[@rel='items']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Add with Item Look Up")
def click_add_with_item_look_up(context):
    try:
        context.driver.find_element(by=By.ID, value="add_with_item_lookup").click()
    except:
        ends_timer(context)
        raise


@when("Search Inbounded Item by Name")
def search_inbounded_item_by_name(context):
    try:
        name_input = context.driver.find_element(
            by=By.XPATH, value="//input[@rel='name']"
        )
        name_input.send_keys(context.inbounded_product)
        name_input.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Click on Inbounded Item")
def click_inbounded_item(context):
    try:
        time.sleep(3)
        context.driver.find_element(
            by=By.XPATH,
            value=f"//td[@rel='name' and text()='{context.inbounded_product}']",
        ).click()
    except:
        ends_timer(context)
        raise


@when("Select Lot and Expiration Date")
def select_lot_expiration_date(context):
    try:
        time.sleep(3)
        context.driver.find_element(by=By.XPATH, value="//img[@alt='Select']").click()
        context.driver.find_element(by=By.ID, value="_tt_checkbox_field_0").click()
        context.driver.find_element(
            by=By.XPATH, value="//span[text()='Add Selection']"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Select Inbounded Item")
def select_lot_expiration_date(context):
    try:
        context.driver.find_element(by=By.ID, value="_tt_checkbox_field_0").click()
    except:
        ends_timer(context)
        raise


@when("Click on OK - Transfer Items")
def click_ok_transfer_items(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//span[text()='OK']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Quarantine")
def click_on_quarantine(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//a[@href='/quarantine/']"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Click on Quarantine Items")
def click_on_quarantine_items(context):
    try:
        context.driver.find_element(by=By.CLASS_NAME, value="quarantine_items").click()
    except:
        ends_timer(context)
        raise


@when("Click on Items in Quarantine")
def click_on_items_in_quarantine(context):
    try:
        time.sleep(5)
        context.driver.find_element(
            by=By.CLASS_NAME, value="items_in_quarantine"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Click on Inventory Adjustments")
def click_on_inventory_adjustments(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//a[@href='/adjustments/']"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Click on Destructions")
def click_on_destructions(context):
    try:
        context.driver.find_element(by=By.CLASS_NAME, value="destructions").click()
    except:
        ends_timer(context)
        raise


@when("Click on Destruct Inventory")
def click_on_destruct_inventory(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//span[text()='Destruct Inventory']"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Click on Dispenses")
def click_on_dispenses(context):
    try:
        context.driver.find_element(by=By.CLASS_NAME, value="dispense").click()
    except:
        ends_timer(context)
        raise


@when("Click on Dispense Inventory")
def click_on_dispense_inventory(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//span[text()='Dispense Inventory']"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Click on Missing/Stolen")
def click_missing_stolen(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//a[@href='/adjustments/misc_adjustment']"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Click on Add Missing/Stolen Item")
def click_add_missing_stolen_item(context):
    try:
        context.driver.find_element(
            by=By.XPATH, value="//span[text()='Add Missing/Stolen Items']"
        ).click()
    except:
        ends_timer(context)
        raise


@when("Click on Add - Report Missing/Stolen")
def click_add_report_missing_stolen(context):
    try:
        context.driver.find_element(
            by=By.XPATH,
            value="//button[contains(@class,'tt_utils_ui_dlg_modal-default-enabled-button')]/span[text()='Add']",
        ).click()
    except:
        ends_timer(context)
        raise


@then("Item should be reported")
def item_should_be_reported(context):
    try:
        time.sleep(5)
        context.driver.find_element(
            by=By.CLASS_NAME, value="tt_utils_ui_search-search-criterias-btns-search"
        ).click()
        time.sleep(1)
        context.driver.find_element(by=By.XPATH, value="//span[text()='Date']").click()
        time.sleep(1)
        context.driver.find_element(by=By.XPATH, value="//img[@alt='View']").click()
        context.driver.find_element(
            by=By.XPATH,
            value=f"//p[@class='location_name' and text()='{context.inbounded_location}']",
        )
    except:
        ends_timer(context)
        raise


@then("Item should be quarantined")
def item_should_be_quarantined(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//img[@alt='View']").click()
        context.driver.find_element(by=By.XPATH, value="//li[@rel='items']").click()
        context.driver.find_element(
            by=By.XPATH, value=f"//span[contains(text(),'{context.inbounded_product}')]"
        )

    except:
        ends_timer(context)
        raise


@then("Item should be transferred")
def item_should_be_transferred(context):
    try:
        time.sleep(5)
        context.driver.find_element(
            by=By.CLASS_NAME, value="tt_utils_ui_search-search-criterias-btns-search"
        ).click()
        time.sleep(1)
        context.driver.find_element(by=By.XPATH, value="//img[@alt='View']").click()
        context.driver.find_element(by=By.XPATH, value="//li[@rel='items']").click()
        context.driver.find_element(
            by=By.XPATH, value=f"//span[text()='{context.inbounded_product}']"
        )
    except:
        ends_timer(context)
        raise


@then("Item should be destroyed")
def item_should_be_destroyed(context):
    try:
        time.sleep(5)
        context.driver.find_element(
            by=By.CLASS_NAME, value="tt_utils_ui_search-search-criterias-btns-search"
        ).click()
        time.sleep(1)
        context.driver.find_element(by=By.XPATH, value="//span[text()='Date']").click()
        time.sleep(1)
        context.driver.find_element(by=By.XPATH, value="//img[@alt='View']").click()
        context.driver.find_element(
            by=By.XPATH,
            value=f"//p[@class='location_name' and text()='{context.inbounded_location}']",
        )
    except:
        ends_timer(context)
        raise


@then("Item should be dispensed")
def item_should_be_dispensed(context):
    try:
        time.sleep(5)
        context.driver.find_element(
            by=By.CLASS_NAME, value="tt_utils_ui_search-search-criterias-btns-search"
        ).click()
        time.sleep(1)
        context.driver.find_element(by=By.XPATH, value="//span[text()='Date']").click()
        time.sleep(1)
        context.driver.find_element(by=By.XPATH, value="//img[@alt='View']").click()
        context.driver.find_element(
            by=By.XPATH,
            value=f"//p[@class='location_name' and text()='{context.inbounded_location}']",
        )
    except:
        ends_timer(context)
        raise
