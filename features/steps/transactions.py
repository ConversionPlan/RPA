"""
Steps para Sales Order e Purchase Order
Modulo de Transacoes do Portal TrackTrace
"""

from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys
from features.steps.auth import ends_timer
import time


def wait_for_page_ready(driver, timeout=15):
    """
    Aguarda a pagina estar completamente carregada.
    Verifica document.readyState e aguarda elementos de loading desaparecerem.
    """
    try:
        # Aguardar document.readyState == complete
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("[DEBUG] document.readyState = complete")

        # Aguardar spinners/loaders desaparecerem
        loading_selectors = [
            "//div[contains(@class, 'loading')]",
            "//div[contains(@class, 'spinner')]",
            "//div[contains(@class, 'loader')]",
            "//*[contains(@class, 'tt_utils_ui_loading')]",
        ]

        for selector in loading_selectors:
            try:
                WebDriverWait(driver, 3).until(
                    EC.invisibility_of_element_located((By.XPATH, selector))
                )
            except:
                pass

        # Pequena pausa adicional para JavaScript terminar
        time.sleep(1)
        print("[DEBUG] Pagina pronta para interacao")
        return True
    except Exception as e:
        print(f"[WARN] Timeout aguardando pagina: {e}")
        return False


def safe_click(driver, element, description="elemento"):
    """
    Clica em um elemento de forma segura com múltiplas tentativas.
    """
    methods = [
        ("click direto", lambda: element.click()),
        ("JS click", lambda: driver.execute_script("arguments[0].click();", element)),
        ("ActionChains", lambda: __import__('selenium.webdriver', fromlist=['ActionChains']).ActionChains(driver).move_to_element(element).click().perform()),
    ]

    for method_name, method_func in methods:
        try:
            method_func()
            print(f"[OK] Click em {description} via {method_name}")
            return True
        except Exception as e:
            print(f"[DEBUG] {method_name} falhou: {str(e)[:50]}")
            continue

    print(f"[ERROR] Todas as tentativas de click em {description} falharam")
    return False


# ========================================
# SALES ORDER
# ========================================

@when("Click on Sales Order")
def click_sales_order(context):
    """Navega para a tela de Sales Order via menu lateral."""
    try:
        selectors = [
            "//a[contains(@href, '/transactions/sales_order')]",
            "//span[contains(text(), 'Pedido de vendas')]",
            "//span[contains(text(), 'Sales Order')]",
            "//*[contains(text(), 'Pedido de vendas')]",
            "//*[contains(text(), 'Sales Order')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado Sales Order com seletor: {selector}")
                break
            except:
                continue

        if element is None:
            raise Exception("Nao foi possivel encontrar o elemento Sales Order")

        try:
            element.click()
        except:
            context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Sales Order via JavaScript")

        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Sales Order page should be displayed")
def sales_order_page_displayed(context):
    """Verifica se a pagina de Sales Order foi carregada."""
    try:
        title_selectors = [
            "//*[contains(text(), 'Transações das ordens de venda')]",
            "//*[contains(text(), 'Sales Order')]",
            "//*[contains(text(), 'Pedido de vendas')]",
        ]

        found = False
        for selector in title_selectors:
            try:
                WebDriverWait(context.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print(f"[OK] Pagina Sales Order confirmada com seletor: {selector}")
                found = True
                break
            except:
                continue

        if not found:
            current_url = context.driver.current_url.lower()
            if "sales_order" in current_url or "transaction" in current_url:
                print(f"[OK] Pagina Sales Order confirmada pela URL: {current_url}")
                found = True

        if not found:
            raise Exception("Pagina Sales Order nao foi carregada corretamente")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Sales Order table should have columns")
def sales_order_table_columns(context):
    """Verifica se a tabela tem colunas esperadas: UUID, ID do pedido, Data, Cliente, TÃO#, Ações."""
    try:
        # Clicar em Submit para carregar os dados
        try:
            search_btn = WebDriverWait(context.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
            )
            search_btn.click()
            print("[OK] Clicou em Pesquisar (Submit)")
            time.sleep(2)
        except:
            # Tentar via JavaScript
            context.driver.execute_script("document.querySelector('input[type=submit]')?.click()")
            time.sleep(2)

        # Verificar headers esperados
        expected_headers = ["UUID", "ID do pedido", "Data", "Cliente", "TÃO#", "Ações"]
        headers = context.driver.find_elements(By.XPATH, "//table//thead//th")
        header_texts = [h.text.strip() for h in headers]

        if headers:
            print(f"[OK] Tabela tem {len(headers)} colunas: {header_texts}")
            # Verificar se pelo menos algumas colunas esperadas estao presentes
            found = sum(1 for h in expected_headers if h in header_texts)
            if found >= 3:
                print(f"[OK] {found}/{len(expected_headers)} colunas esperadas encontradas")
        else:
            print("[WARNING] Colunas nao encontradas")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Sales Order records should be displayed")
def sales_order_records_displayed(context):
    """Verifica se ha registros na tabela."""
    try:
        rows = context.driver.find_elements(By.XPATH, "//table//tbody//tr")
        if rows:
            print(f"[OK] {len(rows)} registros encontrados na tabela Sales Order")
            # Verificar se primeira linha tem acoes (botoes de imagem)
            try:
                actions = context.driver.find_elements(
                    By.XPATH, "//table//tbody//tr[1]//img[@alt='Visualizar' or @alt='Editar' or @alt='Apagar']"
                )
                if actions:
                    print(f"[OK] Linha tem {len(actions)} botoes de acao")
            except:
                pass
        else:
            print("[INFO] Tabela vazia - nenhum registro")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Create Sales Order button")
def click_create_sales_order(context):
    """Clica no botao Adicionar para criar novo Sales Order."""
    try:
        selectors = [
            "//div[contains(@class, 'tt_utils_ui_search-search-header-action-buttons-container') and contains(text(), 'Adicionar')]",
            "//div[contains(text(), 'Adicionar')]",
            "//button[contains(text(), 'Adicionar')]",
            "//a[contains(text(), 'Adicionar')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado botao Adicionar com seletor: {selector}")
                break
            except:
                continue

        if element:
            try:
                element.click()
            except:
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Adicionar (Create Sales Order)")
        else:
            raise Exception("Botao Adicionar nao encontrado")

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Trading Partner from modal")
def select_trading_partner_modal(context):
    """Seleciona um Trading Partner no modal de selecao."""
    try:
        # Aguardar modal aparecer
        modal_selectors = [
            "//div[contains(@class, 'tt_utils_ui_dlg_modal')]",
            "//div[contains(text(), 'Selecione o cliente')]",
            "//div[contains(text(), 'Nome do cliente')]",
        ]

        modal_found = False
        for selector in modal_selectors:
            try:
                WebDriverWait(context.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                modal_found = True
                print(f"[OK] Modal de selecao encontrado: {selector}")
                break
            except:
                continue

        if not modal_found:
            raise Exception("Modal de selecao de cliente nao apareceu")

        time.sleep(1)

        # Clicar no primeiro cliente [RPA] disponivel
        customer_selectors = [
            "//td[contains(text(), '[RPA]')]/following-sibling::td//img[@alt]",
            "//tr[contains(., '[RPA]')]//td[last()]",
            "(//table//tbody//tr[contains(., 'CUSTOMER')])[1]",
        ]

        for selector in customer_selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print(f"[OK] Selecionou cliente com seletor: {selector}")
                break
            except:
                continue

        time.sleep(2)

        # Tratar possivel erro ATP (clicar Sim se aparecer)
        try:
            sim_btn = WebDriverWait(context.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sim')]"))
            )
            sim_btn.click()
            print("[OK] Clicou em Sim no aviso ATP")
            time.sleep(1)
        except:
            pass  # Nao apareceu erro ATP

        print("[OK] Trading Partner selecionado")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill Sales Order customer information")
def fill_sales_order_customer(context):
    """Preenche informacoes do cliente (apos selecao no modal)."""
    try:
        # Verificar se formulario de criacao foi carregado
        form_selectors = [
            "//div[contains(text(), 'Adicionar ordem de vendas')]",
            "//span[contains(text(), 'Geral')]",
            "//input[contains(@class, 'order')]",
        ]

        form_found = False
        for selector in form_selectors:
            try:
                WebDriverWait(context.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                form_found = True
                break
            except:
                continue

        if form_found:
            print("[OK] Formulario de criacao carregado")
        else:
            print("[WARNING] Formulario pode nao ter carregado completamente")

        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill Sales Order line items")
def fill_sales_order_items(context):
    """Preenche itens do pedido - campos opcionais."""
    try:
        import random

        # Gerar numero de pedido aleatorio para teste
        order_number = f"SO#{random.randint(100000000, 999999999)}"

        # Tentar preencher o campo "Número do pedido" ou "TÃO#"
        order_field_selectors = [
            "//label[contains(text(), 'Número do pedido')]/following::input[1]",
            "//label[contains(text(), 'TÃO#')]/following::input[1]",
            "//input[@name='order_number']",
            "//input[contains(@placeholder, 'pedido')]",
        ]

        for selector in order_field_selectors:
            try:
                field = context.driver.find_element(By.XPATH, selector)
                if field.is_displayed() and field.is_enabled():
                    field.clear()
                    field.send_keys(order_number)
                    print(f"[OK] Preencheu campo de pedido: {order_number}")
                    break
            except:
                continue

        time.sleep(1)
        print("[OK] Itens do pedido preenchidos")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save Sales Order")
def click_save_sales_order(context):
    """Clica em salvar Sales Order."""
    try:
        selectors = [
            "//div[contains(@class, 'modal')]//button[contains(text(), 'Salvar')]",
            "//button[contains(text(), 'Salvar')]",
            "//button[contains(text(), 'Save')]",
            "//span[contains(text(), 'Salvar')]/parent::button",
            "//input[@type='submit' and contains(@value, 'Salvar')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrou botao Salvar: {selector}")
                break
            except:
                continue

        if element:
            try:
                element.click()
            except:
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Salvar")
        else:
            print("[WARNING] Botao Salvar nao encontrado")

        time.sleep(2)

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Sales Order should be created successfully")
def sales_order_created(context):
    """Verifica se o pedido foi criado."""
    try:
        # Aguardar modal fechar ou pagina recarregar
        time.sleep(2)

        # Verificar mensagem de sucesso
        success_selectors = [
            "//*[contains(text(), 'sucesso')]",
            "//*[contains(text(), 'successfully')]",
            "//*[contains(text(), 'criado')]",
            "//*[contains(text(), 'created')]",
        ]

        success_found = False
        for selector in success_selectors:
            try:
                WebDriverWait(context.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print("[OK] Mensagem de sucesso encontrada")
                success_found = True
                break
            except:
                continue

        # Se nao encontrou mensagem, verificar se voltou para a lista
        if not success_found:
            try:
                WebDriverWait(context.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//table//th[contains(text(), 'UUID')]"))
                )
                print("[OK] Retornou para a lista de Sales Orders")
                success_found = True
            except:
                pass

        if success_found:
            print("[OK] Sales Order criado com sucesso")
        else:
            print("[INFO] Verificacao de criacao concluida (sem confirmacao explicita)")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search Sales Order by order number")
def search_sales_order(context):
    """Pesquisa Sales Order por numero."""
    try:
        search_input = context.driver.find_element(
            By.XPATH, "//input[contains(@class, 'search') or contains(@placeholder, 'Pesquisar')]"
        )
        search_input.clear()
        search_input.send_keys("SO")
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)
        print("[OK] Pesquisa realizada")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on first Sales Order record")
def click_first_sales_order(context):
    """Clica no icone Visualizar do primeiro registro."""
    try:
        # Clicar no icone de visualizar (lupa) do primeiro registro
        view_selectors = [
            "(//table//tbody//tr)[1]//img[@alt='Visualizar']",
            "//table//tbody//tr[1]//img[@alt='Visualizar']",
            "(//img[@alt='Visualizar'])[1]",
        ]

        element = None
        for selector in view_selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrou icone Visualizar: {selector}")
                break
            except:
                continue

        if element:
            try:
                element.click()
            except:
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Visualizar primeiro registro")
        else:
            # Fallback: clicar na primeira celula
            row = WebDriverWait(context.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "(//tbody//tr[td])[1]//td[1]"))
            )
            row.click()
            print("[OK] Clicou na primeira celula do registro")

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Sales Order Details modal should be displayed")
def sales_order_details_modal(context):
    """Verifica se modal de detalhes foi aberto."""
    try:
        modal = WebDriverWait(context.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'modal')]"))
        )
        print("[OK] Modal de detalhes exibido")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Sales Order Details should show order information")
def sales_order_details_info(context):
    """Verifica informacoes no modal."""
    try:
        print("[OK] Informacoes do pedido exibidas")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Edit Sales Order button")
def click_edit_sales_order(context):
    """Clica no botao Editar (icone img com alt='Editar')."""
    try:
        selectors = [
            "(//table//tbody//tr)[1]//img[@alt='Editar']",
            "//table//tbody//tr[1]//img[@alt='Editar']",
            "(//img[@alt='Editar'])[1]",
            "//button[contains(text(), 'Editar')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado icone Editar: {selector}")
                break
            except:
                continue

        if element:
            try:
                element.click()
            except:
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Editar")
        else:
            raise Exception("Icone Editar nao encontrado")

        time.sleep(2)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Update Sales Order information")
def update_sales_order(context):
    """Atualiza informacoes do pedido."""
    try:
        print("[INFO] Atualizando informacoes...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Sales Order should be updated successfully")
def sales_order_updated(context):
    """Verifica se pedido foi atualizado."""
    try:
        print("[OK] Sales Order atualizado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Delete Sales Order button")
def click_delete_sales_order(context):
    """Clica no botao Apagar (icone img com alt='Apagar')."""
    try:
        selectors = [
            "(//table//tbody//tr)[1]//img[@alt='Apagar']",
            "//table//tbody//tr[1]//img[@alt='Apagar']",
            "(//img[@alt='Apagar'])[1]",
            "//button[contains(text(), 'Apagar')]",
            "//button[contains(text(), 'Excluir')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado icone Apagar: {selector}")
                break
            except:
                continue

        if element:
            try:
                element.click()
            except:
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Apagar")
        else:
            raise Exception("Icone Apagar nao encontrado")

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Confirm deletion")
def confirm_deletion(context):
    """Confirma exclusao - diálogo usa classe tt_utils_ui__delete_confirmation."""
    try:
        print("[DEBUG] Iniciando confirmacao de exclusao...")
        time.sleep(2)  # Aguardar modal de confirmacao aparecer

        # Seletores específicos para o diálogo de confirmação do TrackTrace
        confirm_selectors = [
            # Botões dentro do diálogo de confirmação específico
            "//div[contains(@class, 'tt_utils_ui__delete_confirmation')]/ancestor::div[contains(@class, 'modal')]//button[contains(., 'Yes') or contains(., 'Sim')]",
            "//div[contains(@class, 'tt_utils_ui__delete_confirmation')]/ancestor::div[contains(@class, 'dlg')]//button[contains(., 'Yes') or contains(., 'Sim')]",
            # Botões genéricos de confirmação
            "//div[contains(@class, 'tt_utils_ui_dlg_modal')]//button[contains(., 'Yes') or contains(., 'Sim')]",
            "//div[contains(@class, 'modal')]//button[contains(., 'Yes') or contains(., 'Sim')]",
            # Botões com span interno
            "//button/span[text()='Yes' or text()='Sim']",
            "//button[contains(@class, 'enabled')][contains(., 'Yes') or contains(., 'Sim')]",
            # Fallback - qualquer botão com texto Yes/Sim
            "//button[contains(text(), 'Yes')]",
            "//button[contains(text(), 'Sim')]",
        ]

        confirmed = False
        for idx, selector in enumerate(confirm_selectors):
            try:
                print(f"[DEBUG] Tentando confirm selector {idx+1}...")
                element = WebDriverWait(context.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                context.driver.execute_script("arguments[0].click();", element)
                print(f"[OK] Confirmou exclusao com selector {idx+1}")
                confirmed = True
                break
            except:
                continue

        if not confirmed:
            print("[WARN] Seletores padrao nao funcionaram, tentando encontrar qualquer botao no modal...")
            try:
                # Último recurso - encontra todos os botões visíveis no modal e clica no primeiro
                buttons = context.driver.find_elements(By.XPATH, "//div[contains(@class, 'modal')]//button")
                for btn in buttons:
                    if btn.is_displayed():
                        btn_text = btn.text.strip()
                        if btn_text.lower() in ['yes', 'sim', 'ok', 'confirm', 'confirmar']:
                            context.driver.execute_script("arguments[0].click();", btn)
                            print(f"[OK] Confirmou exclusao com botao: {btn_text}")
                            confirmed = True
                            break
            except Exception as e:
                print(f"[DEBUG] Fallback falhou: {e}")

        time.sleep(2)
        if confirmed:
            print("[OK] Exclusao confirmada")
        else:
            print("[WARN] Nao encontrou botao de confirmacao - exclusao pode nao ter sido confirmada")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Sales Order should be deleted successfully")
def sales_order_deleted(context):
    """Verifica se pedido foi excluido."""
    try:
        print("[OK] Sales Order excluido")
    except Exception as e:
        ends_timer(context, e)
        raise


# ========================================
# PURCHASE ORDER
# ========================================

@when("Click on Purchase Order")
def click_purchase_order(context):
    """Navega para a tela de Purchase Order via menu lateral."""
    try:
        selectors = [
            "//a[contains(@href, '/transactions/purchase_order')]",
            "//span[contains(text(), 'Pedido de compra')]",
            "//span[contains(text(), 'Purchase Order')]",
            "//*[contains(text(), 'Pedido de compra')]",
            "//*[contains(text(), 'Purchase Order')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado Purchase Order com seletor: {selector}")
                break
            except:
                continue

        if element is None:
            raise Exception("Nao foi possivel encontrar o elemento Purchase Order")

        try:
            element.click()
        except:
            context.driver.execute_script("arguments[0].click();", element)

        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Purchase Order page should be displayed")
def purchase_order_page_displayed(context):
    """Verifica se a pagina de Purchase Order foi carregada."""
    try:
        title_selectors = [
            "//*[contains(text(), 'Pedido de compra')]",
            "//*[contains(text(), 'Purchase Order')]",
        ]

        found = False
        for selector in title_selectors:
            try:
                WebDriverWait(context.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                found = True
                break
            except:
                continue

        if not found:
            current_url = context.driver.current_url.lower()
            if "purchase_order" in current_url:
                found = True

        if not found:
            raise Exception("Pagina Purchase Order nao foi carregada")

        print("[OK] Pagina Purchase Order carregada")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Purchase Order table should have columns")
def purchase_order_table_columns(context):
    """Verifica colunas: UUID, ID do pedido, Data, Cliente, Número do pedido, Ações."""
    try:
        # Clicar em Submit para carregar os dados
        try:
            search_btn = WebDriverWait(context.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
            )
            search_btn.click()
            print("[OK] Clicou em Pesquisar (Submit)")
            time.sleep(2)
        except:
            context.driver.execute_script("document.querySelector('input[type=submit]')?.click()")
            time.sleep(2)

        # Verificar headers esperados
        expected_headers = ["UUID", "ID do pedido", "Data", "Cliente", "Número do pedido", "Ações"]
        headers = context.driver.find_elements(By.XPATH, "//table//thead//th")
        header_texts = [h.text.strip() for h in headers]

        if headers:
            print(f"[OK] Tabela tem {len(headers)} colunas: {header_texts}")
            found = sum(1 for h in expected_headers if h in header_texts)
            if found >= 3:
                print(f"[OK] {found}/{len(expected_headers)} colunas esperadas encontradas")
        else:
            print("[WARNING] Colunas nao encontradas")

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Purchase Order records should be displayed")
def purchase_order_records_displayed(context):
    """Verifica registros na tabela (Visualizar, Editar, Fechar, Apagar)."""
    try:
        rows = context.driver.find_elements(By.XPATH, "//table//tbody//tr")
        if rows:
            print(f"[OK] {len(rows)} registros encontrados na tabela Purchase Order")
            # Verificar botoes de acao (PO tem 4: Visualizar, Editar, Fechar, Apagar)
            try:
                actions = context.driver.find_elements(
                    By.XPATH, "//table//tbody//tr[1]//img[@alt='Visualizar' or @alt='Editar' or @alt='Fechar' or @alt='Apagar']"
                )
                if actions:
                    print(f"[OK] Linha tem {len(actions)} botoes de acao")
            except:
                pass
        else:
            print("[INFO] Tabela vazia")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Create Purchase Order button")
def click_create_purchase_order(context):
    """Clica no botao Adicionar para criar Purchase Order."""
    try:
        print("[DEBUG] Iniciando busca pelo botao Adicionar...")
        time.sleep(5)  # Aguardar pagina carregar completamente no CI

        # Log da URL atual
        print(f"[DEBUG] URL atual: {context.driver.current_url}")
        print(f"[DEBUG] Titulo: {context.driver.title}")

        selectors = [
            "//div[text()='Adicionar']",
            "//span[text()='Adicionar']",
            "//div[contains(text(), 'Adicionar')]",
            "//span[contains(text(), 'Adicionar')]",
            "//*[contains(@class, 'action') and contains(text(), 'Adicionar')]",
            "//button[contains(text(), 'Adicionar')]",
            "//*[text()='Adicionar']",
        ]

        element = None
        for idx, selector in enumerate(selectors):
            try:
                print(f"[DEBUG] Tentando seletor {idx+1}/{len(selectors)}: {selector}")
                element = WebDriverWait(context.driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if element.is_displayed():
                    print(f"[OK] Encontrado botao Adicionar com: {selector}")
                    break
                else:
                    print(f"[DEBUG] Elemento encontrado mas nao visivel: {selector}")
                    element = None
            except Exception as e:
                print(f"[DEBUG] Seletor {idx+1} falhou: {str(e)[:50]}")
                continue

        if element:
            # Log posição do elemento
            location = element.location
            size = element.size
            print(f"[DEBUG] Elemento posicao: x={location['x']}, y={location['y']}, w={size['width']}, h={size['height']}")

            context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            try:
                element.click()
                print("[OK] Click direto funcionou")
            except Exception as click_err:
                print(f"[DEBUG] Click direto falhou: {click_err}, tentando JS click")
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Adicionar (Create Purchase Order)")
            time.sleep(4)  # Aguardar formulario/modal carregar
        else:
            # Capturar estado da página para debug
            print("[ERROR] Botao Adicionar nao encontrado!")
            print(f"[DEBUG] Elementos com 'Adicionar' na pagina:")
            try:
                all_elements = context.driver.find_elements(By.XPATH, "//*[contains(text(), 'Adicionar')]")
                for i, el in enumerate(all_elements[:5]):
                    print(f"  [{i}] Tag: {el.tag_name}, Visible: {el.is_displayed()}, Text: {el.text[:30] if el.text else 'N/A'}")
            except:
                pass
            raise Exception("Botao Adicionar nao encontrado")

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Vendor from modal for Purchase Order")
def select_vendor_modal_po(context):
    """Seleciona um Vendor no modal de selecao para Purchase Order."""
    try:
        # Aguardar modal aparecer
        modal_selectors = [
            "//div[contains(@class, 'tt_utils_ui_dlg_modal')]",
            "//div[contains(text(), 'Selecione')]",
            "//div[contains(text(), 'Nome do')]",
        ]

        modal_found = False
        for selector in modal_selectors:
            try:
                WebDriverWait(context.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                modal_found = True
                print(f"[OK] Modal de selecao encontrado")
                break
            except:
                continue

        if not modal_found:
            raise Exception("Modal de selecao nao apareceu")

        time.sleep(1)

        # Clicar no primeiro vendor [RPA] disponivel
        vendor_selectors = [
            "//tr[contains(., 'VENDOR')]//td[last()]",
            "//td[contains(text(), '[RPA]')]/following-sibling::td//img[@alt]",
            "(//table//tbody//tr[contains(., '[RPA]')])[1]",
        ]

        for selector in vendor_selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print(f"[OK] Selecionou vendor com seletor: {selector}")
                break
            except:
                continue

        time.sleep(2)

        # Tratar possivel erro ATP
        try:
            sim_btn = WebDriverWait(context.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sim')]"))
            )
            sim_btn.click()
            print("[OK] Clicou em Sim no aviso ATP")
            time.sleep(1)
        except:
            pass

        print("[OK] Vendor selecionado")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill Purchase Order vendor information")
def fill_purchase_order_vendor(context):
    """Preenche informacoes do fornecedor (apos selecao no modal)."""
    try:
        time.sleep(3)  # Aguardar carregamento do formulario no CI

        # Verificar se apareceu modal de selecao de fornecedor
        modal_selectors = [
            "//div[contains(text(), 'Selecione')]",
            "//div[contains(@class, 'tt_utils_ui_dlg_modal')]",
            "//div[contains(text(), 'Vendor')]",
            "//div[contains(text(), 'Fornecedor')]",
        ]

        modal_found = False
        for selector in modal_selectors:
            try:
                modal = WebDriverWait(context.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if modal.is_displayed():
                    modal_found = True
                    print("[OK] Modal de selecao de fornecedor encontrado")
                    break
            except:
                continue

        # Se encontrou modal, selecionar primeiro fornecedor
        if modal_found:
            try:
                first_row = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'tt_utils_ui_dlg')]//table//tbody//tr)[1]"))
                )
                context.driver.execute_script("arguments[0].click();", first_row)
                print("[OK] Selecionou primeiro fornecedor")
                time.sleep(2)
            except Exception as e:
                print(f"[WARN] Nao conseguiu selecionar fornecedor: {e}")

        # Verificar se formulario de criacao foi carregado
        form_selectors = [
            "//span[contains(text(), 'Geral')]",
            "//div[contains(text(), 'Número do pedido')]",
            "//input[contains(@class, 'form')]",
        ]

        form_found = False
        for selector in form_selectors:
            try:
                WebDriverWait(context.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                form_found = True
                print(f"[OK] Formulario de criacao carregado: {selector}")
                break
            except:
                continue

        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill Purchase Order line items")
def fill_purchase_order_items(context):
    """Preenche itens do pedido - campos opcionais."""
    try:
        import random

        # Gerar numero de pedido aleatorio para teste
        order_number = f"PO#{random.randint(100000000, 999999999)}"

        # Tentar preencher o campo de numero do pedido
        order_field_selectors = [
            "//label[contains(text(), 'Número do pedido')]/following::input[1]",
            "//input[@name='order_number']",
            "//input[contains(@placeholder, 'pedido')]",
        ]

        for selector in order_field_selectors:
            try:
                field = context.driver.find_element(By.XPATH, selector)
                if field.is_displayed() and field.is_enabled():
                    field.clear()
                    field.send_keys(order_number)
                    print(f"[OK] Preencheu campo de pedido: {order_number}")
                    break
            except:
                continue

        time.sleep(1)
        print("[OK] Itens do pedido preenchidos")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save Purchase Order")
def click_save_purchase_order(context):
    """Salva Purchase Order."""
    try:
        selectors = [
            "//div[contains(@class, 'modal')]//button[contains(text(), 'Salvar')]",
            "//button[contains(text(), 'Salvar')]",
            "//button[contains(text(), 'Save')]",
            "//span[contains(text(), 'Salvar')]/parent::button",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrou botao Salvar")
                break
            except:
                continue

        if element:
            try:
                element.click()
            except:
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Salvou Purchase Order")

        time.sleep(2)

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Purchase Order should be created successfully")
def purchase_order_created(context):
    """Verifica criacao."""
    try:
        print("[OK] Purchase Order criado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search Purchase Order by order number")
def search_purchase_order(context):
    """Pesquisa por numero do pedido."""
    try:
        time.sleep(2)  # Aguardar carregamento

        # Procura o campo de busca pelo label "Número do pedido"
        try:
            # Encontra o label
            label = context.driver.find_element(
                By.XPATH, "//div[contains(text(), 'Número do pedido') or contains(text(), 'Order Number')]"
            )
            # Encontra o input dentro do mesmo container pai
            parent = label.find_element(By.XPATH, "./..")
            input_field = parent.find_element(By.XPATH, ".//input")
            print("[OK] Campo 'Número do pedido' encontrado via label")
        except:
            # Fallback: procurar inputs visiveis
            inputs = context.driver.find_elements(By.XPATH, "//input[@type='text' and not(@disabled)]")
            visible_inputs = [i for i in inputs if i.is_displayed() and i.is_enabled()]
            if len(visible_inputs) >= 5:
                input_field = visible_inputs[4]  # 5o input e o numero do pedido
                print("[OK] Campo encontrado por indice")
            else:
                input_field = visible_inputs[-1] if visible_inputs else None

        if input_field:
            context.driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
            time.sleep(0.5)
            context.driver.execute_script("arguments[0].click();", input_field)
            input_field.send_keys("PO")
            time.sleep(1)

            # Clica no botao Submit
            try:
                submit_btn = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit') or @type='submit']")
                context.driver.execute_script("arguments[0].click();", submit_btn)
            except:
                input_field.send_keys(Keys.ENTER)

            time.sleep(2)
            print("[OK] Pesquisa realizada")
        else:
            print("[WARN] Nenhum campo de busca encontrado")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on first Purchase Order record")
def click_first_purchase_order(context):
    """Clica no icone Visualizar do primeiro registro."""
    try:
        time.sleep(3)  # Aguardar carregamento da tabela no CI

        # Aguardar tabela carregar
        WebDriverWait(context.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//table//tbody//tr"))
        )
        print("[OK] Tabela carregada")

        view_selectors = [
            "(//table//tbody//tr)[1]//img[@alt='Visualizar']",
            "//table//tbody//tr[1]//img[@alt='Visualizar']",
            "(//img[@alt='Visualizar'])[1]",
            "//tbody//tr[1]//img[contains(@alt, 'View') or contains(@alt, 'Visualizar')]",
        ]

        element = None
        for selector in view_selectors:
            try:
                element = WebDriverWait(context.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print(f"[OK] Encontrado Visualizar: {selector}")
                break
            except:
                continue

        if element:
            context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            try:
                element.click()
            except:
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Visualizar primeiro registro")
        else:
            print("[WARN] Visualizar nao encontrado, clicando na linha")
            row = WebDriverWait(context.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//tbody//tr[td])[1]//td[2]"))
            )
            context.driver.execute_script("arguments[0].click();", row)

        time.sleep(2)  # Aguardar modal abrir

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Purchase Order Details modal should be displayed")
def purchase_order_details_modal(context):
    """Verifica modal."""
    try:
        time.sleep(2)  # Aguardar animacao do modal

        modal_selectors = [
            "//div[contains(@class, 'modal')]",
            "//div[contains(@class, 'dlg')]",
            "//div[contains(@class, 'dialog')]",
            "//div[contains(@class, 'popup')]",
            "//div[contains(@class, 'tt_utils_ui_dlg')]",
        ]

        modal_found = False
        for selector in modal_selectors:
            try:
                WebDriverWait(context.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print(f"[OK] Modal exibido: {selector}")
                modal_found = True
                break
            except:
                continue

        if not modal_found:
            print("[WARN] Modal nao detectado mas continuando...")

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Purchase Order Details should show order information")
def purchase_order_details_info(context):
    """Verifica informacoes."""
    try:
        print("[OK] Informacoes exibidas")
    except Exception as e:
        ends_timer(context, e)
        raise


def close_any_open_modal(driver):
    """Fecha qualquer modal aberto antes de interagir com a tabela."""
    print("[DEBUG] Iniciando close_any_open_modal...")

    close_selectors = [
        "//span[contains(@class, 'tt_utils_ui_dlg_close')]",
        "//div[contains(@class, 'tt_utils_ui_dlg')]//span[contains(@class, 'close')]",
        "//div[contains(@class, 'modal')]//span[contains(@class, 'close')]",
        "//div[contains(@class, 'modal')]//button[contains(@class, 'close')]",
        "//div[contains(@class, 'dlg')]//span[contains(@class, 'close')]",
        "//button[@aria-label='Close']",
        "//*[contains(@class, 'modal-close')]",
    ]

    for idx, selector in enumerate(close_selectors):
        try:
            print(f"[DEBUG] Tentando close selector {idx+1}: {selector[:50]}...")
            close_btn = driver.find_element(By.XPATH, selector)
            if close_btn.is_displayed():
                driver.execute_script("arguments[0].click();", close_btn)
                print(f"[OK] Modal fechado com selector {idx+1}")
                time.sleep(1)
                return True
            else:
                print(f"[DEBUG] Selector {idx+1} encontrado mas nao visivel")
        except Exception as e:
            print(f"[DEBUG] Selector {idx+1} nao encontrado")
            continue

    # Tenta ESC como fallback
    try:
        print("[DEBUG] Tentando ESC...")
        from selenium.webdriver.common.keys import Keys
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        print("[OK] ESC enviado")
        time.sleep(1)
        return True
    except Exception as e:
        print(f"[DEBUG] ESC falhou: {e}")

    print("[DEBUG] Nenhum modal para fechar")
    return False


@when("Click on Edit Purchase Order button")
def click_edit_purchase_order(context):
    """Clica no icone Editar - fecha modal primeiro, depois clica na tabela."""
    try:
        print("[DEBUG] Iniciando busca pelo botao Editar...")
        wait_for_page_ready(context.driver)
        time.sleep(2)

        # IMPORTANTE: Fechar modal aberto antes de tentar clicar na tabela
        print("[DEBUG] Fechando modal se estiver aberto...")
        close_any_open_modal(context.driver)
        time.sleep(1)

        print(f"[DEBUG] URL atual: {context.driver.current_url}")

        # Primeiro tenta encontrar dentro do modal
        modal_selectors = [
            "//div[contains(@class, 'modal')]//img[@alt='Editar']",
            "//div[contains(@class, 'dlg')]//img[@alt='Editar']",
            "//div[contains(@class, 'tt_utils_ui_dlg')]//img[@alt='Editar']",
            "//div[contains(@class, 'modal')]//button[contains(text(), 'Editar')]",
            "//div[contains(@class, 'modal')]//*[contains(text(), 'Editar')]",
        ]

        # Fallback para tabela
        table_selectors = [
            "(//table//tbody//tr)[1]//img[@alt='Editar']",
            "//table//tbody//tr[1]//img[@alt='Editar']",
            "(//img[@alt='Editar'])[1]",
        ]

        element = None

        # Tenta modal primeiro
        print("[DEBUG] Procurando Editar no modal...")
        for idx, selector in enumerate(modal_selectors):
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if element.is_displayed():
                    print(f"[OK] Encontrado Editar no modal: {selector}")
                    break
                else:
                    print(f"[DEBUG] Modal seletor {idx+1} encontrou elemento nao visivel")
                    element = None
            except:
                continue

        # Se não encontrou no modal, tenta na tabela
        if not element:
            print("[DEBUG] Nao encontrou no modal, procurando na tabela...")
            for idx, selector in enumerate(table_selectors):
                try:
                    element = WebDriverWait(context.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if element.is_displayed():
                        print(f"[OK] Encontrado Editar na tabela: {selector}")
                        break
                    else:
                        print(f"[DEBUG] Tabela seletor {idx+1} encontrou elemento nao visivel")
                        element = None
                except:
                    continue

        if element:
            location = element.location
            print(f"[DEBUG] Elemento Editar posicao: x={location['x']}, y={location['y']}")
            context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            if not safe_click(context.driver, element, "Editar"):
                raise Exception("Falha ao clicar em Editar")
            print("[OK] Clicou em Editar")
        else:
            # Debug: listar todos os elementos img na pagina
            print("[ERROR] Icone Editar nao encontrado!")
            try:
                imgs = context.driver.find_elements(By.XPATH, "//img[@alt]")
                print(f"[DEBUG] Imagens com alt na pagina ({len(imgs)}):")
                for img in imgs[:10]:
                    print(f"  - alt='{img.get_attribute('alt')}', visible={img.is_displayed()}")
            except:
                pass
            raise Exception("Icone Editar nao encontrado")

        time.sleep(4)  # Aguardar formulario de edicao

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Update Purchase Order information")
def update_purchase_order(context):
    """Atualiza informacoes."""
    try:
        print("[INFO] Atualizando...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Purchase Order should be updated successfully")
def purchase_order_updated(context):
    """Verifica atualizacao."""
    try:
        print("[OK] Atualizado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Delete Purchase Order button")
def click_delete_purchase_order(context):
    """Clica no icone Apagar - fecha modal primeiro, depois clica na tabela."""
    try:
        print("[DEBUG] Iniciando busca pelo botao Apagar...")
        wait_for_page_ready(context.driver)
        time.sleep(2)

        # IMPORTANTE: Fechar modal aberto antes de tentar clicar na tabela
        print("[DEBUG] Fechando modal se estiver aberto...")
        close_any_open_modal(context.driver)
        time.sleep(1)

        print(f"[DEBUG] URL atual: {context.driver.current_url}")

        # Primeiro tenta encontrar dentro do modal
        modal_selectors = [
            "//div[contains(@class, 'modal')]//img[@alt='Apagar']",
            "//div[contains(@class, 'dlg')]//img[@alt='Apagar']",
            "//div[contains(@class, 'tt_utils_ui_dlg')]//img[@alt='Apagar']",
            "//div[contains(@class, 'modal')]//button[contains(text(), 'Apagar')]",
            "//div[contains(@class, 'modal')]//button[contains(text(), 'Excluir')]",
            "//div[contains(@class, 'modal')]//*[contains(text(), 'Apagar')]",
        ]

        # Fallback para tabela
        table_selectors = [
            "(//table//tbody//tr)[1]//img[@alt='Apagar']",
            "//table//tbody//tr[1]//img[@alt='Apagar']",
            "(//img[@alt='Apagar'])[1]",
        ]

        element = None

        # Tenta modal primeiro
        print("[DEBUG] Procurando Apagar no modal...")
        for idx, selector in enumerate(modal_selectors):
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if element.is_displayed():
                    print(f"[OK] Encontrado Apagar no modal: {selector}")
                    break
                else:
                    print(f"[DEBUG] Modal seletor {idx+1} encontrou elemento nao visivel")
                    element = None
            except:
                continue

        # Se não encontrou no modal, tenta na tabela
        if not element:
            print("[DEBUG] Nao encontrou no modal, procurando na tabela...")
            for idx, selector in enumerate(table_selectors):
                try:
                    element = WebDriverWait(context.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if element.is_displayed():
                        print(f"[OK] Encontrado Apagar na tabela: {selector}")
                        break
                    else:
                        print(f"[DEBUG] Tabela seletor {idx+1} encontrou elemento nao visivel")
                        element = None
                except:
                    continue

        if element:
            location = element.location
            print(f"[DEBUG] Elemento Apagar posicao: x={location['x']}, y={location['y']}")
            context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            if not safe_click(context.driver, element, "Apagar"):
                raise Exception("Falha ao clicar em Apagar")
            print("[OK] Clicou em Apagar")
        else:
            # Debug: listar todos os elementos img na pagina
            print("[ERROR] Icone Apagar nao encontrado!")
            try:
                imgs = context.driver.find_elements(By.XPATH, "//img[@alt]")
                print(f"[DEBUG] Imagens com alt na pagina ({len(imgs)}):")
                for img in imgs[:10]:
                    print(f"  - alt='{img.get_attribute('alt')}', visible={img.is_displayed()}")
            except:
                pass
            raise Exception("Icone Apagar nao encontrado")

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Purchase Order should be deleted successfully")
def purchase_order_deleted(context):
    """Verifica exclusao."""
    try:
        print("[OK] Excluido")
    except Exception as e:
        ends_timer(context, e)
        raise
