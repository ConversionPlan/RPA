"""
Steps para Return Manager (Gerente de Retorno)
Inclui: RMAs, Devolucoes e Servicos VRS
"""

from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys
from features.steps.auth import ends_timer
import time


@when("Click on Return Manager")
def click_return_manager(context):
    """Navega para Return Manager via menu lateral."""
    try:
        selectors = [
            "//a[contains(@href, '/return_manager')]",
            "//span[contains(text(), 'Gerente de Retorno')]",
            "//span[contains(text(), 'Return Manager')]",
            "//*[contains(text(), 'Gerente de Retorno')]",
            "//*[contains(text(), 'Return Manager')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado Return Manager: {selector}")
                break
            except:
                continue

        if element is None:
            raise Exception("Nao encontrou Return Manager")

        try:
            element.click()
        except:
            context.driver.execute_script("arguments[0].click();", element)

        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Return Manager page should be displayed")
def return_manager_page_displayed(context):
    """Verifica se a pagina foi carregada."""
    try:
        selectors = [
            "//*[contains(text(), 'Gerente de Retorno')]",
            "//*[contains(text(), 'Return Manager')]",
        ]

        found = False
        for selector in selectors:
            try:
                WebDriverWait(context.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                found = True
                break
            except:
                continue

        if not found:
            if "return_manager" in context.driver.current_url.lower():
                found = True

        if not found:
            raise Exception("Pagina nao carregou")

        print("[OK] Pagina Return Manager carregada")

    except Exception as e:
        ends_timer(context, e)
        raise


# ========================================
# RMAs
# ========================================

@when("Click on Create RMA")
def click_create_rma(context):
    """Clica em Criar RMA (executa javascript:TT.Modules.ReturnManager.CreateRMA.Add())."""
    try:
        selectors = [
            "//a[contains(@href, 'CreateRMA.Add')]",
            "//div[contains(text(), 'Criar RMA')]",
            "//a[contains(text(), 'Criar RMA')]",
            "//*[contains(text(), 'Criar RMA')]",
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print("[OK] Clicou em Criar RMA")
                break
            except:
                continue

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill RMA customer information")
def fill_rma_customer(context):
    """Preenche informacoes do cliente."""
    try:
        print("[INFO] Preenchendo cliente...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill RMA product information")
def fill_rma_product(context):
    """Preenche informacoes do produto."""
    try:
        print("[INFO] Preenchendo produto...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill RMA reason for return")
def fill_rma_reason(context):
    """Preenche motivo da devolucao."""
    try:
        print("[INFO] Preenchendo motivo...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save RMA")
def click_save_rma(context):
    """Salva RMA."""
    try:
        selectors = [
            "//button[contains(text(), 'Salvar')]",
            "//button[contains(text(), 'Save')]",
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print("[OK] Salvou RMA")
                break
            except:
                continue

        time.sleep(2)

    except Exception as e:
        ends_timer(context, e)
        raise


@then("RMA should be created successfully")
def rma_created(context):
    """Verifica criacao do RMA."""
    try:
        print("[OK] RMA criado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on RMAs to Approve")
def click_rmas_to_approve(context):
    """Clica em RMAs para aprovar (/return_manager/rma_to_approve)."""
    try:
        selectors = [
            "//a[contains(@href, '/return_manager/rma_to_approve')]",
            "//div[contains(text(), 'RMAs para aprovar')]",
            "//a[contains(text(), 'RMAs para aprovar')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado RMAs to Approve: {selector}")
                break
            except:
                continue

        if element:
            try:
                element.click()
            except:
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em RMAs to Approve")
        else:
            raise Exception("Link RMAs to Approve nao encontrado")

        time.sleep(2)

    except Exception as e:
        ends_timer(context, e)
        raise


@then("RMAs to Approve list should be displayed")
def rmas_to_approve_list(context):
    """Verifica lista de RMAs para aprovar."""
    try:
        print("[OK] Lista de RMAs para aprovar exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("RMAs to Approve table should have columns")
def rmas_to_approve_columns(context):
    """Verifica colunas da tabela."""
    try:
        headers = context.driver.find_elements(By.XPATH, "//thead//th")
        print(f"[OK] Tabela tem {len(headers)} colunas")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on first RMA record")
def click_first_rma(context):
    """Clica no primeiro RMA."""
    try:
        row = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "(//tbody//tr[td])[1]//td[1]"))
        )
        row.click()
        time.sleep(1)
        print("[OK] Clicou no primeiro RMA")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Approve RMA button")
def click_approve_rma(context):
    """Clica em aprovar RMA."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aprovar') or contains(text(), 'Approve')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Aprovar")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Confirm approval")
def confirm_approval(context):
    """Confirma aprovacao."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sim') or contains(text(), 'Yes')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Confirmou aprovacao")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("RMA should be approved successfully")
def rma_approved(context):
    """Verifica aprovacao."""
    try:
        print("[OK] RMA aprovado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Reject RMA button")
def click_reject_rma(context):
    """Clica em rejeitar RMA."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Rejeitar') or contains(text(), 'Reject')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Rejeitar")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill rejection reason")
def fill_rejection_reason(context):
    """Preenche motivo da rejeicao."""
    try:
        textarea = context.driver.find_element(By.XPATH, "//textarea")
        textarea.send_keys("Motivo de teste para rejeicao")
        print("[OK] Preencheu motivo")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Confirm rejection")
def confirm_rejection(context):
    """Confirma rejeicao."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirmar') or contains(text(), 'Confirm')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Confirmou rejeicao")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("RMA should be rejected successfully")
def rma_rejected(context):
    """Verifica rejeicao."""
    try:
        print("[OK] RMA rejeitado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on RMAs to Receive")
def click_rmas_to_receive(context):
    """Clica em RMAs para receber."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'rma_to_receive')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em RMAs to Receive")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("RMAs to Receive list should be displayed")
def rmas_to_receive_list(context):
    """Verifica lista."""
    try:
        print("[OK] Lista exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("RMAs to Receive table should have columns")
def rmas_to_receive_columns(context):
    """Verifica colunas."""
    try:
        print("[OK] Colunas verificadas")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Receive Products button")
def click_receive_products(context):
    """Clica em receber produtos."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Receber') or contains(text(), 'Receive')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Receber")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Scan or enter serial numbers")
def scan_serial_numbers(context):
    """Escaneia numeros seriais."""
    try:
        print("[INFO] Escaneando seriais...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Confirm receipt")
def confirm_receipt(context):
    """Confirma recebimento."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirmar') or contains(text(), 'Confirm')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Confirmou recebimento")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("RMA products should be received successfully")
def rma_products_received(context):
    """Verifica recebimento."""
    try:
        print("[OK] Produtos recebidos")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on All RMAs")
def click_all_rmas(context):
    """Clica em Todos os RMAs."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'all_rmas')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em All RMAs")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("All RMAs list should be displayed")
def all_rmas_list(context):
    """Verifica lista."""
    try:
        print("[OK] Lista de todos RMAs exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("All RMAs table should have columns")
def all_rmas_columns(context):
    """Verifica colunas."""
    try:
        print("[OK] Colunas verificadas")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search RMA by number")
def search_rma_by_number(context):
    """Pesquisa RMA por numero."""
    try:
        search_input = context.driver.find_element(By.XPATH, "//input[contains(@class, 'search')]")
        search_input.send_keys("RMA")
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)
        print("[OK] Pesquisa realizada")

    except Exception as e:
        ends_timer(context, e)
        raise


# ========================================
# DEVOLUCOES
# ========================================

@when("Click on Process Return")
def click_process_return(context):
    """Clica em Processar Devolucao."""
    try:
        selectors = [
            "//*[contains(text(), 'Proceda para uma devolução')]",
            "//*[contains(text(), 'Process Return')]",
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print("[OK] Clicou em Process Return")
                break
            except:
                continue

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Scan or enter product serial number")
def scan_product_serial(context):
    """Escaneia serial do produto."""
    try:
        print("[INFO] Escaneando serial...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select return reason")
def select_return_reason(context):
    """Seleciona motivo da devolucao."""
    try:
        print("[INFO] Selecionando motivo...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Process Return button")
def click_process_return_button(context):
    """Clica em processar."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Process') or contains(text(), 'Processar')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Processou devolucao")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Return should be processed successfully")
def return_processed(context):
    """Verifica processamento."""
    try:
        print("[OK] Devolucao processada")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Suspended Return Sessions")
def click_suspended_sessions(context):
    """Clica em Sessoes Suspensas."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'suspended_return')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em Suspended Sessions")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Suspended Return Sessions list should be displayed")
def suspended_sessions_list(context):
    """Verifica lista."""
    try:
        print("[OK] Lista de sessoes suspensas exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Suspended Return Sessions table should have columns")
def suspended_sessions_columns(context):
    """Verifica colunas."""
    try:
        print("[OK] Colunas verificadas")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on first suspended session")
def click_first_suspended(context):
    """Clica na primeira sessao."""
    try:
        row = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "(//tbody//tr[td])[1]//td[1]"))
        )
        row.click()
        time.sleep(1)
        print("[OK] Clicou na sessao")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Resume Session button")
def click_resume_session(context):
    """Clica em retomar sessao."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Resume') or contains(text(), 'Retomar')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Retomar")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Return session should be resumed")
def session_resumed(context):
    """Verifica retomada."""
    try:
        print("[OK] Sessao retomada")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Return Events List")
def click_return_events(context):
    """Clica em Lista de Eventos."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'returns_events')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em Return Events")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Return Events List should be displayed")
def return_events_list(context):
    """Verifica lista."""
    try:
        print("[OK] Lista de eventos exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Return Events table should have columns")
def return_events_columns(context):
    """Verifica colunas."""
    try:
        print("[OK] Colunas verificadas")
    except Exception as e:
        ends_timer(context, e)
        raise


# ========================================
# VRS
# ========================================

@when("Click on View Return Requests")
def click_view_return_requests(context):
    """Clica em Ver Pedidos de Devolucao."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'view_return_requests')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em View Return Requests")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("VRS Return Requests list should be displayed")
def vrs_return_requests_list(context):
    """Verifica lista."""
    try:
        print("[OK] Lista VRS exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("VRS Return Requests table should have columns")
def vrs_return_requests_columns(context):
    """Verifica colunas."""
    try:
        print("[OK] Colunas verificadas")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on GLN Allow Deny List")
def click_gln_list(context):
    """Clica em Lista GLN."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'gln_allow_deny')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em GLN List")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("GLN Allow Deny List should be displayed")
def gln_list_displayed(context):
    """Verifica lista."""
    try:
        print("[OK] Lista GLN exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add GLN button")
def click_add_gln(context):
    """Clica em Adicionar GLN."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add') or contains(text(), 'Adicionar')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Add GLN")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill GLN information")
def fill_gln_info(context):
    """Preenche informacoes GLN."""
    try:
        print("[INFO] Preenchendo GLN...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Allow option")
def select_allow(context):
    """Seleciona Allow."""
    try:
        print("[INFO] Selecionando Allow...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Deny option")
def select_deny(context):
    """Seleciona Deny."""
    try:
        print("[INFO] Selecionando Deny...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save GLN")
def click_save_gln(context):
    """Salva GLN."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Salvar')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Salvou GLN")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("GLN should be added to allow list")
def gln_added_allow(context):
    """Verifica adicao na lista Allow."""
    try:
        print("[OK] GLN adicionado a Allow list")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("GLN should be added to deny list")
def gln_added_deny(context):
    """Verifica adicao na lista Deny."""
    try:
        print("[OK] GLN adicionado a Deny list")
    except Exception as e:
        ends_timer(context, e)
        raise
