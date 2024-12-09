from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

@given("Launching Chrome browser")
def launchBrowser(context):
    options = Options()
    options.add_argument("--headless=new")
    context.driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)

@when('Open Portal Login page {url}')
def openLoginURL(context, url):
    context.driver.maximize_window()
    context.driver.get(url)

@when('Enter Username {email}')
def enterEmail(context, email):
    context.driver.find_element(by=By.ID, value="auth__login_form__username").send_keys(email)

@when('Click Next to Login')
def clickNextToLogin(context):
    context.driver.find_element(by=By.ID, value="auth__login_form__step1_next_btn").click()

@when('Enter Password {password}')
def enterPassword(context, password):
    password_input = context.driver.find_element(by=By.ID, value="auth__login_form__password")
    wait = WebDriverWait(context.driver, timeout=3)
    wait.until(lambda d : password_input.is_displayed())
    password_input.send_keys(password)

@when('click on the Login button')
def clickSubmitButton(context):
    context.driver.find_element(by=By.ID, value="auth__login_form__step2_next_btn").click()

@then('User must login successfully')
def assertLogin(context):
    context.driver.implicitly_wait(5)
    context.driver.find_element(by=By.ID, value="tt2_ui__header__main_container")
    context.driver.close()