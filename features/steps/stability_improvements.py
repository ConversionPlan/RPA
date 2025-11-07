"""
Melhorias de estabilidade para resolver falhas intermitentes nos testes.
Adiciona funcoes robustas para lidar com StaleElementReferenceException
e outras condicoes de race.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException
)
import time


def safe_get_text(driver, by, value, timeout=15, retries=3):
    """
    Obtem texto de elemento de forma segura, lidando com StaleElement.
    Util para validacoes apos acoes que podem atualizar o DOM.
    """
    for attempt in range(retries):
        try:
            # Re-buscar elemento a cada tentativa
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )

            # Pequeno delay para garantir que o elemento esta estavel
            time.sleep(0.2)

            text = element.text

            if text:
                return text
            else:
                # Se texto vazio, aguardar um pouco mais
                time.sleep(0.5)
                element = driver.find_element(by, value)
                text = element.text
                if text:
                    return text

        except StaleElementReferenceException:
            time.sleep(0.5)

        except Exception:
            pass

        if attempt < retries - 1:
            time.sleep(1)

    return ""


def wait_for_page_stable(driver, timeout=5):
    """
    Aguarda a pagina estabilizar apos navegacao ou acao.
    Util para evitar StaleElement em transicoes.
    """
    try:
        # Aguardar jQuery completar (se existir)
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("""
                if (typeof jQuery !== 'undefined') {
                    return jQuery.active == 0;
                }
                return true;
            """)
        )
    except:
        pass  # jQuery pode nao estar presente

    # Aguardar estado ready
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except:
        pass

    # Pequeno delay adicional para garantir estabilidade
    time.sleep(0.3)


def refresh_and_wait(driver, by, value, timeout=15):
    """
    Faz refresh da pagina e aguarda elemento aparecer.
    Util para validacoes apos criacao de registros.
    """
    try:
        driver.refresh()
        wait_for_page_stable(driver)

        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element

    except TimeoutException:
        raise


def click_with_retry(driver, by, value, timeout=15, max_attempts=3):
    """
    Versao melhorada de click com multiplas estrategias de retry.
    """
    from selenium.webdriver.common.action_chains import ActionChains

    for attempt in range(max_attempts):
        try:
            # Estrategia 1: Click normal
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            wait_for_page_stable(driver, timeout=2)
            element.click()
            return True

        except ElementClickInterceptedException:

            # Estrategia 2: Scroll e click
            try:
                element = driver.find_element(by, value)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.5)
                element.click()
                return True
            except:
                pass

            # Estrategia 3: ActionChains
            try:
                element = driver.find_element(by, value)
                ActionChains(driver).move_to_element(element).click().perform()
                return True
            except:
                pass

            # Estrategia 4: JavaScript click
            try:
                element = driver.find_element(by, value)
                driver.execute_script("arguments[0].click();", element)
                return True
            except:
                pass

        except StaleElementReferenceException:
            time.sleep(0.5)

        except Exception:
            pass

        if attempt < max_attempts - 1:
            time.sleep(1)

    raise Exception(f"[FALHA] Impossivel clicar em {by}={value} apos {max_attempts} tentativas")


def wait_for_text_present(driver, text, timeout=15):
    """
    Aguarda texto especifico aparecer em qualquer lugar da pagina.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                ("xpath", f"//*[contains(text(), '{text}')]")
            )
        )
        return True
    except TimeoutException:
        return False


def smart_validation(driver, expected_text, timeout=15, with_refresh=False):
    """
    Validacao inteligente que pode incluir refresh se necessario.
    """
    # Primeira tentativa sem refresh
    if wait_for_text_present(driver, expected_text, timeout=5):
        return True

    if with_refresh:
        # Tentar com refresh
        driver.refresh()
        wait_for_page_stable(driver)

        if wait_for_text_present(driver, expected_text, timeout=timeout):
            return True

    # Se ainda nao encontrou, tentar busca mais ampla
    try:
        elements = driver.find_elements("xpath", f"//*[contains(., '{expected_text}')]")
        if elements:
            return True
    except:
        pass
    return False


def ensure_element_interaction(driver, by, value, action="click", data=None, timeout=15):
    """
    Garante interacao com elemento mesmo em condicoes adversas.
    action pode ser: 'click', 'send_keys', 'clear', 'get_text'
    """
    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            wait_for_page_stable(driver, timeout=2)

            if action == "click":
                return click_with_retry(driver, by, value, timeout)

            elif action == "send_keys":
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
                element.clear()
                element.send_keys(data)
                return True

            elif action == "clear":
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
                element.clear()
                return True

            elif action == "get_text":
                return safe_get_text(driver, by, value, timeout)

        except StaleElementReferenceException:
            time.sleep(1)

        except Exception:
            time.sleep(1)

    raise Exception(f"[FALHA] Impossivel executar {action} em {by}={value}")


# Exportar funcoes principais
__all__ = [
    'safe_get_text',
    'wait_for_page_stable',
    'refresh_and_wait',
    'click_with_retry',
    'wait_for_text_present',
    'smart_validation',
    'ensure_element_interaction'
]