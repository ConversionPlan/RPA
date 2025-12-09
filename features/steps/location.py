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
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Aguardar menu estar visível
        time.sleep(2)

        # Tentar múltiplos seletores
        selectors = [
            "//a[contains(@href, '/company_mgt/')]/span[contains(text(), 'Company Management')]",
            "//a[contains(@href, '/company_mgt/')]",
            "//span[contains(text(), 'Company Management')]",
            "//*[contains(text(), 'Company Management') and (self::span or self::a)]"
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado Company Management com seletor: {selector}")
                break
            except:
                continue

        if element is None:
            raise Exception("Não foi possível encontrar o elemento Company Management")

        # Tentar clicar
        try:
            element.click()
        except:
            # Se click normal falhar, usar JavaScript
            context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Company Management via JavaScript")

        time.sleep(2)

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
        context.location_name = wait_and_find(context.driver, By.XPATH, "//div[contains(@class,'field__name') and contains(text(), '[RPA]')]",
            timeout=30
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
        # Botão "Adicionar" na aba de endereços (address)
        wait_and_find(context.driver, By.XPATH, "//div[contains(@class, 'loc_form__tabs__2_address')]//div[contains(@class, 'tt_utils_forms-one-header-action-button--add-action')]/span",
            timeout=30
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
        time.sleep(1)
        # Botão pode ser "Add" ou "Adicionar" dependendo do idioma
        # Usar o modal mais recente (maior z-index)
        element = wait_and_find(context.driver, By.XPATH, "(//div[contains(@class,'tt_utils_ui_dlg_modal-width-class-xl')]//button[contains(@class,'tt_utils_ui_dlg_modal-default-enabled-button')])[last()]", timeout=30)
        context.driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save - Location")
def click_save_location(context):
    try:
        # Botão pode ser "Save" ou "Salvar" dependendo do idioma
        wait_and_find(context.driver, By.XPATH, "//button[contains(@class,'tt_utils_ui_dlg_modal-default-enabled-button')]/span",
            timeout=30
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
