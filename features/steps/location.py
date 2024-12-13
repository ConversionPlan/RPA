from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
import time


@when("Click on Company Management")
def click_company_management(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//a[contains(@href, '/company_mgt/')]/span[contains(text(), 'Company Management')]").click()
    except:
        ends_timer(context)
        raise


@when("Click on Locations Management")
def click_locations_management(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//a[contains(@href, '/company_mgt/locations')]").click()
    except:
        ends_timer(context)
        raise


@when("Click on Close")
def click_close(context):
    try:
        context.driver.find_element(by=By.XPATH, value="(//span[text()='Close'])[2]").click()
        context.driver.find_element(by=By.XPATH, value="//span[text()='Close']").click()
    except:
        ends_timer(context)
        raise


@when("Save RPA location")
def search_rpa_location(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//img[@alt='View']").click()
        context.receiver_sgln = context.driver.find_element(by=By.XPATH, value="//div[contains(@class,'field__gs1_sgln')]").text
    except:
        ends_timer(context)
        raise


@when("Save Location's Name")
def save_location_name(context):
    try:
        context.location_name = context.driver.find_element(by=By.XPATH, value="//div[contains(@class,'field__name')]").text
    except:
        ends_timer(context)
        raise


@when("View Location's First Address' Details")
def view_location_address_details(context):
    try:
        context.driver.find_element(by=By.XPATH, value=f"//span[text()='{context.location_name}']").click()
    except:
        ends_timer(context)
        raise


@when("Save Location's Address Line 1")
def save_location_address(context):
    try:
        context.location_address = context.driver.find_element(by=By.XPATH, value="//div[contains(@class,'field__line1')]").text
    except:
        ends_timer(context)
        raise


@when("Save Location's City")
def save_location_city(context):
    try:
        context.location_city = context.driver.find_element(by=By.XPATH, value="//div[contains(@class,'field__city')]").text
    except:
        ends_timer(context)
        raise


@when("Save Location's State")
def save_location_state(context):
    try:
        context.location_state = context.driver.find_element(by=By.XPATH, value="//div[contains(@class,'field__state')]").text
    except:
        ends_timer(context)
        raise


@when("Save Location's Zip")
def save_location_zip(context):
    try:
        context.location_zip = context.driver.find_element(by=By.XPATH, value="//div[contains(@class,'field__zip')]").text
    except:
        ends_timer(context)
        raise


@when("Click on Add - Location Management Page")
def click_add_location_management(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//div[@class='tt_utils_ui_search-one-header-action-button tt_utils_ui_search-one-header-action-button--add-action']/span").click()
    except:
        ends_timer(context)
        raise


@when("Add Location Name")
def add_location_name(context):
    try:
        context.location_name = generate_trading_partner_name()
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_name").send_keys(
            context.location_name)
    except:
        ends_timer(context)
        raise


@when("Add Location GLN {company_prefix}")
def add_location_gln(context, company_prefix):
    try:
        context.company_prefix = company_prefix
        context.gln = generate_gln(context.company_prefix)
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_gs1_id").send_keys(context.gln)
    except:
        ends_timer(context)
        raise


@when("Add Location SGLN")
def add_location_sgln(context):
    try:
        context.sgln = generate_sgln_from_gln(context.gln)
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_gs1_sgln").send_keys(context.sgln)
    except:
        ends_timer(context)
        raise


@when("Search Location by Name")
def search_location_name(context):
    try:
        name_input_field = context.driver.find_element(by=By.XPATH, value="//input[@rel='name']")
        name_input_field.send_keys(context.location_name)
        name_input_field.send_keys(Keys.ENTER)
        time.sleep(3)
    except:
        ends_timer(context)
        raise


@when("Click on Address Tab - Location Management Page")
def click_address_tab(context):
    try:
        time.sleep(2)
        context.driver.find_element(by=By.XPATH, value="//li[@rel='address']/span").click()
    except:
        ends_timer(context)
        raise


@when("Click on Add - Location")
def click_add_location(context):
    try:
        time.sleep(2)
        context.driver.find_element(by=By.XPATH,
                                    value="//div[contains(@class, 'tt_form__tabs__one_tab_pane') ]//div[@class='tt_utils_forms-one-header-action-button tt_utils_forms-one-header-action-button--add-action']/span[text()='Add']").click()
    except:
        ends_timer(context)
        raise


@when("Add Customer Address Nickname")
def add_customer_address_nickname(context):
    try:
        time.sleep(2)
        context.driver.find_element(by=By.XPATH, value="//input[@rel='address_nickname']").send_keys(
            context.location_name)
    except:
        ends_timer(context)
        raise


@when("Add Customer Address GLN")
def add_customer_address_gln(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__3_gs1_id").send_keys(context.gln)
    except:
        ends_timer(context)
        raise


@when("Add Customer Address SGLN")
def add_customer_address_sgln(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__3_gs1_sgln").send_keys(context.sgln)
    except:
        ends_timer(context)
        raise


@when("Add Customer Address Recipient Name")
def add_customer_address_name(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//input[@rel='recipient_name']").send_keys(
            context.location_name)
    except:
        ends_timer(context)
        raise


@when("Add Customer Address Line 1")
def add_customer_address_line(context):
    try:
        context.address = generate_address()
        context.driver.find_element(by=By.XPATH, value="//input[@rel='line1']").send_keys(context.address)
    except:
        ends_timer(context)
        raise


@when("Add Customer Address City")
def add_customer_address_city(context):
    try:
        context.city = generate_city()
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__3_city").send_keys(context.city)
    except:
        ends_timer(context)
        raise


@when("Add Customer Address ZIP")
def add_customer_address_city(context):
    try:
        context.zip = generate_zip()
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__3_zip").send_keys(context.zip)
    except:
        ends_timer(context)
        raise


@when("Click on Add - Save Customer Address")
def click_add_save_customer_address(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//div[contains(@class,'tt_utils_ui_dlg_modal-width-class-xl')]//button/span[text()='Add']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Save - Location")
def click_save_location(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//button[@class='tt_utils_ui_dlg_modal-button tt_utils_ui_dlg_modal-default-enabled-button']/span[text()='Save']").click()
    except:
        ends_timer(context)
        raise


@then("Location should be saved")
def location_should_be_saved(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value=f"//*[contains(text(),'{context.location_name}')]")
    except:
        ends_timer(context)
        raise
