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
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys


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

    # Load test times - ensure it's always a list
    time_json = []
    times_path = "report/test_times.json"
    if os.path.exists(times_path):
        try:
            with open(times_path, "r") as file:
                loaded_data = json.load(file)
                # Ensure loaded_data is a list, convert dict to empty list if needed
                if isinstance(loaded_data, list):
                    time_json = loaded_data
                elif isinstance(loaded_data, dict):
                    # Corrupted data (dict instead of list), start fresh
                    print(f"[WARNING] test_times.json contains dict instead of list, resetting")
                    time_json = []
                else:
                    time_json = []
        except (FileNotFoundError, json.JSONDecodeError) as read_error:
            print(f"[WARNING] Could not load test_times.json: {read_error}")
            time_json = []

    time_json.append({"start": context.initial_time, "end": context.final_time})

    try:
        with open(times_path, "w") as file:
            file.write(json.dumps(time_json))
    except Exception as write_error:
        print(f"[WARNING] Could not write test_times.json: {write_error}")

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
                    time.sleep(2)  # Aguardar antes de retry
    else:
        print("Driver não inicializado, pulando fechamento.")


@given("Is Logged In")
def is_logged_in(context):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            launchBrowser(context)
            # Increase implicit wait for complex pages
            context.driver.implicitly_wait(15)

            # Clear cookies to ensure clean login
            context.driver.delete_all_cookies()

            openLoginURL(context, "https://qualityportal.qa-test.tracktraceweb.com/auth")

            # Small wait to ensure page is loaded
            time.sleep(2)

            enterEmail(context, "teste@teste.com")
            clickNextToLogin(context)
            enterPassword(context, "Mudar@12345342")
            clickSubmitButton(context)

            # Wait for login to complete
            time.sleep(3)

            # Verify login success by checking URL or element
            if "/dashboard" in context.driver.current_url or "/home" in context.driver.current_url:
                return  # Success

            # If not redirected, check for any error and retry
            if attempt < max_attempts - 1:
                print(f"Login attempt {attempt + 1} failed, retrying...")
                time.sleep(2)
                continue

        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"Login attempt {attempt + 1} failed with error: {str(e)[:100]}")
                time.sleep(3)
                # Try to close driver and start fresh
                try:
                    context.driver.quit()
                except:
                    pass
                continue
            else:
                ends_timer(context, e)
                raise


@given("Launching Chrome browser")
def launchBrowser(context):
    try:
        options = Options()

        # Detectar se deve usar headless
        if headless is not None:
            options.add_argument("--headless=new")
        elif os.getenv("HEADLESS", "False").lower() == "true":
            options.add_argument("--headless=new")
            print("[INFO] Modo headless ativado via variável de ambiente")

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

        # Adicionar timeout explícito e retry logic
        max_retries = 3
        retry_delay = 5  # segundos

        for attempt in range(max_retries):
            try:
                print(f"[INFO] Tentativa {attempt + 1} de {max_retries} para inicializar o Chrome...")

                # Configurar o service com timeout menor
                service = Service(ChromeDriverManager().install())

                # Criar o driver com timeout configurado
                context.driver = webdriver.Chrome(
                    service=service,
                    options=options,
                )

                # Configurar timeouts do driver
                context.driver.set_page_load_timeout(30)  # 30 segundos para carregar página
                context.driver.implicitly_wait(10)  # 10 segundos de wait implícito

                print("[OK] Chrome inicializado com sucesso!")
                break  # Sucesso, sair do loop

            except Exception as retry_error:
                print(f"[ERRO] Tentativa {attempt + 1} falhou: {str(retry_error)}")

                if attempt < max_retries - 1:
                    print(f"[INFO] Aguardando {retry_delay} segundos antes de tentar novamente...")
                    time.sleep(retry_delay)
                    retry_delay *= 1.5  # Backoff exponencial
                else:
                    print("[ERRO] Todas as tentativas falharam!")
                    raise retry_error

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
        wait_and_find(context.driver, By.ID, "auth__login_form__username"
        , timeout=30).send_keys(email)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click Next to Login")
def clickNextToLogin(context):
    try:
        wait_and_find(context.driver, By.ID, "auth__login_form__step1_next_btn"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Enter Password {password}")
def enterPassword(context, password):
    try:
        password_input = wait_and_find(context.driver, By.ID, "auth__login_form__password"
        , timeout=30)
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
        wait_and_find(context.driver, By.ID, "auth__login_form__step2_next_btn"
        , timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@then("User must login successfully")
def assertLogin(context):
    try:
        WebDriverWait(context.driver, 30).until(
            lambda x: x.find_element(by=By.XPATH, value="//div[@class='client_logo']/a")
        )
    except Exception as e:
        ends_timer(context, e)
        raise
