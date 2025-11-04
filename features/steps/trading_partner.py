from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
import time
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys



@when("Click on Trading Partners")
def click_trading_partner(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//a[contains(@href, '/trading_partners/', timeout=30)]/span[contains(text(), 'Trading Partners')]",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on Add - Trading Partner Page")
def click_add_trading_partner(context):
    try:
        wait_and_find(context.driver, By.CLASS_NAME, "tt_utils_ui_search-one-header-action-button--add-action",
        , timeout=30).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Trading Partner Name")
def input_trading_partner_name(context):
    try:
        context.trading_partner_name = generate_trading_partner_name()
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_name"
        , timeout=30).send_keys(context.trading_partner_name)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Select Trading Partner Type as Customer")
def select_tp_type_customer(context):
    try:
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_type"
        , timeout=30).click()
        wait_and_find(context.driver, By.XPATH, "//select[@id='TT_UTILS_UI_FORM_UUID__1_type']/option[@value='CUSTOMER']",
        , timeout=30).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Trading Partner GS1 ID (GLN)")
def input_tp_gs1_id(context):
    try:
        context.company_prefix = generate_company_prefix()
        context.gln = generate_gln(context.company_prefix)
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_id"
        , timeout=30).send_keys(context.gln)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Trading Partner GS1 Company Prefix")
def input_tp_gs1_company_prefix(context):
    try:
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_company_id"
        , timeout=30).send_keys(context.company_prefix)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Trading Partner GS1 ID (SGLN)")
def input_tp_sgln(context):
    try:
        context.sgln = generate_sgln_from_gln(context.gln)
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_sgln"
        , timeout=30).send_keys(context.sgln)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Search Trading Partner by Name")
def search_tp_by_name(context):
    try:
        name_input_field = wait_and_find(context.driver, By.XPATH, "//input[@rel='name']"
        , timeout=30)
        name_input_field.send_keys(context.trading_partner_name)
        name_input_field.send_keys(Keys.ENTER)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on RPA Seller")
def click_rpa_seller(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[@class='tt_utils_ui_search-table-cell-responsive-value' and contains(text(, timeout=30),'[RPA]')]",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Save the Seller Name")
def click_rpa_seller(context):
    try:
        context.seller_name = wait_and_find(context.driver, By.XPATH, "//div[contains(@class,'field__name', timeout=30) and contains(text(), '[RPA]')]",
        ).text
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Save the Seller SGLN")
def click_rpa_seller(context):
    try:
        context.seller_sgln = wait_and_find(context.driver, By.XPATH, "//div[contains(text(, timeout=30),'urn:epc:id:sgln:')]"
        ).text
        time.sleep(1)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on the Pencil next to its Name")
def edit_tp(context):
    try:
        time.sleep(1)
        wait_and_find(context.driver, By.XPATH, "//img[@alt='Edit']", timeout=30).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on Address Tab")
def click_addresses_tab(context):
    try:
        time.sleep(3)
        wait_and_find(context.driver, By.XPATH, "//li[@rel='addresses']/span"
        , timeout=30).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on Add - Address")
def click_add_address(context):
    try:
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "//div[contains(@class, 'tp_form__tabs__', timeout=30) and contains(@class, 'addresses')]//span[text()='Add']",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Ship From Address Nickname")
def add_ship_from_address_nickname(context):
    try:
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "//input[@rel='address_nickname']"
        , timeout=30).send_keys("Ship From")
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Ship To Address Nickname")
def add_ship_to_address_nickname(context):
    try:
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "//input[@rel='address_nickname']"
        , timeout=30).send_keys("Ship To")
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Main Address Nickname")
def add_main_address_nickname(context):
    try:
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "//input[@rel='address_nickname']"
        , timeout=30).send_keys("Main Address")
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Address GLN")
def add_address_gln(context):
    try:
        context.gln = generate_gln(context.company_prefix)
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__3_gs1_id"
        , timeout=30).send_keys(context.gln)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Second Address GLN")
def add_sec_address_gln(context):
    try:
        context.gln = generate_gln(context.company_prefix)
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__4_gs1_id"
        , timeout=30).send_keys(context.gln)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Address SGLN")
def add_address_sgln(context):
    try:
        context.sgln = generate_sgln_from_gln(context.gln)
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__3_gs1_sgln"
        , timeout=30).send_keys(context.sgln)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Second Address SGLN")
def add_sec_address_sgln(context):
    try:
        context.sgln = generate_sgln_from_gln(context.gln)
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__4_gs1_sgln"
        , timeout=30).send_keys(context.sgln)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Ship From Address Recipient Name")
def add_ship_from_address_recipient(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//input[@rel='recipient_name']"
        , timeout=30).send_keys("Ship From")
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Ship To Address Recipient Name")
def add_ship_to_address_recipient(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//input[@rel='recipient_name']"
        , timeout=30).send_keys("Ship To")
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Main Address Recipient Name")
def add_main_address_recipient(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//input[@rel='recipient_name']"
        , timeout=30).send_keys("Main Address")
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Address Line 1")
def add_address_line(context):
    try:
        context.address = generate_address()
        wait_and_find(context.driver, By.XPATH, "//input[@rel='line1']"
        , timeout=30).send_keys(context.address)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Address City")
def add_address_city(context):
    try:
        context.city = generate_city()
        wait_and_find(context.driver, By.XPATH, "//input[@rel='city']"
        , timeout=30).send_keys(context.city)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Address ZIP")
def add_address_zip(context):
    try:
        context.zip = generate_zip()
        wait_and_find(context.driver, By.XPATH, "//input[@rel='zip']", timeout=30).send_keys(
            context.zip
        )
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on Add - Save Address")
def click_add_address(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//button[contains(@class,'tt_utils_ui_dlg_modal-default-enabled-button', timeout=30)]/span[text()='Add']",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on Save")
def click_save_tp(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//button[contains(@class,'tt_utils_ui_dlg_modal-default-enabled-button', timeout=30)]/span[text()='Save']",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@then("Trading Partner should be saved")
def tp_saved(context):
    try:
        wait_and_find(context.driver, By.XPATH, f"//*[contains(text(, timeout=30),'{context.trading_partner_name}')]"
        )
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise
