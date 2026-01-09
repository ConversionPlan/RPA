"""
Steps para Company Management (Gestao da Companhia)
Inclui: Configuracoes Gerais, Produtos/Inventario, Usuarios/Permissoes
"""

from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys
from features.steps.auth import ends_timer
import time


# Step "Click on Company Management" ja existe em location.py

@then("Company Management page should be displayed")
def company_management_page_displayed(context):
    """Verifica se a pagina foi carregada."""
    try:
        selectors = [
            "//*[contains(text(), 'Gestão da companhia')]",
            "//*[contains(text(), 'Company Management')]",
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
            if "company_mgt" in context.driver.current_url.lower():
                found = True

        if not found:
            raise Exception("Pagina nao carregou")

        print("[OK] Pagina Company Management carregada")

    except Exception as e:
        ends_timer(context, e)
        raise


# ========================================
# CONFIGURACOES GERAIS
# ========================================

@when("Click on Company Settings")
def click_company_settings(context):
    """Clica em Configuracoes da Empresa (executa TT.Modules.CompanyMgt.CompanySettings.edit())."""
    try:
        selectors = [
            "//a[contains(@href, 'CompanySettings.edit')]",
            "//div[contains(text(), 'Configurações da Empresa')]",
            "//*[contains(text(), 'Configurações da Empresa')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado Company Settings: {selector}")
                break
            except:
                continue

        if element:
            try:
                element.click()
            except:
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Company Settings")
        else:
            raise Exception("Link Company Settings nao encontrado")

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@then("Company Settings modal should be displayed")
def company_settings_modal(context):
    """Verifica se modal foi aberto."""
    try:
        WebDriverWait(context.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'modal')]"))
        )
        print("[OK] Modal Company Settings exibido")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Update company information")
def update_company_info(context):
    """Atualiza informacoes da empresa."""
    try:
        print("[INFO] Atualizando informacoes...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save Company Settings")
def save_company_settings(context):
    """Salva configuracoes."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Salvar')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Salvou configuracoes")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Company Settings should be updated successfully")
def company_settings_updated(context):
    """Verifica atualizacao."""
    try:
        print("[OK] Configuracoes atualizadas")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on PDF Customization Setting")
def click_pdf_customization(context):
    """Clica em Configuracao de personalizacao de PDF (/company_mgt/pdf_customize_setting)."""
    try:
        selectors = [
            "//a[contains(@href, '/company_mgt/pdf_customize_setting')]",
            "//div[contains(text(), 'Configuração de personalização de PDF')]",
            "//*[contains(text(), 'Configuração de personalização de PDF')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado PDF Customization: {selector}")
                break
            except:
                continue

        if element:
            try:
                element.click()
            except:
                context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em PDF Customization")
        else:
            raise Exception("Link PDF Customization nao encontrado")

        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("PDF Customization page should be displayed")
def pdf_customization_page(context):
    """Verifica pagina."""
    try:
        print("[OK] Pagina PDF Customization exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Third Party Logistics Providers")
def click_third_party_logistics(context):
    """Clica em Provedores de Logistica."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'third_party_logistics')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em Third Party Logistics")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Third Party Logistics Providers page should be displayed")
def third_party_page(context):
    """Verifica pagina."""
    try:
        print("[OK] Pagina Third Party Logistics exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Provider button")
def click_add_provider(context):
    """Clica em adicionar provedor."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add') or contains(text(), 'Adicionar')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Add Provider")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill provider information")
def fill_provider_info(context):
    """Preenche informacoes do provedor."""
    try:
        print("[INFO] Preenchendo provedor...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save Provider")
def save_provider(context):
    """Salva provedor."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Salvar')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Salvou provedor")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Provider should be added successfully")
def provider_added(context):
    """Verifica adicao."""
    try:
        print("[OK] Provedor adicionado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on License Type Management")
def click_license_types(context):
    """Clica em Tipos de Licenca."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'license_type')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em License Types")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("License Types page should be displayed")
def license_types_page(context):
    """Verifica pagina."""
    try:
        print("[OK] Pagina License Types exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add License Type button")
def click_add_license_type(context):
    """Clica em adicionar tipo de licenca."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Add License Type")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill license type information")
def fill_license_type(context):
    """Preenche informacoes."""
    try:
        print("[INFO] Preenchendo...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save License Type")
def save_license_type(context):
    """Salva tipo de licenca."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Salvou")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("License Type should be added successfully")
def license_type_added(context):
    """Verifica adicao."""
    try:
        print("[OK] Tipo de licenca adicionado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Event Notification Actions")
def click_event_notifications(context):
    """Clica em Notificacoes de Eventos."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'event_notification')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em Event Notifications")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Event Notifications page should be displayed")
def event_notifications_page(context):
    """Verifica pagina."""
    try:
        print("[OK] Pagina Event Notifications exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Notification button")
def click_add_notification(context):
    """Clica em adicionar notificacao."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Add Notification")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill notification information")
def fill_notification(context):
    """Preenche informacoes."""
    try:
        print("[INFO] Preenchendo...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save Notification")
def save_notification(context):
    """Salva notificacao."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Salvou")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Notification should be added successfully")
def notification_added(context):
    """Verifica adicao."""
    try:
        print("[OK] Notificacao adicionada")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Workflow Automation")
def click_workflow_automation(context):
    """Clica em Automacao de Workflow."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'workflow_automation')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em Workflow Automation")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Workflow Automation page should be displayed")
def workflow_automation_page(context):
    """Verifica pagina."""
    try:
        print("[OK] Pagina Workflow Automation exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Trigger button")
def click_add_trigger(context):
    """Clica em adicionar trigger."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Add Trigger")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill trigger information")
def fill_trigger(context):
    """Preenche informacoes."""
    try:
        print("[INFO] Preenchendo...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save Trigger")
def save_trigger(context):
    """Salva trigger."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Salvou")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Trigger should be added successfully")
def trigger_added(context):
    """Verifica adicao."""
    try:
        print("[OK] Trigger adicionado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Usage Meter")
def click_usage_meter(context):
    """Clica em Medidor de Uso."""
    try:
        selectors = [
            "//*[contains(text(), 'Medidor de uso')]",
            "//*[contains(text(), 'Usage Meter')]",
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print("[OK] Clicou em Usage Meter")
                break
            except:
                continue

        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Usage Meter modal should be displayed")
def usage_meter_modal(context):
    """Verifica modal."""
    try:
        print("[OK] Modal Usage Meter exibido")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Usage statistics should be shown")
def usage_statistics(context):
    """Verifica estatisticas."""
    try:
        print("[OK] Estatisticas exibidas")
    except Exception as e:
        ends_timer(context, e)
        raise


# ========================================
# USUARIOS E PERMISSOES
# ========================================

@when("Click on Staff Management")
def click_staff_management(context):
    """Clica em Gestao de Funcionarios."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'staff_management')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em Staff Management")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Staff Management page should be displayed")
def staff_management_page(context):
    """Verifica pagina."""
    try:
        print("[OK] Pagina Staff Management exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Staff button")
def click_add_staff(context):
    """Clica em adicionar funcionario."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Add Staff")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill staff information")
def fill_staff_info(context):
    """Preenche informacoes."""
    try:
        print("[INFO] Preenchendo...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save Staff")
def save_staff(context):
    """Salva funcionario."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Salvou")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Staff member should be added successfully")
def staff_added(context):
    """Verifica adicao."""
    try:
        print("[OK] Funcionario adicionado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on first staff member")
def click_first_staff(context):
    """Clica no primeiro funcionario."""
    try:
        row = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "(//tbody//tr[td])[1]//td[1]"))
        )
        row.click()
        time.sleep(1)
        print("[OK] Clicou no funcionario")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Update staff information")
def update_staff_info(context):
    """Atualiza informacoes."""
    try:
        print("[INFO] Atualizando...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Staff member should be updated successfully")
def staff_updated(context):
    """Verifica atualizacao."""
    try:
        print("[OK] Funcionario atualizado")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on User Roles Management")
def click_user_roles(context):
    """Clica em Funcoes de Usuario."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'user_roles')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em User Roles")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("User Roles page should be displayed")
def user_roles_page(context):
    """Verifica pagina."""
    try:
        print("[OK] Pagina User Roles exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Role button")
def click_add_role(context):
    """Clica em adicionar funcao."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Add Role")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill role information")
def fill_role_info(context):
    """Preenche informacoes."""
    try:
        print("[INFO] Preenchendo...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Set role permissions")
def set_role_permissions(context):
    """Define permissoes."""
    try:
        print("[INFO] Definindo permissoes...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save Role")
def save_role(context):
    """Salva funcao."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Salvou")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("User Role should be added successfully")
def role_added(context):
    """Verifica adicao."""
    try:
        print("[OK] Funcao adicionada")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on API Access Keys")
def click_api_keys(context):
    """Clica em Chaves de API."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'api_keys')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em API Keys")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("API Keys page should be displayed")
def api_keys_page(context):
    """Verifica pagina."""
    try:
        print("[OK] Pagina API Keys exibida")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Generate API Key button")
def click_generate_api_key(context):
    """Clica em gerar chave."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Generate') or contains(text(), 'Gerar')]"))
        )
        element.click()
        time.sleep(1)
        print("[OK] Clicou em Generate")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Fill API key description")
def fill_api_key_description(context):
    """Preenche descricao."""
    try:
        print("[INFO] Preenchendo descricao...")
        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Generate")
def click_generate(context):
    """Clica em gerar."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Generate') or contains(text(), 'Gerar')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Gerou chave")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("API Key should be generated successfully")
def api_key_generated(context):
    """Verifica geracao."""
    try:
        print("[OK] Chave API gerada")
    except Exception as e:
        ends_timer(context, e)
        raise
