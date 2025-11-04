from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from features.steps.auth import ends_timer
from features.steps.utils import generate_sgtin_with_gtin
import time
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys



@when("Open a new tab")
def open_new_tab(context):
    try:
        context.driver.execute_script("window.open('');")
        context.driver.switch_to.window(context.driver.window_handles[-1])
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Open EPCIS Generator")
def open_epcis_generator(context):
    try:
        context.driver.get("https://epcis-file-generator.tracktracenetwork.com/")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Generate Random Data")
def click_generate_random_data(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//p[text(, timeout=30)='Generate Random Data']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Sender Main Location Information")
def click_generate_random_data(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//p[text(, timeout=30)='Sender Main Location Information']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Replace SGLN with Location's saved SGLN")
def replace_location_sgln(context):
    try:
        location_sgln = wait_and_find(context.driver, By.XPATH, "(//input[contains(@value, 'urn:epc:id:sgln:', timeout=30)])[3]"
        )
        location_sgln.click()
        ActionChains(context.driver).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).perform()
        location_sgln.send_keys(Keys.BACKSPACE)
        location_sgln.send_keys(context.location_sgln)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Replace Location Name with Location's saved name")
def replace_location_name(context):
    try:
        location_name = wait_and_find(context.driver, By.XPATH, "//input[contains(@value, 'Sender ', timeout=30)]"
        )
        location_name.click()
        ActionChains(context.driver).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).perform()
        location_name.send_keys(Keys.BACKSPACE)
        location_name.send_keys(context.location_name)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Receiver Main Location Information")
def click_generate_random_data(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//p[text(, timeout=30)='Receiver Main Location Information']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Replace SGLN with Seller's saved SGLN")
def replace_seller_sgln(context):
    try:
        seller_sgln = wait_and_find(context.driver, By.XPATH, "(//input[contains(@value, 'urn:epc:id:sgln:', timeout=30)])[4]"
        )
        seller_sgln.click()
        ActionChains(context.driver).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).perform()
        seller_sgln.send_keys(Keys.BACKSPACE)
        seller_sgln.send_keys(context.seller_sgln)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Replace Location Name with Seller's saved name")
def replace_seller_name(context):
    try:
        seller_name = wait_and_find(context.driver, By.XPATH, "//input[contains(@value, 'Receiver ', timeout=30)]"
        )
        seller_name.click()
        ActionChains(context.driver).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).perform()
        seller_name.send_keys(Keys.BACKSPACE)
        seller_name.send_keys(context.seller_name)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on #1 Product Information")
def click_product_information(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//p[text(, timeout=30)='#1 Product Information']"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Replace SGTIN's with a new SGTIN GCP and GS1 ID")
def replace_product_sgtin(context):
    try:
        product_sgtin = wait_and_find(context.driver, By.XPATH, "//input[contains(@value, 'urn:epc:id:sgtin:', timeout=30)]"
        )
        product_sgtin.click()
        ActionChains(context.driver).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).perform()
        product_sgtin.send_keys(Keys.BACKSPACE)
        product_sgtin.send_keys(generate_sgtin_with_gtin(context.product_gtin))
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Replace Product Name with Product's saved name")
def replace_product_name(context):
    try:
        product_name = wait_and_find(context.driver, By.XPATH, "//input[contains(@value, 'Product ', timeout=30)]"
        )
        product_name.click()
        ActionChains(context.driver).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).perform()
        product_name.send_keys(Keys.BACKSPACE)
        product_name.send_keys(context.product_name)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Submit")
def click_submit(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//p[text(, timeout=30)='Submit']").click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Download EPCIS file")
def click_submit(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//p[text(, timeout=30)='Download EPCIS file']"
        ).click()
        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Close the tab")
def click_submit(context):
    try:
        tabs = context.driver.window_handles
        context.driver.close()
        context.driver.switch_to.window(tabs[0])
    except Exception as e:
        ends_timer(context, e)
        raise
