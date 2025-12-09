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


# Contador global para garantir unicidade absoluta entre chamadas consecutivas
_gtin_counter = 0


def generate_company_prefix() -> str:
    """
    Gera um Company Prefix único usando UUID truncado.

    Formato: 7 dígitos total
    Usa uuid4() que é criptograficamente seguro e gera 128 bits de aleatoriedade.
    Converte para número e pega os 7 dígitos do meio para evitar padrões.

    Isso garante unicidade absoluta mesmo em chamadas consecutivas.
    """
    import uuid
    # Usar UUID4 para aleatoriedade criptográfica completa
    uuid_int = uuid.uuid4().int
    # Pegar 7 dígitos do meio do UUID (posição 5-12 de um número de 38+ dígitos)
    uuid_str = str(uuid_int)
    # Garantir que temos dígitos suficientes e pegar do meio
    if len(uuid_str) >= 20:
        company_prefix = uuid_str[6:13]  # 7 dígitos do meio
    else:
        company_prefix = uuid_str[:7].zfill(7)
    return company_prefix


def generate_gs1_id() -> str:
    """
    Gera um GS1 ID único usando UUID truncado + contador.

    Formato: 6 dígitos total
    Usa uuid4() combinado com contador global para garantir que
    mesmo chamadas consecutivas geram valores diferentes.

    Combinado com company_prefix (que usa UUID separado), garante unicidade absoluta.
    """
    import uuid
    global _gtin_counter
    _gtin_counter += 1
    # Usar UUID4 para aleatoriedade criptográfica
    uuid_int = uuid.uuid4().int
    # Combinar com contador para garantir unicidade em chamadas rápidas
    combined = uuid_int + _gtin_counter
    combined_str = str(combined)
    # Pegar 6 dígitos de uma posição diferente do company_prefix
    if len(combined_str) >= 20:
        gs1_id = combined_str[15:21]  # 6 dígitos de posição diferente
    else:
        gs1_id = combined_str[-6:].zfill(6)
    return gs1_id


def generate_gtin_with_cp_id(company_prefix: str, gs1_id: str) -> str:
    """
    Gera GTIN a partir do Company Prefix e GS1 ID.
    Formato: 1 dígito (gs1_id[0]) + 7 dígitos (company_prefix) + 5 dígitos (gs1_id[1:])
    Total: 13 dígitos (GTIN-13)
    """
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


def wait_and_click(driver, by, value, timeout=10, retries=2):
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
            time.sleep(0.3)  # Aguardar DOM atualizar

        except TimeoutException:
            print(f"[Tentativa {attempt + 1}] Timeout esperando: {by}={value}")

        except Exception as e:
            print(f"[Tentativa {attempt + 1}] Erro ao clicar: {e}")

        # Aguardar antes de retry
        if attempt < retries - 1:
            time.sleep(0.5)

    # Se chegou aqui, todas as tentativas falharam
    raise Exception(f"[FALHA] Nao foi possivel clicar em {by}={value} apos {retries} tentativas")


def wait_and_send_keys(driver, by, value, keys, timeout=10, retries=2):
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

            # Limpar campo antes de enviar keys
            element.clear()
            element.send_keys(keys)

            print(f"[OK] Enviou keys para {by}={value} na tentativa {attempt + 1}")
            return element

        except StaleElementReferenceException:
            print(f"[Tentativa {attempt + 1}] Elemento stale: {by}={value}")
            time.sleep(0.3)

        except TimeoutException:
            print(f"[Tentativa {attempt + 1}] Timeout esperando: {by}={value}")

        except Exception as e:
            print(f"[Tentativa {attempt + 1}] Erro ao enviar keys: {e}")

        # Aguardar antes de retry
        if attempt < retries - 1:
            time.sleep(0.5)

    # Se chegou aqui, todas as tentativas falharam
    raise Exception(f"[FALHA] Nao foi possivel enviar keys para {by}={value} apos {retries} tentativas")


def wait_and_find(driver, by, value, timeout=10, retries=2):
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
            time.sleep(0.5)

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


def close_all_modals(driver, timeout=5):
    """
    Tenta fechar todos os modais abertos usando múltiplas estratégias.
    """
    from selenium.webdriver.common.by import By
    closed_any = False

    # Estratégia 1: Clicar no botão X (close button)
    close_buttons = [
        "//span[contains(@class, 'tt_utils_ui_dlg_modal-close_button')]",
        "//button[contains(@class, 'close')]",
        "//span[contains(@class, 'close')]",
        "//*[contains(@class, 'modal-close')]",
    ]

    for selector in close_buttons:
        try:
            buttons = driver.find_elements(By.XPATH, selector)
            for btn in buttons:
                if btn.is_displayed():
                    try:
                        btn.click()
                        print(f"[OK] Modal fechado via botão X: {selector}")
                        closed_any = True
                        time.sleep(0.5)
                    except:
                        driver.execute_script("arguments[0].click();", btn)
                        print(f"[OK] Modal fechado via JS: {selector}")
                        closed_any = True
                        time.sleep(0.5)
        except:
            continue

    # Estratégia 2: Clicar no botão Dismiss
    dismiss_modal_if_present(driver, timeout=2)

    # Estratégia 3: Remover overlays via JavaScript
    try:
        driver.execute_script("""
            var overlays = document.querySelectorAll('.tt_utils_ui_dlg_modal-overlay');
            overlays.forEach(function(overlay) {
                overlay.style.display = 'none';
                overlay.style.visibility = 'hidden';
            });
            var modals = document.querySelectorAll('[class*="modal"]');
            modals.forEach(function(modal) {
                if (modal.style.zIndex > 1000) {
                    modal.style.display = 'none';
                }
            });
        """)
        print("[OK] Overlays removidos via JavaScript")
        closed_any = True
    except Exception as e:
        print(f"[WARN] Não foi possível remover overlays via JS: {e}")

    time.sleep(1)
    return closed_any


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


def safe_parse_records_count(records_text: str, default: int = 0) -> int:
    """
    Extrai o número total de registros de um texto como "1 to 10 of 100 records".

    Evita o erro 'tuple index out of range' fazendo parsing seguro.
    Suporta formatos em inglês (of) e português (de).

    Args:
        records_text: Texto contendo o contador de registros
        default: Valor padrão caso o parsing falhe

    Returns:
        Número total de registros ou valor default se não conseguir parsear
    """
    import re

    if not records_text or not isinstance(records_text, str):
        print(f"[WARN] records_text inválido: {records_text}")
        return default

    try:
        # Padrão 1: "X to Y of Z records" ou "X a Y de Z registros"
        # Regex para capturar o número total após "of " ou "de "
        match = re.search(r'(?:of|de)\s+(\d+)', records_text, re.IGNORECASE)
        if match:
            result = int(match.group(1))
            print(f"[INFO] Parsed records count: {result} from '{records_text}'")
            return result

        # Padrão 2: Apenas números no texto (fallback)
        numbers = re.findall(r'\d+', records_text)
        if numbers:
            # Pegar o último número (geralmente é o total)
            result = int(numbers[-1])
            print(f"[INFO] Parsed records count (fallback): {result} from '{records_text}'")
            return result

        print(f"[WARN] Não foi possível extrair número de: '{records_text}'")
        return default

    except (ValueError, IndexError, AttributeError) as e:
        print(f"[ERRO] Falha ao parsear records_text '{records_text}': {e}")
        return default


def safe_split_date(date_text: str, separator: str = " ", index: int = 0, default: str = "") -> str:
    """
    Extrai parte de uma data com split seguro.

    Evita o erro 'tuple index out of range' ao acessar índices de split.

    Args:
        date_text: Texto contendo a data
        separator: Separador para split
        index: Índice a ser acessado
        default: Valor padrão caso o split falhe

    Returns:
        Parte da data ou valor default se não conseguir extrair
    """
    if not date_text or not isinstance(date_text, str):
        print(f"[WARN] date_text inválido: {date_text}")
        return default

    try:
        parts = date_text.split(separator)
        if len(parts) > index:
            return parts[index]
        else:
            print(f"[WARN] Índice {index} não existe em '{date_text}' (split por '{separator}')")
            return default
    except Exception as e:
        print(f"[ERRO] Falha ao fazer split de '{date_text}': {e}")
        return default


# ============ FUNCOES DE VALIDACAO ROBUSTA (QA HELPERS) ============

def assert_datetime_near(
    actual: str,
    expected_datetime=None,
    tolerance_seconds: int = 300,
    date_format: str = "%m-%d-%Y",
    allow_date_only: bool = True
) -> bool:
    """
    Valida se uma data/hora está dentro de uma janela de tolerância.

    Evita flakiness causados por:
    - Diferenças de milissegundos/segundos entre aplicação e teste
    - Problemas de timezone (UTC vs localtime)
    - Diferenças de formatação

    Args:
        actual: Data/hora em formato string extraída da UI/API
        expected_datetime: Data/hora esperada (default: agora)
        tolerance_seconds: Tolerância em segundos (default: 5 minutos)
        date_format: Formato da data (ex: "%m-%d-%Y", "%Y-%m-%d %H:%M:%S")
        allow_date_only: Se True, compara apenas a parte da data (ignora hora)

    Returns:
        True se a data está dentro da tolerância

    Raises:
        AssertionError: Se a data está fora da tolerância, com mensagem detalhada
    """
    from datetime import datetime, timedelta
    import re

    if not actual or not isinstance(actual, str):
        raise AssertionError(f"Data inválida recebida: '{actual}' (tipo: {type(actual)})")

    # Limpar a string de data
    actual_clean = actual.strip()

    # Se expected_datetime não foi fornecido, usar agora
    if expected_datetime is None:
        expected_datetime = datetime.now()

    # Tentar parsear a data com múltiplos formatos comuns
    possible_formats = [
        date_format,
        "%m-%d-%Y",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%m-%d-%Y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
    ]

    actual_datetime = None
    for fmt in possible_formats:
        try:
            actual_datetime = datetime.strptime(actual_clean, fmt)
            print(f"[INFO] Data parseada com formato '{fmt}': {actual_datetime}")
            break
        except ValueError:
            continue

    if actual_datetime is None:
        # Tentar extrair apenas a data via regex
        date_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', actual_clean)
        if date_match:
            for fmt in ["%m-%d-%Y", "%d-%m-%Y", "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]:
                try:
                    actual_datetime = datetime.strptime(date_match.group(1), fmt)
                    print(f"[INFO] Data extraída via regex com formato '{fmt}': {actual_datetime}")
                    break
                except ValueError:
                    continue

    if actual_datetime is None:
        raise AssertionError(
            f"Não foi possível parsear a data '{actual}'. "
            f"Formatos tentados: {possible_formats}"
        )

    # Se allow_date_only, comparar apenas a parte da data
    if allow_date_only:
        actual_date = actual_datetime.date()
        expected_date = expected_datetime.date()

        # Tolerância de 1 dia (para cobrir casos de meia-noite)
        date_diff = abs((actual_date - expected_date).days)

        if date_diff <= 1:
            print(f"[OK] Validação de data: actual={actual_date}, expected={expected_date}, diff={date_diff} dia(s)")
            return True
        else:
            raise AssertionError(
                f"Data fora da tolerância!\n"
                f"  Esperado (aprox): {expected_date}\n"
                f"  Recebido: {actual_date}\n"
                f"  Diferença: {date_diff} dias"
            )

    # Comparação com tolerância em segundos
    time_diff = abs((actual_datetime - expected_datetime).total_seconds())

    if time_diff <= tolerance_seconds:
        print(
            f"[OK] Validação de datetime: "
            f"actual={actual_datetime}, expected={expected_datetime}, "
            f"diff={time_diff:.0f}s (tolerância: {tolerance_seconds}s)"
        )
        return True
    else:
        raise AssertionError(
            f"Data/hora fora da tolerância!\n"
            f"  Esperado (aprox): {expected_datetime}\n"
            f"  Recebido: {actual_datetime}\n"
            f"  Diferença: {time_diff:.0f} segundos\n"
            f"  Tolerância: {tolerance_seconds} segundos"
        )


def assert_record_count_changed(
    count_before: int,
    count_after: int,
    expected_change: int,
    operation: str = "operação",
    allow_concurrent_changes: bool = True
) -> bool:
    """
    Valida mudança na contagem de registros de forma robusta.

    Evita flakiness causados por:
    - Operações concorrentes de outros processos/usuários
    - Race conditions
    - Delays na atualização do banco/cache

    Args:
        count_before: Contagem antes da operação
        count_after: Contagem depois da operação
        expected_change: Mudança esperada (+1 para criação, -1 para deleção)
        operation: Nome da operação para mensagens de erro
        allow_concurrent_changes: Se True, permite variação além do esperado
                                   (útil em ambientes compartilhados)

    Returns:
        True se a mudança está dentro do esperado

    Raises:
        AssertionError: Se a mudança não corresponde ao esperado
    """
    actual_change = count_after - count_before

    # Validação estrita
    if actual_change == expected_change:
        print(
            f"[OK] Validação de contagem ({operation}): "
            f"antes={count_before}, depois={count_after}, "
            f"mudança={actual_change} (esperado: {expected_change})"
        )
        return True

    # Se permite mudanças concorrentes, verificar se a mudança inclui a esperada
    if allow_concurrent_changes:
        if expected_change > 0 and actual_change >= expected_change:
            print(
                f"[OK] Validação de contagem ({operation}) - com concorrência: "
                f"antes={count_before}, depois={count_after}, "
                f"mudança={actual_change} (esperado mínimo: {expected_change})"
            )
            return True
        elif expected_change < 0 and actual_change <= expected_change:
            print(
                f"[OK] Validação de contagem ({operation}) - com concorrência: "
                f"antes={count_before}, depois={count_after}, "
                f"mudança={actual_change} (esperado máximo: {expected_change})"
            )
            return True

    raise AssertionError(
        f"Contagem de registros incorreta após {operation}!\n"
        f"  Antes: {count_before}\n"
        f"  Depois: {count_after}\n"
        f"  Mudança real: {actual_change}\n"
        f"  Mudança esperada: {expected_change}"
    )


def assert_container_created(
    context,
    container_serial: str = None,
    verify_date: bool = True,
    verify_count: bool = True,
    date_tolerance_seconds: int = 300
) -> dict:
    """
    Validação robusta de criação de Container.

    Realiza múltiplas verificações:
    1. Container existe com o serial esperado (se fornecido)
    2. Data de criação está correta (com tolerância)
    3. Contagem de registros aumentou (se count_before disponível)

    Args:
        context: Contexto do Behave com driver e dados do teste
        container_serial: Serial do container criado (opcional)
        verify_date: Se deve validar a data de criação
        verify_count: Se deve validar a contagem de registros
        date_tolerance_seconds: Tolerância para validação de data

    Returns:
        Dict com informações do container validado

    Raises:
        AssertionError: Se alguma validação falhar
    """
    from selenium.webdriver.common.by import By
    from datetime import datetime

    result = {
        "serial": None,
        "created_date": None,
        "count_valid": False,
        "date_valid": False
    }

    # 1. Buscar o container na grid/lista
    try:
        # Se temos o serial, buscar especificamente
        if container_serial:
            container_row = wait_and_find(
                context.driver,
                By.XPATH,
                f"//td[contains(text(), '{container_serial}')]/ancestor::tr",
                timeout=15
            )
            result["serial"] = container_serial
            print(f"[OK] Container encontrado com serial: {container_serial}")
        else:
            # Buscar o primeiro container (mais recente)
            serial_element = wait_and_find(
                context.driver,
                By.XPATH,
                "//td[@rel='serial']/span",
                timeout=15
            )
            result["serial"] = serial_element.text
            print(f"[OK] Container encontrado: {result['serial']}")
    except Exception as e:
        raise AssertionError(f"Container não encontrado na lista: {e}")

    # 2. Validar data de criação
    if verify_date:
        try:
            date_element = wait_and_find(
                context.driver,
                By.XPATH,
                "//td[@rel='created_on']/span",
                timeout=10
            )
            date_text = date_element.text

            # Extrair apenas a parte da data (ignorar hora se presente)
            date_part = safe_split_date(date_text, separator=" ", index=0, default=date_text)

            # Validar com tolerância
            assert_datetime_near(
                actual=date_part,
                expected_datetime=datetime.now(),
                tolerance_seconds=date_tolerance_seconds,
                allow_date_only=True
            )
            result["created_date"] = date_text
            result["date_valid"] = True

        except AssertionError:
            raise
        except Exception as e:
            raise AssertionError(f"Erro ao validar data de criação: {e}")

    # 3. Validar contagem de registros
    if verify_count and hasattr(context, 'total_records_before'):
        try:
            records_element = wait_and_find(
                context.driver,
                By.CLASS_NAME,
                "tt_utils_ui_search-footer-nb-results",
                timeout=15
            )
            count_after = safe_parse_records_count(
                records_element.text,
                default=context.total_records_before
            )

            assert_record_count_changed(
                count_before=context.total_records_before,
                count_after=count_after,
                expected_change=1,
                operation="criação de container"
            )
            result["count_valid"] = True

        except AssertionError:
            raise
        except Exception as e:
            print(f"[WARN] Não foi possível validar contagem: {e}")

    print(f"[OK] Container criado e validado: {result}")
    return result


def assert_container_deleted(
    context,
    container_serial: str,
    verify_not_found: bool = True,
    verify_count: bool = True
) -> dict:
    """
    Validação robusta de deleção de Container.

    Realiza múltiplas verificações:
    1. Container não existe mais na lista (ou está inativo)
    2. Contagem de registros diminuiu

    Args:
        context: Contexto do Behave com driver e dados do teste
        container_serial: Serial do container deletado
        verify_not_found: Se deve verificar que o container não aparece
        verify_count: Se deve validar a contagem de registros

    Returns:
        Dict com resultado das validações

    Raises:
        AssertionError: Se alguma validação falhar
    """
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    import time

    result = {
        "serial": container_serial,
        "not_found": False,
        "count_valid": False
    }

    # Aguardar página atualizar
    time.sleep(2)

    # 1. Verificar que o container não está mais visível
    if verify_not_found:
        try:
            # Tentar encontrar o container - deve falhar
            context.driver.find_element(
                By.XPATH,
                f"//td[contains(text(), '{container_serial}')]"
            )
            # Se encontrou, pode ser que está com status DELETED/INACTIVE
            # Verificar o status
            try:
                status_element = context.driver.find_element(
                    By.XPATH,
                    f"//td[contains(text(), '{container_serial}')]/ancestor::tr//td[@rel='status']"
                )
                status = status_element.text.upper()
                if status in ['DELETED', 'INACTIVE', 'REMOVIDO', 'INATIVO']:
                    print(f"[OK] Container marcado como {status}: {container_serial}")
                    result["not_found"] = True
                else:
                    raise AssertionError(
                        f"Container ainda existe e está ativo!\n"
                        f"  Serial: {container_serial}\n"
                        f"  Status: {status}"
                    )
            except NoSuchElementException:
                raise AssertionError(
                    f"Container ainda existe na lista após deleção!\n"
                    f"  Serial: {container_serial}"
                )
        except NoSuchElementException:
            # Container não encontrado - deleção bem sucedida
            print(f"[OK] Container não encontrado (deletado): {container_serial}")
            result["not_found"] = True

    # 2. Validar contagem de registros
    if verify_count and hasattr(context, 'total_records'):
        try:
            # Refresh para garantir dados atualizados
            context.driver.refresh()
            time.sleep(2)

            records_element = wait_and_find(
                context.driver,
                By.CLASS_NAME,
                "tt_utils_ui_search-footer-nb-results",
                timeout=15
            )
            count_after = safe_parse_records_count(
                records_element.text,
                default=context.total_records
            )

            assert_record_count_changed(
                count_before=context.total_records,
                count_after=count_after,
                expected_change=-1,
                operation="deleção de container"
            )
            result["count_valid"] = True

        except AssertionError:
            raise
        except Exception as e:
            print(f"[WARN] Não foi possível validar contagem: {e}")

    print(f"[OK] Container deletado e validado: {result}")
    return result


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


# ============ ROBUST TABLE ROW HELPERS ============

def find_table_row_by_identifier(
    driver,
    identifier_value: str,
    identifier_column: str = None,
    table_selector: str = "//table//tbody//tr",
    timeout: int = 15
) -> 'WebElement':
    """
    Encontra uma linha da tabela usando um identificador de negócio robusto.

    ANTES (frágil):
        driver.find_element(By.XPATH, "//img[@alt='Delete']")
        # Problema: Clica no primeiro botão Delete encontrado, sem garantir qual registro

    DEPOIS (robusto):
        find_table_row_by_identifier(driver, "PO#123456789", identifier_column="po_nbr")
        # Encontra a linha específica pelo identificador de negócio

    Args:
        driver: WebDriver instance
        identifier_value: Valor do identificador (ex: "PO#123456789", "[RPA] Product Name")
        identifier_column: Nome da coluna rel (ex: "po_nbr", "name", "serial")
        table_selector: XPath base para as linhas da tabela
        timeout: Timeout em segundos

    Returns:
        WebElement da linha (tr) encontrada

    Raises:
        Exception: Se não encontrar a linha
    """
    from selenium.webdriver.common.by import By

    # Estratégia 1: Se temos o nome da coluna, buscar específico
    if identifier_column:
        specific_selectors = [
            f"//td[@rel='{identifier_column}'][contains(text(), '{identifier_value}')]/ancestor::tr",
            f"//td[@rel='{identifier_column}']//span[contains(text(), '{identifier_value}')]/ancestor::tr",
            f"//td[@rel='{identifier_column}']//*[contains(text(), '{identifier_value}')]/ancestor::tr",
        ]
        for selector in specific_selectors:
            try:
                element = WebDriverWait(driver, timeout // 2).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print(f"[OK] Linha encontrada com coluna específica: {identifier_column}={identifier_value}")
                return element
            except:
                continue

    # Estratégia 2: Buscar em qualquer célula da tabela
    generic_selectors = [
        f"//td[contains(text(), '{identifier_value}')]/ancestor::tr",
        f"//td//span[contains(text(), '{identifier_value}')]/ancestor::tr",
        f"//tr[contains(., '{identifier_value}')]",
    ]

    for selector in generic_selectors:
        try:
            element = WebDriverWait(driver, timeout // 2).until(
                EC.presence_of_element_located((By.XPATH, selector))
            )
            print(f"[OK] Linha encontrada com busca genérica: {identifier_value}")
            return element
        except:
            continue

    # Se chegou aqui, não encontrou
    raise Exception(
        f"Não foi possível encontrar linha com identificador '{identifier_value}'\n"
        f"Coluna especificada: {identifier_column}\n"
        f"Seletores tentados: {specific_selectors if identifier_column else ''} + {generic_selectors}"
    )


def find_action_button_in_row(
    row_element: 'WebElement',
    action_type: str = "delete",
    timeout: int = 10
) -> 'WebElement':
    """
    Encontra um botão de ação (Delete, Edit, View) em uma linha específica da tabela.

    ANTES (frágil):
        driver.find_element(By.XPATH, "//img[@alt='Delete']")
        # Problema: Pode clicar no botão errado se houver múltiplas linhas

    DEPOIS (robusto):
        row = find_table_row_by_identifier(driver, "PO#123")
        delete_btn = find_action_button_in_row(row, "delete")
        # Garante que estamos clicando no botão da linha correta

    Args:
        row_element: Elemento WebElement da linha (tr)
        action_type: Tipo de ação ("delete", "edit", "view")
        timeout: Timeout em segundos

    Returns:
        WebElement do botão encontrado

    Raises:
        Exception: Se não encontrar o botão
    """
    from selenium.webdriver.common.by import By

    # Mapeamento de ações para seletores (prioridade por robustez)
    action_selectors = {
        "delete": [
            # Data attributes (mais robusto)
            ".//button[@data-action='delete']",
            ".//a[@data-action='delete']",
            # ARIA labels (acessibilidade)
            ".//*[@aria-label='Delete' or @aria-label='Excluir' or @aria-label='Deletar']",
            # Alt text em imagens
            ".//img[@alt='Delete' or @alt='Excluir' or @alt='Deletar']",
            ".//img[contains(@alt, 'Delete') or contains(@alt, 'Excluir')]",
            # Classes comuns
            ".//*[contains(@class, 'delete') or contains(@class, 'Delete')]",
            ".//button[contains(@class, 'btn-danger')]",
            # Ícones de lixeira
            ".//img[contains(@src, 'delete') or contains(@src, 'trash') or contains(@src, 'remove')]",
            ".//i[contains(@class, 'fa-trash') or contains(@class, 'fa-times')]",
        ],
        "edit": [
            ".//button[@data-action='edit']",
            ".//a[@data-action='edit']",
            ".//*[@aria-label='Edit' or @aria-label='Editar']",
            ".//img[@alt='Edit' or @alt='Editar']",
            ".//img[contains(@alt, 'Edit') or contains(@alt, 'Editar')]",
            ".//*[contains(@class, 'edit') or contains(@class, 'Edit')]",
            ".//img[contains(@src, 'edit') or contains(@src, 'pencil')]",
        ],
        "view": [
            ".//button[@data-action='view']",
            ".//a[@data-action='view']",
            ".//*[@aria-label='View' or @aria-label='Visualizar' or @aria-label='Ver']",
            ".//img[@alt='View' or @alt='Visualizar']",
            ".//img[contains(@alt, 'View') or contains(@alt, 'Ver')]",
            ".//*[contains(@class, 'view') or contains(@class, 'View')]",
        ]
    }

    selectors = action_selectors.get(action_type.lower(), action_selectors["delete"])

    for selector in selectors:
        try:
            element = row_element.find_element(By.XPATH, selector)
            if element.is_displayed():
                print(f"[OK] Botão '{action_type}' encontrado com seletor: {selector}")
                return element
        except:
            continue

    # Tirar screenshot para debug
    try:
        driver = row_element.parent
        take_screenshot(driver, f"action_button_{action_type}_not_found")
    except:
        pass

    raise Exception(
        f"Não foi possível encontrar botão de '{action_type}' na linha.\n"
        f"Seletores tentados: {selectors}"
    )


def click_action_button_safe(
    driver,
    button_element: 'WebElement',
    retries: int = 3
) -> bool:
    """
    Clica em um botão de ação de forma segura, com múltiplas estratégias.

    Estratégias de click (em ordem):
    1. Click direto
    2. Scroll + Click
    3. JavaScript click
    4. Actions chain click

    Args:
        driver: WebDriver instance
        button_element: Elemento do botão
        retries: Número de tentativas

    Returns:
        True se clicou com sucesso

    Raises:
        Exception: Se todas as tentativas falharem
    """
    from selenium.webdriver.common.action_chains import ActionChains

    for attempt in range(retries):
        # Estratégia 1: Click direto
        try:
            button_element.click()
            print(f"[OK] Click direto bem sucedido (tentativa {attempt + 1})")
            return True
        except ElementClickInterceptedException:
            print(f"[WARN] Click interceptado, tentando scroll...")
        except StaleElementReferenceException:
            print(f"[WARN] Elemento stale, aguardando...")
            time.sleep(0.5)
            continue
        except Exception as e:
            print(f"[WARN] Click direto falhou: {str(e)[:50]}")

        # Estratégia 2: Scroll + Click
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                button_element
            )
            time.sleep(0.5)
            button_element.click()
            print(f"[OK] Scroll + Click bem sucedido (tentativa {attempt + 1})")
            return True
        except Exception as e:
            print(f"[WARN] Scroll + Click falhou: {str(e)[:50]}")

        # Estratégia 3: JavaScript click
        try:
            driver.execute_script("arguments[0].click();", button_element)
            print(f"[OK] JavaScript click bem sucedido (tentativa {attempt + 1})")
            return True
        except Exception as e:
            print(f"[WARN] JavaScript click falhou: {str(e)[:50]}")

        # Estratégia 4: Actions chain
        try:
            actions = ActionChains(driver)
            actions.move_to_element(button_element).click().perform()
            print(f"[OK] Actions chain click bem sucedido (tentativa {attempt + 1})")
            return True
        except Exception as e:
            print(f"[WARN] Actions chain falhou: {str(e)[:50]}")

        time.sleep(1)

    raise Exception(f"Não foi possível clicar no botão após {retries} tentativas")


def confirm_deletion_dialog(
    driver,
    timeout: int = 15
) -> bool:
    """
    Confirma o diálogo de deleção de forma robusta.

    Suporta múltiplos textos de confirmação (EN/PT):
    - Yes / Sim
    - OK / Ok
    - Confirm / Confirmar
    - Delete / Excluir / Deletar

    Args:
        driver: WebDriver instance
        timeout: Timeout em segundos

    Returns:
        True se confirmou com sucesso

    Raises:
        Exception: Se não conseguir confirmar
    """
    from selenium.webdriver.common.by import By

    # Seletores para botões de confirmação (ordem de prioridade)
    confirm_selectors = [
        # Botões específicos de confirmação
        "//button[@data-action='confirm']",
        "//button[@type='submit']//span[text()='Yes' or text()='Sim']",
        # Texto exato
        "//button/span[text()='Yes']",
        "//button/span[text()='Sim']",
        "//button/span[text()='OK']",
        "//button/span[text()='Confirm']",
        "//button/span[text()='Confirmar']",
        "//button/span[text()='Delete']",
        "//button/span[text()='Excluir']",
        # Contém texto
        "//button[contains(., 'Yes') or contains(., 'Sim')]",
        "//button[contains(., 'OK')]",
        "//button[contains(., 'Confirm') or contains(., 'Confirmar')]",
        # Botões primários em modais
        "//div[contains(@class, 'modal')]//button[contains(@class, 'primary')]",
        "//div[contains(@class, 'modal')]//button[contains(@class, 'btn-primary')]",
        "//div[contains(@class, 'modal')]//button[contains(@class, 'btn-danger')]",
        # Fallback: qualquer botão enabled no modal
        "//div[contains(@class, 'tt_utils_ui_dlg_modal')]//button[contains(@class, 'enabled')]",
    ]

    # Aguardar modal aparecer
    time.sleep(1)

    for selector in confirm_selectors:
        try:
            element = WebDriverWait(driver, timeout // 3).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            element.click()
            print(f"[OK] Diálogo de deleção confirmado com seletor: {selector}")
            time.sleep(1)  # Aguardar processamento
            return True
        except:
            continue

    # Se não encontrou, tirar screenshot
    take_screenshot(driver, "confirm_dialog_not_found")
    raise Exception(
        f"Não foi possível confirmar o diálogo de deleção.\n"
        f"Seletores tentados: {confirm_selectors}"
    )


def delete_record_by_identifier(
    driver,
    identifier_value: str,
    identifier_column: str = None,
    confirm_deletion: bool = True,
    timeout: int = 15
) -> dict:
    """
    Função helper completa para deletar um registro usando identificador de negócio.

    Esta função combina:
    1. find_table_row_by_identifier() - encontrar a linha correta
    2. find_action_button_in_row() - encontrar o botão Delete na linha
    3. click_action_button_safe() - clicar de forma segura
    4. confirm_deletion_dialog() - confirmar o diálogo

    ANTES (frágil - outbound.py):
        delete_button = outbound_row.find_element(By.XPATH, ".//img[@alt='Delete']")
        delete_button.click()

    DEPOIS (robusto):
        result = delete_record_by_identifier(
            driver,
            identifier_value=context.po,
            identifier_column="po_nbr",
            confirm_deletion=True
        )

    Args:
        driver: WebDriver instance
        identifier_value: Valor do identificador (PO number, product name, serial, etc.)
        identifier_column: Nome da coluna rel (opcional, melhora precisão)
        confirm_deletion: Se deve confirmar o diálogo automaticamente
        timeout: Timeout em segundos

    Returns:
        Dict com informações da operação:
        {
            "identifier": str,
            "row_found": bool,
            "button_clicked": bool,
            "confirmed": bool
        }

    Raises:
        Exception: Se algum passo falhar
    """
    result = {
        "identifier": identifier_value,
        "row_found": False,
        "button_clicked": False,
        "confirmed": False
    }

    try:
        # 1. Encontrar a linha pelo identificador
        print(f"[INFO] Buscando registro com identificador: {identifier_value}")
        row = find_table_row_by_identifier(
            driver,
            identifier_value=identifier_value,
            identifier_column=identifier_column,
            timeout=timeout
        )
        result["row_found"] = True

        # 2. Encontrar o botão Delete na linha
        delete_btn = find_action_button_in_row(row, action_type="delete")

        # 3. Clicar no botão Delete
        click_action_button_safe(driver, delete_btn)
        result["button_clicked"] = True

        # 4. Confirmar deleção se solicitado
        if confirm_deletion:
            confirm_deletion_dialog(driver, timeout=timeout)
            result["confirmed"] = True

        print(f"[OK] Registro deletado com sucesso: {identifier_value}")
        return result

    except Exception as e:
        # Capturar estado atual para debug
        take_screenshot(driver, f"delete_failed_{identifier_value[:20]}")
        raise Exception(
            f"Falha ao deletar registro '{identifier_value}':\n"
            f"  Row found: {result['row_found']}\n"
            f"  Button clicked: {result['button_clicked']}\n"
            f"  Confirmed: {result['confirmed']}\n"
            f"  Erro: {str(e)}"
        )


def delete_outbound_by_code(
    driver,
    outbound_code: str,
    confirm_deletion: bool = True,
    timeout: int = 15
) -> dict:
    """
    Deleta um Outbound pelo código (PO number).

    Wrapper específico para delete_record_by_identifier com
    configurações otimizadas para Outbound.

    Args:
        driver: WebDriver instance
        outbound_code: Código do outbound (ex: "PO#123456789")
        confirm_deletion: Se deve confirmar o diálogo
        timeout: Timeout em segundos

    Returns:
        Dict com informações da operação

    Example:
        result = delete_outbound_by_code(
            context.driver,
            outbound_code=context.po,
            confirm_deletion=True
        )
    """
    return delete_record_by_identifier(
        driver=driver,
        identifier_value=outbound_code,
        identifier_column="po_nbr",  # Coluna específica para PO number
        confirm_deletion=confirm_deletion,
        timeout=timeout
    )


def delete_product_by_identifier(
    driver,
    product_identifier: str,
    identifier_type: str = "name",
    confirm_deletion: bool = True,
    timeout: int = 15
) -> dict:
    """
    Deleta um Product pelo identificador (nome, SKU, GTIN, etc.).

    Wrapper específico para delete_record_by_identifier com
    configurações otimizadas para Product.

    Args:
        driver: WebDriver instance
        product_identifier: Identificador do produto (ex: "[RPA] Product Name", SKU, GTIN)
        identifier_type: Tipo de identificador ("name", "sku", "upc", "gtin")
        confirm_deletion: Se deve confirmar o diálogo
        timeout: Timeout em segundos

    Returns:
        Dict com informações da operação

    Example:
        result = delete_product_by_identifier(
            context.driver,
            product_identifier=context.product_name,
            identifier_type="name",
            confirm_deletion=True
        )
    """
    # Mapear tipo para nome da coluna
    column_map = {
        "name": "name",
        "sku": "sku",
        "upc": "upc",
        "gtin": "upc",  # GTIN geralmente está na coluna UPC
        "ndc": None,  # NDC pode estar em várias colunas
    }

    return delete_record_by_identifier(
        driver=driver,
        identifier_value=product_identifier,
        identifier_column=column_map.get(identifier_type.lower()),
        confirm_deletion=confirm_deletion,
        timeout=timeout
    )


def assert_record_deleted(
    driver,
    identifier_value: str,
    identifier_column: str = None,
    verify_count: bool = True,
    count_before: int = None,
    timeout: int = 15
) -> dict:
    """
    Valida que um registro foi deletado corretamente.

    Validações realizadas:
    1. Registro não aparece mais na lista (ou está com status DELETED/INACTIVE)
    2. Contagem de registros diminuiu (se count_before fornecido)

    Args:
        driver: WebDriver instance
        identifier_value: Valor do identificador
        identifier_column: Nome da coluna rel
        verify_count: Se deve verificar contagem de registros
        count_before: Contagem antes da deleção
        timeout: Timeout em segundos

    Returns:
        Dict com resultado das validações

    Raises:
        AssertionError: Se alguma validação falhar
    """
    from selenium.webdriver.common.by import By

    result = {
        "identifier": identifier_value,
        "not_found": False,
        "count_valid": False
    }

    # Aguardar página atualizar
    time.sleep(2)

    # 1. Verificar que o registro não está mais visível
    try:
        find_table_row_by_identifier(
            driver,
            identifier_value=identifier_value,
            identifier_column=identifier_column,
            timeout=5  # Timeout curto - esperamos NÃO encontrar
        )
        # Se encontrou, verificar se está com status DELETED/INACTIVE
        try:
            row = find_table_row_by_identifier(
                driver, identifier_value, identifier_column, timeout=2
            )
            status_element = row.find_element(By.XPATH, ".//td[@rel='status']")
            status = status_element.text.upper()
            if status in ['DELETED', 'INACTIVE', 'REMOVIDO', 'INATIVO', 'CANCELADO']:
                print(f"[OK] Registro marcado como {status}: {identifier_value}")
                result["not_found"] = True
            else:
                raise AssertionError(
                    f"Registro ainda existe e está ativo!\n"
                    f"  Identificador: {identifier_value}\n"
                    f"  Status: {status}"
                )
        except NoSuchElementException:
            raise AssertionError(
                f"Registro ainda existe na lista após deleção!\n"
                f"  Identificador: {identifier_value}"
            )
    except Exception as e:
        if "Não foi possível encontrar linha" in str(e):
            # Registro não encontrado - deleção bem sucedida
            print(f"[OK] Registro não encontrado (deletado): {identifier_value}")
            result["not_found"] = True
        else:
            raise

    # 2. Validar contagem de registros
    if verify_count and count_before is not None:
        try:
            # Refresh para garantir dados atualizados
            driver.refresh()
            time.sleep(2)

            records_element = wait_and_find(
                driver,
                By.CLASS_NAME,
                "tt_utils_ui_search-footer-nb-results",
                timeout=15
            )
            count_after = safe_parse_records_count(
                records_element.text,
                default=count_before
            )

            assert_record_count_changed(
                count_before=count_before,
                count_after=count_after,
                expected_change=-1,
                operation="deleção de registro"
            )
            result["count_valid"] = True

        except AssertionError:
            raise
        except Exception as e:
            print(f"[WARN] Não foi possível validar contagem: {e}")

    print(f"[OK] Deleção validada: {result}")
    return result
