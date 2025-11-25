from faker import Faker
from random import randint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException
)
import time

fake = Faker()


def generate_product_name() -> str:
    word_list = fake.get_words_list()
    product_name = "[RPA]"
    for _ in range(4):
        product_name += f" {word_list[randint(0, len(word_list) - 1)].capitalize()}"

    return product_name


def generate_trading_partner_name() -> str:
    trading_partner_name = "[RPA] " + fake.company()
    return trading_partner_name


def generate_x_length_number(x: int) -> str:
    number = ""
    for i in range(x):
        number += str(randint(0, 9))

    return number


def generate_company_prefix() -> str:
    company_prefix = "0" + generate_x_length_number(6)
    return company_prefix


def generate_gs1_id() -> str:
    gs1_id = "0" + generate_x_length_number(5)
    return gs1_id


def generate_gtin_with_cp_id(company_prefix: str, gs1_id: str) -> str:
    gtin = gs1_id[0] + company_prefix + gs1_id[1:]
    return gtin


def generate_sgtin_with_gtin(gtin: str) -> str:
    company_prefix = gtin[:7]
    item_reference = gtin[7:-1]
    item_reference = gtin[7:-1]
    sgtin = f"{company_prefix}{item_reference}.0"
    return sgtin


def generate_ndc() -> str:
    ndc = f"{generate_x_length_number(4)}-{generate_x_length_number(3)}-{generate_x_length_number(3)}"
    return ndc


def generate_text_with_n_chars(n=5) -> str:
    if n < 5 or n is None:
        n = 5
    text = fake.text(n)
    return text


def generate_cp_id_by_gtin(gtin: str) -> [str, str]:
    id = gtin[0] + gtin[8:]
    cp = gtin[1:8]
    return [cp, id]


def calculate_check_digit(base: str) -> int:
    weights = [3 if i % 2 == 0 else 1 for i in range(len(base))]
    total = sum(int(digit) * weight for digit, weight in zip(reversed(base), weights))
    remainder = total % 10
    return (10 - remainder) if remainder != 0 else 0


def generate_gln(company_prefix: str) -> str:
    gln = company_prefix + generate_x_length_number(5)
    check_digit = calculate_check_digit(gln)
    gln += str(check_digit)
    return gln


def generate_sgln_from_gln(gln: str) -> str:
    company_prefix = gln[:7]
    location_reference = gln[7:12]
    sgln_base = f"{company_prefix}.{location_reference}.0"
    sgln = f"urn:epc:id:sgln:{sgln_base}"
    return sgln


def generate_address() -> str:
    address = fake.address()
    return address


def generate_city() -> str:
    city = fake.city()
    return city


def generate_zip() -> str:
    zip = fake.zipcode()
    return zip


def generate_po() -> str:
    po = "PO#" + generate_x_length_number(9)
    return po


def generate_ref_number() -> str:
    ref = "REF#" + generate_x_length_number(9)
    return ref


# ============ FUNCOES DE WAIT E RETRY LOGIC ============

def wait_for_element(driver, by, value, timeout=30):
    """Espera um elemento estar presente no DOM"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"[TIMEOUT] Elemento nao encontrado: {by}={value}")
        raise


def wait_for_clickable(driver, by, value, timeout=30):
    """Espera um elemento estar clicavel"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        return element
    except TimeoutException:
        print(f"[TIMEOUT] Elemento nao clicavel: {by}={value}")
        raise


def wait_and_click(driver, by, value, timeout=30, retries=3):
    """
    Espera elemento estar clicavel e clica com retry logic.
    Lida com StaleElement, ElementClickIntercepted e outros erros comuns.
    """
    for attempt in range(retries):
        try:
            # Aguardar elemento estar clicavel
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )

            # Pequeno delay para evitar race conditions
            time.sleep(0.3)

            # Tentar clicar
            element.click()

            print(f"[OK] Clicou em {by}={value} na tentativa {attempt + 1}")
            return element

        except ElementClickInterceptedException:
            print(f"[Tentativa {attempt + 1}] Elemento interceptado: {by}={value}")

            # Tentar scroll ate o elemento
            try:
                element = driver.find_element(by, value)
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.click()
                print(f"[OK] Clicou apos scroll na tentativa {attempt + 1}")
                return element
            except Exception as scroll_error:
                print(f"[ERRO] Scroll falhou: {scroll_error}")
                # Tentar JavaScript click como ultimo recurso
                try:
                    element = driver.find_element(by, value)
                    driver.execute_script("arguments[0].click();", element)
                    print(f"[OK] Clicou com JavaScript apos falha de scroll")
                    return element
                except Exception as js_error:
                    print(f"[ERRO] JavaScript click falhou: {js_error}")

        except StaleElementReferenceException:
            print(f"[Tentativa {attempt + 1}] Elemento stale: {by}={value}")
            time.sleep(0.5)  # Aguardar DOM atualizar

        except TimeoutException:
            print(f"[Tentativa {attempt + 1}] Timeout esperando: {by}={value}")

        except Exception as e:
            print(f"[Tentativa {attempt + 1}] Erro ao clicar: {e}")

        # Aguardar antes de retry
        if attempt < retries - 1:
            time.sleep(1)

    # Se chegou aqui, todas as tentativas falharam
    raise Exception(f"[FALHA] Nao foi possivel clicar em {by}={value} apos {retries} tentativas")


def wait_and_send_keys(driver, by, value, keys, timeout=30, retries=3):
    """
    Espera elemento estar disponivel e envia keys com retry logic.
    Lida com StaleElement e outros erros comuns.
    """
    for attempt in range(retries):
        try:
            # Aguardar elemento estar presente
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )

            # Aguardar estar visivel
            WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )

            # Pequeno delay
            time.sleep(0.3)

            # Limpar campo antes de enviar keys
            element.clear()
            element.send_keys(keys)

            print(f"[OK] Enviou keys para {by}={value} na tentativa {attempt + 1}")
            return element

        except StaleElementReferenceException:
            print(f"[Tentativa {attempt + 1}] Elemento stale: {by}={value}")
            time.sleep(0.5)

        except TimeoutException:
            print(f"[Tentativa {attempt + 1}] Timeout esperando: {by}={value}")

        except Exception as e:
            print(f"[Tentativa {attempt + 1}] Erro ao enviar keys: {e}")

        # Aguardar antes de retry
        if attempt < retries - 1:
            time.sleep(1)

    # Se chegou aqui, todas as tentativas falharam
    raise Exception(f"[FALHA] Nao foi possivel enviar keys para {by}={value} apos {retries} tentativas")


def wait_and_find(driver, by, value, timeout=30, retries=3):
    """
    Espera e busca elemento com retry logic.
    Retorna o elemento quando encontrado.
    """
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            print(f"[OK] Encontrou {by}={value} na tentativa {attempt + 1}")
            return element

        except TimeoutException:
            print(f"[Tentativa {attempt + 1}] Timeout esperando: {by}={value}")

        except Exception as e:
            print(f"[Tentativa {attempt + 1}] Erro ao buscar: {e}")

        if attempt < retries - 1:
            time.sleep(1)

    raise Exception(f"[FALHA] Nao foi possivel encontrar {by}={value} apos {retries} tentativas")


def dismiss_modal_if_present(driver, timeout=3):
    """
    Tenta fechar modal de 'Dismiss' se estiver presente.
    Nao falha se o modal nao existir.
    """
    try:
        from selenium.webdriver.common.by import By
        dismiss_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Dismiss']"))
        )
        dismiss_button.click()
        time.sleep(0.5)
        print("[OK] Modal 'Dismiss' fechado")
        return True
    except:
        # Modal nao presente, tudo bem
        return False


def take_screenshot(driver, name="screenshot", path="report/output/screenshots"):
    """
    Tira screenshot para debug, especialmente útil em falhas.
    """
    import os
    from datetime import datetime

    try:
        # Criar diretório se não existir
        os.makedirs(path, exist_ok=True)

        # Nome único com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{path}/{name}_{timestamp}.png"

        # Tirar screenshot
        driver.save_screenshot(filename)
        print(f"[SCREENSHOT] Salvo em: {filename}")
        return filename
    except Exception as e:
        print(f"[ERRO] Não foi possível tirar screenshot: {str(e)}")
        return None


def wait_for_page_ready(driver, timeout=30):
    """
    Aguarda a página estar completamente carregada.
    """
    try:
        # Aguardar JavaScript indicar página pronta
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Aguardar jQuery se existir
        try:
            WebDriverWait(driver, 2).until(
                lambda d: d.execute_script("return typeof jQuery !== 'undefined' && jQuery.active == 0")
            )
        except:
            pass  # jQuery pode não estar presente

        return True
    except Exception as e:
        print(f"[AVISO] Página pode não estar completamente carregada: {str(e)}")
        return False


def retry_on_stale_element(func, max_retries=3, delay=1):
    """
    Decorador para retry em caso de StaleElementReferenceException.
    """
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    continue
                raise
        return None
    return wrapper


def fill_input_with_js_fallback(driver, by, value, text, timeout=30):
    """
    Preenche um campo de input com fallback para JavaScript.
    Útil para campos que podem não estar interativos via Selenium normal.
    """
    from selenium.webdriver.support import expected_conditions as EC

    # Aguardar o elemento estar presente no DOM
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
    print(f"[INFO] Elemento {by}={value} encontrado no DOM")

    # Scroll até o elemento
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)

    # Tentar interação normal primeiro
    try:
        element.clear()
        element.send_keys(text)
        print(f"[OK] Campo preenchido normalmente com: {text}")
        return element
    except Exception as normal_error:
        print(f"[WARN] Interação normal falhou: {str(normal_error)[:100]}")

    # Se falhar, usar JavaScript para preencher
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
        element,
        text
    )
    print(f"[OK] Campo preenchido via JavaScript com: {text}")
    return element
