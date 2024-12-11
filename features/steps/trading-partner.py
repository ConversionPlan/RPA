from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
import time


@when("Click on Trading Partners")
def click_trading_partner(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//a[contains(@href, '/trading_partners/')]/span[contains(text(), 'Trading Partners')]").click()
    except:
        ends_timer(context)
        raise


@when("Click on Add - Trading Partner Page")
def click_add_trading_partner(context):
    try:
        context.driver.find_element(by=By.CLASS_NAME,
                                    value="tt_utils_ui_search-one-header-action-button--add-action").click()
    except:
        ends_timer(context)
        raise


@when("Add Trading Partner Name")
def input_trading_partner_name(context):
    try:
        context.trading_partner_name = generate_trading_partner_name()
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_name").send_keys(
            context.trading_partner_name)
    except:
        ends_timer(context)
        raise


@when("Select Trading Partner Type as Customer")
def select_tp_type_customer(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_type").click()
        context.driver.find_element(by=By.XPATH,
                                    value="//select[@id='TT_UTILS_UI_FORM_UUID__1_type']/option[@value='CUSTOMER']").click()
    except:
        ends_timer(context)
        raise


@when("Add Trading Partner GS1 ID (GLN)")
def input_tp_gs1_id(context):
    try:
        context.company_prefix = generate_company_prefix()
        context.gln = generate_gln(context.company_prefix)
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_gs1_id").send_keys(context.gln)
    except:
        ends_timer(context)
        raise


@when("Add Trading Partner GS1 Company Prefix")
def input_tp_gs1_company_prefix(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_gs1_company_id").send_keys(
            context.company_prefix)
    except:
        ends_timer(context)
        raise


@when("Add Trading Partner GS1 ID (SGLN)")
def input_tp_sgln(context):
    try:
        context.sgln = generate_sgln_from_gln(context.gln)
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_gs1_sgln").send_keys(context.sgln)
    except:
        ends_timer(context)
        raise


@when("Search Trading Partner by Name")
def search_tp_by_name(context):
    try:
        name_input_field = context.driver.find_element(by=By.XPATH, value="//input[@rel='name']")
        name_input_field.send_keys(context.trading_partner_name)
        name_input_field.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Click on the Pencil next to its Name")
def edit_tp(context):
    try:
        time.sleep(1)
        context.driver.find_element(by=By.XPATH, value="//img[@alt='Edit']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Address Tab")
def click_addresses_tab(context):
    try:
        time.sleep(3)
        context.driver.find_element(by=By.XPATH, value="//li[@rel='addresses']/span").click()
    except:
        ends_timer(context)
        raise


@when("Click on Add - Address")
def click_add_address(context):
    try:
        time.sleep(2)
        context.driver.find_element(by=By.XPATH,
                                    value="//div[contains(@class, 'tp_form__tabs__') and contains(@class, 'addresses')]//span[text()='Add']").click()
    except:
        ends_timer(context)
        raise


@when("Add Ship From Address Nickname")
def add_ship_from_address_nickname(context):
    try:
        time.sleep(2)
        context.driver.find_element(by=By.XPATH, value="//input[@rel='address_nickname']").send_keys("Ship From")
    except:
        ends_timer(context)
        raise


@when("Add Ship To Address Nickname")
def add_ship_to_address_nickname(context):
    try:
        time.sleep(2)
        context.driver.find_element(by=By.XPATH, value="//input[@rel='address_nickname']").send_keys("Ship To")
    except:
        ends_timer(context)
        raise


@when("Add Main Address Nickname")
def add_main_address_nickname(context):
    try:
        time.sleep(2)
        context.driver.find_element(by=By.XPATH, value="//input[@rel='address_nickname']").send_keys("Main Address")
    except:
        ends_timer(context)
        raise


@when("Add Address GLN")
def add_address_gln(context):
    try:
        context.gln = generate_gln(context.company_prefix)
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__3_gs1_id").send_keys(context.gln)
    except:
        ends_timer(context)
        raise


@when("Add Second Address GLN")
def add_sec_address_gln(context):
    try:
        context.gln = generate_gln(context.company_prefix)
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__4_gs1_id").send_keys(context.gln)
    except:
        ends_timer(context)
        raise


@when("Add Address SGLN")
def add_address_sgln(context):
    try:
        context.sgln = generate_sgln_from_gln(context.gln)
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__3_gs1_sgln").send_keys(context.sgln)
    except:
        ends_timer(context)
        raise


@when("Add Second Address SGLN")
def add_sec_address_sgln(context):
    try:
        context.sgln = generate_sgln_from_gln(context.gln)
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__4_gs1_sgln").send_keys(context.sgln)
    except:
        ends_timer(context)
        raise


@when("Add Ship From Address Recipient Name")
def add_ship_from_address_recipient(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//input[@rel='recipient_name']").send_keys("Ship From")
    except:
        ends_timer(context)
        raise


@when("Add Ship To Address Recipient Name")
def add_ship_to_address_recipient(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//input[@rel='recipient_name']").send_keys("Ship To")
    except:
        ends_timer(context)
        raise


@when("Add Main Address Recipient Name")
def add_main_address_recipient(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//input[@rel='recipient_name']").send_keys("Main Address")
    except:
        ends_timer(context)
        raise


@when("Add Address Line 1")
def add_address_line(context):
    try:
        context.address = generate_address()
        context.driver.find_element(by=By.XPATH, value="//input[@rel='line1']").send_keys(context.address)
    except:
        ends_timer(context)
        raise


@when("Add Address City")
def add_address_city(context):
    try:
        context.city = generate_city()
        context.driver.find_element(by=By.XPATH, value="//input[@rel='city']").send_keys(context.city)
    except:
        ends_timer(context)
        raise


@when("Add Address ZIP")
def add_address_zip(context):
    try:
        context.zip = generate_zip()
        context.driver.find_element(by=By.XPATH, value="//input[@rel='zip']").send_keys(context.zip)
    except:
        ends_timer(context)
        raise


@when("Click on Add - Save Address")
def click_add_address(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//button[contains(@class,'tt_utils_ui_dlg_modal-default-enabled-button')]/span[text()='Add']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Save")
def click_save_tp(context):
    try:
        time.sleep(2)
        context.driver.find_element(by=By.XPATH,
                                    value="//button[contains(@class,'tt_utils_ui_dlg_modal-default-enabled-button')]/span[text()='Save']").click()
    except:
        ends_timer(context)
        raise


@then("Trading Partner should be saved")
def tp_saved(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value=f"//*[contains(text(),'{context.trading_partner_name}')]")
    except:
        ends_timer(context)
        raise
