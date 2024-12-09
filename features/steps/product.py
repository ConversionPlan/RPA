from behave import *
from selenium.webdriver.common.by import By
from features.steps.utils import generate_ndc, generate_gs1_id, generate_company_prefix, generate_product_name

@when("Open dashboard page")
def open_dashboard_page(context):
    context.driver.find_element(by=By.CLASS_NAME, value="dashboard_icon")

@when("Open sandwich menu")
def open_sandwich_menu(context):
    context.driver.find_element(by=By.XPATH, value="//div[contains(@class, 'sidebar_menu_toggle_dis')]/a").click()

@when("Click on Product Management")
def click_product_management(context):
    context.driver.find_element(by=By.XPATH, value="//a[contains(@href, '/products/')]/span[contains(text(), 'Product Management')]").click()

@when("Click on Add - Product Management Page")
def click_add_product_management(context):
    context.driver.find_element(by=By.CLASS_NAME, value="tt_utils_ui_search-one-header-action-button--add-action").click()

@when("Add Product Name")
def input_product_name(context):
    product_name = generate_product_name()
    context.product_name = product_name
    context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_name").send_keys(product_name)

@when("Click on Identifiers tab")
def click_identifiers_tab(context):
    context.driver.find_element(by=By.XPATH, value="//li[@rel='identifiers']").click()

@when("Add GS1 Company Prefix")
def input_gs1_company_prefix(context):
    company_prefix = generate_company_prefix()
    context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_gs1_company_prefix").send_keys(company_prefix)

@when("Add GS1 ID")
def input_gs1_id(context):
    gs1_id = generate_gs1_id()
    context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_gs1_id").send_keys(gs1_id)

@when("Click on Add Identifier")
def click_add_identifier(context):
    context.driver.find_element(by=By.CLASS_NAME, value="tt_utils_forms-one-header-action-button--add-action").click()

@when("Click on Identifier Value")
def input_ndc_value(context):
    ndc = generate_ndc()
    context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__2_value").send_keys(ndc)

@when("Wait for Identifier Options to Load")
def wait_identifier_options(context):
    context.driver.find_element(by=By.XPATH, value="//select[@rel='identifier_code']/option[@value='US_NDC']")

@when("Click on Add NDC")
def click_add_ndc(context):
    context.driver.find_element(by=By.XPATH, value="//div[contains(@class, 'tt_utils_ui_dlg_modal-width-class-l')]//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button')]").click()

@when("Click on Add")
def click_add_ndc(context):
    context.driver.find_element(by=By.XPATH, value="//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button')]").click()

@then("Product should be saved")
def func(context):
    context.driver.find_element(by=By.XPATH, value=f"//span[text() = '{context.product_name}']")