from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from datetime import datetime
import json


@given("User exists")
def starts_timer(context):
    context.initial_time = datetime.now().strftime("%H:%M:%S")


@then("End test")
def ends_timer(context):
    context.final_time = datetime.now().strftime("%H:%M:%S")
    with open("report/test_times.json", "r") as file:
        time_json = json.load(file)

    time_json.append({"start": context.initial_time, "end": context.final_time})
    with open("report/test_times.json", "w") as file:
        file.write(json.dumps(time_json))

    context.driver.close()


@given("Is Logged In")
def is_logged_in(context):
    try:
        launchBrowser(context)
        context.driver.implicitly_wait(5)
        openLoginURL(context, "https://demopharmacoltd.qa-test.tracktraceweb.com/auth")
        enterEmail(context, "rpa-user@tracktracerx.com")
        clickNextToLogin(context)
        enterPassword(context, "Rpa!1234")
        clickSubmitButton(context)
    except:
        ends_timer(context)
        raise


@given("Launching Chrome browser")
def launchBrowser(context):
    try:
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        context.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
            options=options)
    except:
        ends_timer(context)
        raise


@when('Open Portal Login page {url}')
def openLoginURL(context, url):
    try:
        context.driver.maximize_window()
        context.driver.get(url)
    except:
        ends_timer(context)
        raise


@when('Enter Username {email}')
def enterEmail(context, email):
    try:
        context.driver.find_element(by=By.ID, value="auth__login_form__username").send_keys(email)
    except:
        ends_timer(context)
        raise


@when('Click Next to Login')
def clickNextToLogin(context):
    try:
        context.driver.find_element(by=By.ID, value="auth__login_form__step1_next_btn").click()
    except:
        ends_timer(context)
        raise


@when('Enter Password {password}')
def enterPassword(context, password):
    try:
        password_input = context.driver.find_element(by=By.ID, value="auth__login_form__password")
        wait = WebDriverWait(context.driver, timeout=3)
        wait.until(lambda d: password_input.is_displayed())
        password_input.send_keys(password)
    except:
        ends_timer(context)
        raise


@when('click on the Login button')
def clickSubmitButton(context):
    try:
        context.driver.find_element(by=By.ID, value="auth__login_form__step2_next_btn").click()
    except:
        ends_timer(context)
        raise


@then('User must login successfully')
def assertLogin(context):
    try:
        WebDriverWait(context.driver, 10).until(lambda x: x.find_element(by=By.CLASS_NAME, value="dashboard_icon"))
    except:
        ends_timer(context)
        raise
