from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
import time
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys



@when("Click on Company Management")
def click_company_management(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//a[contains(@href, '/company_mgt/')]/span[contains(text(), 'Company Management')]", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Locations Management")
def click_locations_management(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//a[contains(@href, '/company_mgt/locations')]", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Location Management Page")
def click_add_location_management(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//div[@class='tt_utils_ui_search-one-header-action-button tt_utils_ui_search-one-header-action-button--add-action']/span", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Location Name")
def add_location_name(context):
    try:
        context.location_name = generate_trading_partner_name()
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_name"
, timeout=30).send_keys(context.location_name)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on RPA Location")
def click_rpa_location(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[@class='tt_utils_ui_search-table-cell-responsive-value' and contains(text(),'[RPA]')]",
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Save Location Name")
def click_rpa_location(context):
    try:
        context.location_name = wait_and_find(context.driver, By.XPATH, "//div[contains(@class,'field__name', timeout=30) and contains(text(), '[RPA]')]",
        ).text
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Save Location SGLN")
def click_rpa_location(context):
    try:
        context.location_sgln = wait_and_find(context.driver, By.XPATH, "//div[contains(text(),'urn:epc:id:sgln:')]"
        ).text
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Location GLN {company_prefix}")
def add_location_gln(context, company_prefix):
    try:
        context.company_prefix = company_prefix
        context.gln = generate_gln(context.company_prefix)
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_id"
, timeout=30).send_keys(context.gln)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Location SGLN")
def add_location_sgln(context):
    try:
        context.sgln = generate_sgln_from_gln(context.gln)
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_sgln"
, timeout=30).send_keys(context.sgln)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search Location by Name")
def search_location_name(context):
    try:
        name_input_field = wait_and_find(context.driver, By.XPATH, "//input[@rel='name']"
, timeout=30)
        name_input_field.send_keys(context.location_name)
        name_input_field.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Address Tab - Location Management Page")
def click_address_tab(context):
    try:
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "//li[@rel='address']/span"
, timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Location")
def click_add_location(context):
    try:
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "//div[contains(@class, 'tt_form__tabs__one_tab_pane', timeout=30) ]//div[@class='tt_utils_forms-one-header-action-button tt_utils_forms-one-header-action-button--add-action']/span[text()='Add']",
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Customer Address Nickname")
def add_customer_address_nickname(context):
    try:
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "//input[@rel='address_nickname']"
, timeout=30).send_keys(context.location_name)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Customer Address GLN")
def add_customer_address_gln(context):
    try:
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__3_gs1_id"
, timeout=30).send_keys(context.gln)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Customer Address SGLN")
def add_customer_address_sgln(context):
    try:
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__3_gs1_sgln"
, timeout=30).send_keys(context.sgln)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Customer Address Recipient Name")
def add_customer_address_name(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//input[@rel='recipient_name']"
, timeout=30).send_keys(context.location_name)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Customer Address Line 1")
def add_customer_address_line(context):
    try:
        context.address = generate_address()
        wait_and_find(context.driver, By.XPATH, "//input[@rel='line1']"
, timeout=30).send_keys(context.address)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Customer Address City")
def add_customer_address_city(context):
    try:
        context.city = generate_city()
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__3_city"
, timeout=30).send_keys(context.city)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Customer Address ZIP")
def add_customer_address_city(context):
    try:
        context.zip = generate_zip()
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__3_zip"
, timeout=30).send_keys(context.zip)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Save Customer Address")
def click_add_save_customer_address(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//div[contains(@class,'tt_utils_ui_dlg_modal-width-class-xl')]//button/span[text()='Add']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save - Location")
def click_save_location(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//button[@class='tt_utils_ui_dlg_modal-button tt_utils_ui_dlg_modal-default-enabled-button']/span[text()='Save']",
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Location should be saved")
def location_should_be_saved(context):
    try:
        wait_and_find(context.driver, By.XPATH, f"//*[contains(text(),'{context.location_name}')]"
        )
    except Exception as e:
        ends_timer(context, e)
        raise
