from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
from features.steps.product import open_dashboard_page, open_sandwich_menu
from features.steps.trading_partner import click_save_tp
from datetime import datetime
import time


@given("There is a Container Created")
def there_is_container_created(context):
    open_dashboard_page(context)
    open_sandwich_menu(context)
    click_container_management(context)
    click_create_new_container(context)
    click_save_tp(context)
    click_dismiss(context)


@when("Click on Container Management")
def click_container_management(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//span[text()='Container Management']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Dismiss")
def click_dismiss(context):
    try:
        dismiss_modal_if_present(context.driver)
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Create New Container")
def click_create_new_container(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//label[text()='Create New Container']")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on List/Search Containers in Inventory")
def click_list_containers(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//label[text()='List/Search Containers in inventory']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Save Container Serial")
def save_container_serial(context):
    try:
        serial_element = wait_and_find(context.driver, By.XPATH, "//td[@rel='serial']/span")
        context.container_serial = serial_element.text
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Delete container")
def click_delete_containers(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//label[text()='Delete container']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Input Saved Serial")
def input_saved_serial(context):
    try:
        wait_and_send_keys(
            context.driver,
            By.XPATH,
            "//input[@name='gs1_unique_id_serial']",
            context.container_serial
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Deletion")
def click_ok_deletion(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//span[text()='OK']")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Container should be deleted")
def container_deleted(context):
    try:
        time.sleep(2)
        context.driver.refresh()

        # Aguardar a página recarregar e os resultados aparecerem
        records_element = wait_and_find(
            context.driver,
            By.CLASS_NAME,
            "tt_utils_ui_search-footer-nb-results",
            timeout=15
        )
        records_text = records_element.text
        new_total_records = int(records_text.split("of ")[1].split(" recor")[0])
        print(f"[INFO] Registros antes: {context.total_records}, depois: {new_total_records}")
        assert context.total_records - new_total_records == 1
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Container should be created")
def container_created(context):
    try:
        container_date_element = wait_and_find(
            context.driver,
            By.XPATH,
            "//td[@rel='created_on']/span"
        )
        container_date = container_date_element.text.split(" ")[0]
        today = datetime.now().strftime("%m-%d-%Y")
        print(f"[INFO] Data do container: {container_date}, hoje: {today}")
        assert today == container_date
    except Exception as e:
        ends_timer(context, e)
        raise
