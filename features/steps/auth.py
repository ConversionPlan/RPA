from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import json
import os
import time
import traceback

headless = os.environ.get("HEADLESS")


@given("User exists")
def starts_timer(context):
    context.initial_time = datetime.now().strftime("%H:%M:%S")


@then("End test")
def ends_timer(context, e=None):
    if e is not None:
        with open("report/output/errors", "a") as file:
            file.write(traceback.format_exc() + "\n\n")

    context.final_time = datetime.now().strftime("%H:%M:%S")
    with open("report/test_times.json", "r") as file:
        time_json = json.load(file)

    time_json.append({"start": context.initial_time, "end": context.final_time})
    with open("report/test_times.json", "w") as file:
        file.write(json.dumps(time_json))

    # Melhorado: Cleanup robusto do driver com retry logic
    if hasattr(context, 'driver') and context.driver is not None:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Aguardar um pouco antes de fechar para evitar race conditions
                time.sleep(0.5)

                # Primeiro fecha todas as janelas
                try:
                    context.driver.close()
                except Exception as close_error:
                    print(f"[Tentativa {attempt + 1}] Erro ao fechar janela: {close_error}")

                # Depois encerra a sessao do WebDriver completamente
                time.sleep(0.3)
                context.driver.quit()

                # Marca driver como None para evitar reutilizacao
                context.driver = None

                print(f"[OK] Driver fechado com sucesso na tentativa {attempt + 1}")
                break

            except Exception as quit_error:
                print(f"[Tentativa {attempt + 1}] Erro ao encerrar driver: {quit_error}")

                if attempt == max_retries - 1:
                    print("[AVISO] Falha ao fechar driver apos 3 tentativas")
                    # Forcar limpeza do driver mesmo com erro
                    context.driver = None

                    # No Windows, tentar matar processos orfaos do Chrome
                    if os.name == 'nt':
                        try:
                            os.system('taskkill /F /IM chrome.exe /T 2>nul')
                            os.system('taskkill /F /IM chromedriver.exe /T 2>nul')
                            print("[INFO] Processos Chrome orfaos eliminados")
                        except Exception as kill_error:
                            print(f"[AVISO] Erro ao matar processos: {kill_error}")
                else:
                    time.sleep(1)  # Aguardar antes de retry
    else:
        print("Driver não inicializado, pulando fechamento.")


@given("Is Logged In")
def is_logged_in(context):
    try:
        launchBrowser(context)
        context.driver.implicitly_wait(5)
        openLoginURL(context, "https://qualityportal.qa-test.tracktraceweb.com/auth")
        enterEmail(context, "teste@teste.com")
        clickNextToLogin(context)
        enterPassword(context, "Mudar@12345342")
        clickSubmitButton(context)
    except Exception as e:
        ends_timer(context, e)
        raise


@given("Launching Chrome browser")
def launchBrowser(context):
    try:
        options = Options()
        if headless is not None:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--lang=en-US")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--unsafely-treat-insecure-origin-as-secure=*")
        options.add_argument("--disable-features=InsecureDownloadWarnings")
        download_dir = os.getcwd()
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        context.driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options,
        )

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Open Portal Login page {url}")
def openLoginURL(context, url):
    try:
        context.driver.maximize_window()
        context.driver.get(url)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Open Track Tace page")
def openTTRXPage(context):
    try:
        context.driver.maximize_window()
        context.driver.get("https://www.tracktracerx.com/")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Enter Username {email}")
def enterEmail(context, email):
    try:
        context.driver.find_element(
            by=By.ID, value="auth__login_form__username"
        ).send_keys(email)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click Next to Login")
def clickNextToLogin(context):
    try:
        context.driver.find_element(
            by=By.ID, value="auth__login_form__step1_next_btn"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Enter Password {password}")
def enterPassword(context, password):
    try:
        password_input = context.driver.find_element(
            by=By.ID, value="auth__login_form__password"
        )
        wait = WebDriverWait(context.driver, timeout=3)
        wait.until(lambda d: password_input.is_displayed())
        password_input.send_keys(password)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("click on the Login button")
def clickSubmitButton(context):
    try:
        time.sleep(2)
        context.driver.find_element(
            by=By.ID, value="auth__login_form__step2_next_btn"
        ).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@then("User must login successfully")
def assertLogin(context):
    try:
        WebDriverWait(context.driver, 10).until(
            lambda x: x.find_element(by=By.XPATH, value="//div[@class='client_logo']/a")
        )
    except Exception as e:
        ends_timer(context, e)
        raise
