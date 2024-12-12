from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
from time import sleep

@when("Open dashboard page")
def open_dashboard_page(context):
    try:
        context.driver.find_element(by=By.CLASS_NAME, value="dashboard_icon")
    except:
        ends_timer(context)
        raise


@when("Open sandwich menu")
def open_sandwich_menu(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//div[contains(@class, 'sidebar_menu_toggle_dis')]/a").click()
        sleep(2)
    except:
        ends_timer(context)
        raise


@when("Click on Product Management")
def click_product_management(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//a[contains(@href, '/products/')]/span[contains(text(), 'Product Management')]").click()
    except:
        ends_timer(context)
        raise


@when("Click on Add - Product Management Page")
def click_add_product_management(context):
    try:
        context.driver.find_element(by=By.CLASS_NAME,
                                    value="tt_utils_ui_search-one-header-action-button--add-action").click()
    except:
        ends_timer(context)
        raise


@when("Click on General Tab")
def click_general_tab(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//li[@rel='general']").click()
    except:
        ends_timer(context)
        raise


@when("Add Product Name")
def input_product_name(context):
    try:
        context.product_name = generate_product_name() + " EACH"
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_name").send_keys(context.product_name)
    except:
        ends_timer(context)
        raise


@when("Add Saved Product Name")
def input_product_name(context):
    try:
        context.product_name = context.product_name.split(" EACH")[0] + " CASE"
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_name").send_keys(context.product_name)
    except:
        ends_timer(context)
        raise


@when("Add Pack Size {size}")
def add_pack_size(context, size):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_pack_size").send_keys(size)
    except:
        ends_timer(context)
        raise


@when("Select Pack Size Case")
def select_pack_size_case(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//select[@name='packaging_type']").click()
        context.driver.find_element(by=By.XPATH, value="//option[text()='Case (CA)']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Identifiers tab")
def click_identifiers_tab(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//li[@rel='identifiers']").click()
    except:
        ends_timer(context)
        raise


@when("Add SKU")
def add_sku(context):
    try:
        context.ndc = generate_ndc()
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_sku").send_keys(context.ndc)
    except:
        ends_timer(context)
        raise


@when("Add Saved SKU")
def add_sku(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_sku").send_keys(context.ndc)
    except:
        ends_timer(context)
        raise


@when("Add UPC")
def add_upc(context):
    try:
        context.company_prefix = generate_company_prefix()
        context.gs1_id = generate_gs1_id()
        context.gtin = generate_gtin_with_cp_id(context.company_prefix, context.gs1_id)
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_upc").send_keys(context.gtin)
    except:
        ends_timer(context)
        raise


@when("Add Saved UPC")
def add_upc(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_upc").send_keys(context.gtin)
    except:
        ends_timer(context)
        raise


@when("Add GS1 Company Prefix")
def input_gs1_company_prefix(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_gs1_company_prefix").send_keys(
            context.company_prefix)
    except:
        ends_timer(context)
        raise


@when("Add GS1 ID")
def input_gs1_id(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_gs1_id").send_keys(context.gs1_id)
    except:
        ends_timer(context)
        raise


@when("Click on Add Identifier")
def click_add_identifier(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//div[@class='tt_utils_forms-one-header-action-button tt_utils_forms-one-header-action-button--add-action']").click()
    except:
        ends_timer(context)
        raise


@when("Add Identifier Value")
def input_ndc_value(context):
    try:
        input_field = context.driver.find_element(by=By.XPATH, value="//input[@rel='value']")
        input_field.send_keys(context.ndc)
    except:
        ends_timer(context)
        raise


@when("Wait for Identifier Options to Load")
def wait_identifier_options(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//select[@name='identifier_code']/option[@value='US_NDC']")
    except:
        ends_timer(context)
        raise


@when("Click on Add NDC")
def click_add_ndc(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//div[contains(@class, 'tt_utils_ui_dlg_modal-width-class-l')]//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button')]").click()
    except:
        ends_timer(context)
        raise


@when("Click on Requirements Tab")
def click_requirements_tab(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//li[@rel='requirements']").click()
    except:
        ends_timer(context)
        raise


@when("Add Generic Name")
def add_generic_name(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_generic_name").send_keys(
            context.product_name)

    except:
        ends_timer(context)
        raise


@when("Add Strength")
def add_strength(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_strength").send_keys("RPA Strength")

    except:
        ends_timer(context)
        raise


@when("Add Net Content Description")
def add_net_content(context):
    try:
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_net_content_desc").send_keys(
            "RPA Net Content")
    except:
        ends_timer(context)
        raise


@when("Add Notes")
def add_notes(context):
    try:
        text = generate_text_with_n_chars(30)
        context.driver.find_element(by=By.ID, value="TT_UTILS_UI_FORM_UUID__1_notes").send_keys(text)
    except:
        ends_timer(context)
        raise


@when("Click on Add")
def click_add_ndc(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button')]").click()
    except:
        ends_timer(context)
        raise


@when("Click on Aggregation Tab")
def click_aggregation_tab(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//li[@rel='composition']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Add Product")
def click_add_product(context):
    try:
        context.driver.find_element(by=By.CLASS_NAME, value="__choose_composition_product").click()
    except:
        ends_timer(context)
        raise


@when("Input Name of Each Product into Product Name")
def input_name_each_product(context):
    try:
        name_input_field = context.driver.find_element(by=By.XPATH, value="//input[@rel='name']")
        name_input_field.send_keys(" EACH")
        name_input_field.send_keys(Keys.ENTER)
    except:
        ends_timer(context)
        raise


@when("Click on Product Name")
def click_product_name(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//table[@class='display']//td[contains(text(),' EACH')]").click()
    except:
        ends_timer(context)
        raise


@when("Add Product Quantity")
def add_product_quantity(context):
    try:
        context.product_name = context.driver.find_element(by=By.CLASS_NAME,
                                                           value="child_product_name_show_container").text
        context.gtin = context.driver.find_element(by=By.CLASS_NAME, value="child_product_gtin14_show_container").text
        context.gtin = "3" + context.gtin[1:13]
        context.ndc = context.driver.find_element(by=By.CLASS_NAME, value="child_product_name_ndc_container").text
        context.company_prefix, context.gs1_id = generate_cp_id_by_gtin(context.gtin)
        context.driver.find_element(by=By.XPATH,
                                    value="//input[starts-with(@id, 'TT_UTILS_UI_FORM_UUID_') and contains(@id, 'quantity') and @rel='quantity']").send_keys(
            "2")
    except:
        ends_timer(context)
        raise


@when("Click on Add Child Product")
def click_add_child_product(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//div[contains(@class, 'tt_utils_ui_dlg_modal-width-class-m')]//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button')]").click()
    except:
        ends_timer(context)
        raise


@when("Click on Misc Tab")
def click_misc_tab(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//li[@rel='misc']").click()
    except:
        ends_timer(context)
        raise


@when("Disable Leaf Product")
def disable_leaf_product(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value="//label[text()='This product is seen as a leaf item in the product composition']").click()
    except:
        ends_timer(context)
        raise


@then("Product should be saved")
def product_saved(context):
    try:
        context.driver.find_element(by=By.XPATH,
                                    value=f"//*[contains(text(),'{context.product_name}') or contains(text(), 'GTIN14 already exist for product')]")
    except:
        ends_timer(context)
        raise
