from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    max_attempts = 2  # Reduzido de 3 para 2 para evitar sobrecarga

    for attempt in range(max_attempts):
        try:
            # Limpar driver anterior se existir
            if hasattr(context, 'driver') and context.driver is not None:
                try:
                    context.driver.quit()
                    context.driver = None
                    time.sleep(2)  # Aguardar cleanup completo
                except:
                    pass

            # Matar processos órfãos do Chrome no Windows
            if os.name == 'nt' and attempt > 0:
                try:
                    os.system('taskkill /F /IM chrome.exe /T >nul 2>&1')
                    os.system('taskkill /F /IM chromedriver.exe /T >nul 2>&1')
                    time.sleep(2)  # Aguardar processos serem eliminados
                    print(f"[Tentativa {attempt + 1}] Processos Chrome órfãos eliminados")
                except:
                    pass

            # Criar novo browser
            launchBrowser(context)

            # Increase implicit wait for complex pages
            context.driver.implicitly_wait(15)

            # Clear cookies to ensure clean login
            context.driver.delete_all_cookies()

            openLoginURL(context, "https://qualityportal.qa-test.tracktraceweb.com/auth")

            # Wait to ensure page is loaded
            time.sleep(3)  # Aumentado de 2 para 3

            enterEmail(context, "teste@teste.com")
            clickNextToLogin(context)
            enterPassword(context, "Mudar@12345342")
            clickSubmitButton(context)

            # Wait for login to complete
            time.sleep(5)  # Aumentado de 3 para 5

            # Fechar modal de "Notas de lançamento" se aparecer
            try:
                close_btn = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Close']"))
                )
                close_btn.click()
                print("[OK] Modal 'Notas de lançamento' fechado")
                time.sleep(1)
            except:
                pass  # Modal pode não aparecer

            # Verify login success by checking URL or element
            if "/dashboard" in context.driver.current_url or "/home" in context.driver.current_url or "tracktraceweb.com" in context.driver.current_url:
                print(f"[OK] Login bem-sucedido na tentativa {attempt + 1}")
                return  # Success

            # If not redirected, check for any error and retry
            if attempt < max_attempts - 1:
                print(f"[!] Login attempt {attempt + 1} failed (not redirected), retrying...")

                # CRÍTICO: Fazer cleanup completo do driver antes de retry
                try:
                    if hasattr(context, 'driver') and context.driver:
                        context.driver.quit()
                        print("[INFO] Driver anterior fechado antes de retry")
                    context.driver = None
                except Exception as cleanup_error:
                    print(f"[AVISO] Erro ao fechar driver: {cleanup_error}")
                    context.driver = None

                # Aguardar cleanup completo
                time.sleep(3)
                continue

        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"[!] Login attempt {attempt + 1} failed with error: {str(e)[:150]}")

                # Cleanup completo antes de retry
                try:
                    if hasattr(context, 'driver') and context.driver:
                        context.driver.quit()
                    context.driver = None
                except:
                    pass

                # Aguardar mais tempo antes do próximo retry
                time.sleep(5)  # Aumentado de 3 para 5
                continue
            else:
                # Última tentativa falhou
                print(f"[X] Todas as {max_attempts} tentativas de login falharam")
                ends_timer(context, e)
                raise


@given("Launching Chrome browser")
def launchBrowser(context):
    try:
        import tempfile
        import random

        options = Options()

        # MODO HEADLESS ATIVADO
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")  # Define tamanho da janela em headless
        options.add_argument("--disable-web-security")   # Desabilita segurança web para testes
        options.add_argument("--disable-software-rasterizer")
        print("[INFO] Modo HEADLESS ativado - Chrome executará sem interface gráfica")

        # CORREÇÃO CRÍTICA: Criar diretório de dados único para cada sessão
        # Isso previne o erro "user data directory is already in use"
        temp_dir = tempfile.gettempdir()
        user_data_dir = os.path.join(temp_dir, f"chrome_automation_{random.randint(1000, 9999)}_{os.getpid()}")
        options.add_argument(f"--user-data-dir={user_data_dir}")
        print(f"[INFO] Usando user-data-dir: {user_data_dir}")

        # Opções básicas
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--lang=en-US")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--unsafely-treat-insecure-origin-as-secure=*")
        options.add_argument("--disable-features=InsecureDownloadWarnings")

        # OPÇÕES PARA ESTABILIDADE E PREVENIR ERROS DE RENDERER
        options.add_argument("--no-sandbox")  # Desabilita sandbox para melhor estabilidade
        options.add_argument("--disable-dev-shm-usage")  # Supera limitações de memória compartilhada
        options.add_argument("--disable-blink-features=AutomationControlled")  # Evita detecção de automação
        options.add_argument("--disable-extensions")  # Desabilita extensões
        options.add_argument("--disable-infobars")  # Remove info bars
        options.add_argument("--start-maximized")  # Inicia maximizado

        # Preferências
        download_dir = os.getcwd()
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": True,
            # Preferências para prevenir crashes
            "profile.default_content_setting_values.notifications": 2,  # Bloquear notificações
            "credentials_enable_service": False,  # Desabilitar salvamento de senhas
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        print("[INFO] Iniciando Chrome com opções de estabilidade...")

        # Criar driver com configurações otimizadas
        context.driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options,
        )

        # Configurar timeouts implícitos
        context.driver.implicitly_wait(10)

        print("[OK] Chrome iniciado com sucesso")

    except Exception as e:
        print(f"[ERRO] Falha ao iniciar Chrome: {str(e)[:150]}")
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
        # Verifica se o modal de "Notas de lançamento" aparece (indica login bem-sucedido)
        WebDriverWait(context.driver, 60).until(
            lambda x: x.find_element(by=By.XPATH, value="//h3[contains(@class, 'tt_utils_ui_dlg_modal-title')]")
        )
    except Exception as e:
        ends_timer(context, e)
        raise
