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
        context.driver.find_element(
            By.XPATH, "//span[text()='Container Management']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Dismiss")
def click_dismiss(context):
    try:
        context.driver.find_element(By.XPATH, "//span[text()='Dismiss']").click()
        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Create New Container")
def click_create_new_container(context):
    try:
        context.driver.find_element(
            By.XPATH, "//label[text()='Create New Container']"
        ).click()
        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on List/Search Containers in Inventory")
def click_list_containers(context):
    try:
        time.sleep(2)
        context.driver.find_element(
            By.XPATH, "//label[text()='List/Search Containers in inventory']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Save Container Serial")
def save_container_serial(context):
    try:
        context.container_serial = context.driver.find_element(
            By.XPATH, "//td[@rel='serial']/span"
        ).text
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Delete container")
def click_delete_containers(context):
    try:
        context.driver.find_element(
            By.XPATH, "//label[text()='Delete container']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Input Saved Serial")
def input_saved_serial(context):
    try:
        context.driver.find_element(
            By.XPATH, "//input[@name='gs1_unique_id_serial']"
        ).send_keys(context.container_serial)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on OK - Deletion")
def click_ok_deletion(context):
    try:
        context.driver.find_element(By.XPATH, "//span[text()='OK']").click()
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Container should be deleted")
def container_deleted(context):
    try:
        time.sleep(2)
        context.driver.refresh()
        time.sleep(3)
        records_text = context.driver.find_element(
            By.CLASS_NAME, "tt_utils_ui_search-footer-nb-results"
        ).text
        new_total_records = int(records_text.split("of ")[1].split(" recor")[0])
        print(new_total_records, context.total_records)
        assert context.total_records - new_total_records == 1
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Container should be created")
def container_created(context):
    try:
        container_date = context.driver.find_element(
            By.XPATH, "//td[@rel='created_on']/span"
        ).text
        container_date = container_date.split(" ")[0]
        today = datetime.now().strftime("%m-%d-%Y")
        assert today == container_date
    except Exception as e:
        ends_timer(context, e)
        raise
