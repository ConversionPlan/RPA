from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.steps.utils import *
from features.steps.auth import ends_timer
import time
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys



@when("Click on Transformation")
def click_transform(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='Transformation']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Recipes Management")
def click_recipe_management(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//label[text(, timeout=30)='Recipes Management']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Recipe")
def click_add_recipe(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='Add Recipe']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Recipe Name")
def add_recipe_name(context):
    try:
        context.recipe_name = generate_product_name() + " RECIPE"
        wait_and_find(context.driver, By.XPATH, "//input[@name='recipe_name']"
        , timeout=30).send_keys(context.recipe_name)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Ingredients Tab")
def click_ingredients_tab(context):
    try:
        time.sleep(3)
        wait_and_find(context.driver, By.XPATH, "//li[@rel='ingredients']"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Product - Transformation Ingredient")
def click_add_product(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='Add Product']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Product - Transformation Outcome")
def click_add_product(context):
    try:
        wait_and_find(context.driver, By.XPATH, "(//span[text(, timeout=30)='Add Product'])[2]"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Add Product")
def click_ok_add_product(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='OK']").click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Add Product")
def click_add_add_product(context):
    try:
        wait_and_find(context.driver, By.XPATH, "(//span[text(, timeout=30)='Add'])[2]"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Outcome Products Tab")
def click_outcome_products_tab(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//li[@rel='outcome_products']"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Add Outcome Product")
def click_add_recipe_management(context):
    try:
        wait_and_find(context.driver, By.XPATH, "(//span[text(, timeout=30)='Add'])[2]"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Recipe Management")
def click_add_recipe_management(context):
    try:
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "(//button/span[text(, timeout=30)='Add'])[2]"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Create Recipe")
def click_add_create_recipe(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//button/span[text(, timeout=30)='Add']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Transform Inventory")
def click_transform_inventory(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//label[text(, timeout=30)='Transform Inventory']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Inbounded Recipe")
def select_inbounded_recipe(context):
    try:
        time.sleep(3)
        context.max_time = 10
        select_locator = (By.XPATH, "//select[@rel='recipe']")
        WebDriverWait(context.driver, context.max_time).until(
            EC.presence_of_element_located(select_locator)
        )
        select_element = WebDriverWait(context.driver, context.max_time).until(
            EC.element_to_be_clickable(select_locator)
        )
        select = Select(select_element)
        select_element = WebDriverWait(context.driver, context.max_time).until(
            EC.element_to_be_clickable(select_locator)
        )
        select = Select(select_element)
        select.select_by_visible_text(context.recipe_name)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Inbounded Location")
def select_inbounded_location(context):
    try:
        select_locator = (By.XPATH, "//select[@rel='production_location']")
        WebDriverWait(context.driver, context.max_time).until(
            EC.presence_of_element_located(select_locator)
        )
        select_element = WebDriverWait(context.driver, context.max_time).until(
            EC.element_to_be_clickable(select_locator)
        )
        select = Select(select_element)
        select_element = WebDriverWait(context.driver, context.max_time).until(
            EC.element_to_be_clickable(select_locator)
        )
        select = Select(select_element)
        select.select_by_visible_text(context.inbounded_location)
        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Transform Product")
def click_ok_transform_product(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='OK']").click()
        time.sleep(3)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Ingredient Record icon")
def click_ingredient_record_icon(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//img[@alt='Ingredient Record']"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Outcome Ingredient Record icon")
def click_ingredient_record_icon(context):
    try:
        wait_and_find(context.driver, By.XPATH, "(//img[@alt='Ingredient Record'], timeout=30)[2]"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Transform Product Ingredient Record")
def click_add_transform_product_ingredient_record(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[@class='_custom_button' and text(, timeout=30)='Add']"
        ).click()
        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Serial")
def click_serial(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//tr[td[@rel='inventory']/span[text(, timeout=30) = '1' or text() = '2']]/td[@rel='actions']/span/div/img[@alt='Select']",
        ).click()
        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select a Serial")
def select_serial(context):
    try:
        wait_and_find(context.driver, By.ID, "_tt_checkbox_field_0", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Transform Product Ingredient Record")
def click_ok_transform_product_ingredient_record(context):
    try:
        wait_and_find(context.driver, By.XPATH, "(//span[text(, timeout=30)='OK'])[2]"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Area")
def select_area(context):
    try:
        select_area = wait_and_find(context.driver, By.XPATH, "//select[@rel='storage_area_uuid']"
        , timeout=30)
        select_area.click()
        select_area.send_keys(Keys.ARROW_DOWN)
        select_area.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Outcome Products")
def click_ok_outcome_products(context):
    try:
        wait_and_find(context.driver, By.XPATH, "(//span[text(, timeout=30)='OK'])[2]"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Inventory button")
def click_inventory_button(context):
    try:
        wait_and_click(context.driver, By.CLASS_NAME, "inventory_block")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Item Transfer")
def click_item_transfer(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//label[text(, timeout=30)='Item Transfer']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on New Item Transfer")
def click_new_item_transfer(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='New Item Transfer']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Change Current Location")
def change_current_location(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//a[text(, timeout=30)='Change Location']"
        ).click()
        name_input = wait_and_find(context.driver, By.XPATH, "//input[@rel='name']"
        , timeout=30)
        name_input.send_keys(context.inbounded_location)
        name_input.send_keys(Keys.ENTER)
        time.sleep(2)
        wait_and_find(context.driver, By.XPATH, "//td[@rel='name']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Change New Location")
def change_new_location(context):
    try:
        wait_and_find(context.driver, By.XPATH, "(//a[text(, timeout=30)='Change Location'])[2]"
        ).click()
        name_input = wait_and_find(context.driver, By.XPATH, "//input[@rel='name']"
        , timeout=30)
        name_input.send_keys("[RPA]")
        name_input.send_keys(Keys.ENTER)
        time.sleep(2)
        new_location = wait_and_find(context.driver, By.XPATH, f"//td[@rel='name' and text(, timeout=30)!='{context.inbounded_location}']",
        )
        context.new_location = new_location.text
        new_location.click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Set Reason")
def set_reason(context):
    try:
        select_reason = wait_and_find(context.driver, By.XPATH, "//select[contains(@id, '_reason_type_preset', timeout=30)]"
        )
        select_reason.click()
        select_reason.send_keys(Keys.ARROW_DOWN)
        select_reason.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Set Inventory Adjustment Reason")
def set_reason(context):
    try:
        select_reason = wait_and_find(context.driver, By.XPATH, "//select[contains(@id, '_reason_uuid', timeout=30)]"
        )
        select_reason.click()
        select_reason.send_keys(Keys.ARROW_DOWN)
        select_reason.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Reference")
def add_reference(context):
    try:
        ref = generate_ref_number()
        wait_and_find(context.driver, By.XPATH, "//input[contains(@id, '_reference_nbr', timeout=30)]"
        ).send_keys(ref)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Items Tab")
def click_items(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//li[@rel='items']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add with Item Look Up")
def click_add_with_item_look_up(context):
    try:
        wait_and_find(context.driver, By.ID, "add_with_item_lookup", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search Inbounded Item by Name")
def search_inbounded_item_by_name(context):
    try:
        name_input = wait_and_find(context.driver, By.XPATH, "//input[@rel='name']"
        , timeout=30)
        name_input.send_keys(context.inbounded_product)
        name_input.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Inbounded Item")
def click_inbounded_item(context):
    try:
        time.sleep(3)
        wait_and_find(context.driver, By.XPATH, f"//td[@rel='name' and text(, timeout=30)='{context.inbounded_product}']",
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Lot and Expiration Date")
def select_lot_expiration_date(context):
    try:
        time.sleep(5)
        wait_and_find(context.driver, By.XPATH, "//img[@alt='Select']", timeout=30).click()
        wait_and_find(context.driver, By.ID, "_tt_checkbox_field_0", timeout=30).click()
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='Add Selection']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Inbounded Item")
def select_inbounded_item(context):
    try:
        wait_and_find(context.driver, By.ID, "_tt_checkbox_field_0", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Transfer Items")
def click_ok_transfer_items(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='OK']").click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Quarantine")
def click_on_quarantine(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//a[@href='/quarantine/']"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Quarantine Items")
def click_on_quarantine_items(context):
    try:
        wait_and_find(context.driver, By.CLASS_NAME, "quarantine_items", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Items in Quarantine")
def click_on_items_in_quarantine(context):
    try:
        # Tentar fechar modal Dismiss se existir
        dismiss_modal_if_present(context.driver)

        # Clicar em items_in_quarantine com wait robusto
        wait_and_click(
            context.driver,
            By.CLASS_NAME,
            "items_in_quarantine"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Inventory Adjustments")
def click_on_inventory_adjustments(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//a[@href='/adjustments/']"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Destructions")
def click_on_destructions(context):
    try:
        wait_and_find(context.driver, By.CLASS_NAME, "destructions", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Destruct Inventory")
def click_on_destruct_inventory(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='Destruct Inventory']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Dispenses")
def click_on_dispenses(context):
    try:
        wait_and_find(context.driver, By.CLASS_NAME, "dispense", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Dispense Inventory")
def click_on_dispense_inventory(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='Dispense Inventory']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Missing/Stolen")
def click_missing_stolen(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//a[@href='/adjustments/misc_adjustment']"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Missing/Stolen Item")
def click_add_missing_stolen_item(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='Add Missing/Stolen Items']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Report Missing/Stolen")
def click_add_report_missing_stolen(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//button[contains(@class,'tt_utils_ui_dlg_modal-default-enabled-button', timeout=30)]/span[text()='Add']",
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Item should be reported")
def item_should_be_reported(context):
    try:
        # Tentar fechar modal Dismiss se existir
        dismiss_modal_if_present(context.driver)

        # Clicar em buscar com wait robusto
        wait_and_click(
            context.driver,
            By.CLASS_NAME,
            "tt_utils_ui_search-search-criterias-btns-search"
        )

        # Clicar em Date para ordenar
        wait_and_click(context.driver, By.XPATH, "//span[text()='Date']")

        # Clicar em View
        wait_and_click(context.driver, By.XPATH, "//img[@alt='View']")

        # Verificar location name aparece
        wait_and_find(
            context.driver,
            By.XPATH,
            f"//p[@class='location_name' and text()='{context.inbounded_location}']"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Item should be quarantined")
def item_should_be_quarantined(context):
    try:
        # Tentar fechar modal Dismiss se existir
        dismiss_modal_if_present(context.driver)

        # Clicar em created_on para ordenar
        wait_and_click(context.driver, By.XPATH, "//th[@rel='created_on']/span")

        # Clicar em View
        wait_and_click(context.driver, By.XPATH, "//img[@alt='View']")

        # Clicar na tab items
        wait_and_click(context.driver, By.XPATH, "//li[@rel='items']")

        # Verificar produto aparece
        wait_and_find(
            context.driver,
            By.XPATH,
            f"//span[contains(text(),'{context.inbounded_product}')]"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Item should be transferred")
def item_should_be_transferred(context):
    try:
        # Tentar fechar modal Dismiss se existir
        dismiss_modal_if_present(context.driver)

        # Clicar em buscar
        wait_and_click(
            context.driver,
            By.CLASS_NAME,
            "tt_utils_ui_search-search-criterias-btns-search"
        )

        # Clicar em Date para ordenar
        wait_and_click(context.driver, By.XPATH, "//span[text()='Date']")

        # Clicar em View
        wait_and_click(context.driver, By.XPATH, "//img[@alt='View']")

        # Clicar na tab items
        wait_and_click(context.driver, By.XPATH, "//li[@rel='items']")

        # Verificar produto aparece
        wait_and_find(
            context.driver,
            By.XPATH,
            f"//span[text()='{context.inbounded_product}']"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Item should be destroyed")
def item_should_be_destroyed(context):
    try:
        # Tentar fechar modal Dismiss se existir
        dismiss_modal_if_present(context.driver)

        # Clicar em buscar
        wait_and_click(
            context.driver,
            By.CLASS_NAME,
            "tt_utils_ui_search-search-criterias-btns-search"
        )

        # Clicar em Date para ordenar
        wait_and_click(context.driver, By.XPATH, "//span[text()='Date']")

        # Clicar em View
        wait_and_click(context.driver, By.XPATH, "//img[@alt='View']")

        # Verificar location name aparece
        wait_and_find(
            context.driver,
            By.XPATH,
            f"//p[@class='location_name' and text()='{context.inbounded_location}']"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Item should be dispensed")
def item_should_be_dispensed(context):
    try:
        # Tentar fechar modal Dismiss se existir
        dismiss_modal_if_present(context.driver)

        # Clicar em buscar
        wait_and_click(
            context.driver,
            By.CLASS_NAME,
            "tt_utils_ui_search-search-criterias-btns-search"
        )

        # Clicar em Date para ordenar
        wait_and_click(context.driver, By.XPATH, "//span[text()='Date']")

        # Clicar em View
        wait_and_click(context.driver, By.XPATH, "//img[@alt='View']")

        # Verificar location name aparece
        wait_and_find(
            context.driver,
            By.XPATH,
            f"//p[@class='location_name' and text()='{context.inbounded_location}']"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Item should be transformed")
def item_should_be_transformed(context):
    try:
        # Clicar em inventory_transformation_log
        wait_and_click(
            context.driver,
            By.CLASS_NAME,
            "inventory_transformation_log"
        )

        # Clicar em created_on para ordenar
        wait_and_click(context.driver, By.XPATH, "//th[@rel='created_on']/span")

        # Verificar recipe name aparece
        wait_and_find(
            context.driver,
            By.XPATH,
            f"//span[text()='{context.recipe_name}']"
        )

    except Exception as e:
        ends_timer(context, e)
        raise
