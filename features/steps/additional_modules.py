"""
Steps para modulos adicionais:
- Utilities (Servicos de Utilidade Publica)
- My Account (Minha Conta)
- Quarantine (Quarentena)
- Inventory Adjustments (Ajustes de Inventario)
"""

from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.steps.auth import ends_timer
import time


# ========================================
# UTILITIES (SERVICOS DE UTILIDADE PUBLICA)
# ========================================

# Step "Click on Utilities" ja existe em inbound.py


@then("Utilities page should be displayed")
def utilities_page_displayed(context):
    """Verifica se a pagina Utilities foi carregada."""
    try:
        selectors = [
            "//*[contains(text(), 'Serviços de utilidade pública')]",
            "//*[contains(text(), 'Utilities')]",
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
            if "utilities" in context.driver.current_url.lower():
                found = True

        if not found:
            raise Exception("Pagina Utilities nao carregou")

        print("[OK] Pagina Utilities carregada")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on EPCIS Upload")
def click_epcis_upload(context):
    """Clica em Upload manual de arquivo EPCIS."""
    try:
        selectors = [
            "//div[contains(text(), 'Upload manual de arquivo EPCIS')]",
            "//*[contains(text(), 'Upload manual de arquivo EPCIS')]",
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print("[OK] Clicou em EPCIS Upload")
                break
            except:
                continue

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Electronic Exchanges Dashboard")
def click_electronic_exchanges(context):
    """Clica em Painel de Trocas Eletronicas."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/utilities/electronic_exchanges_dashboard')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em Electronic Exchanges Dashboard")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Electronic Exchanges Dashboard should be displayed")
def electronic_exchanges_displayed(context):
    """Verifica pagina."""
    try:
        if "electronic_exchanges" in context.driver.current_url.lower():
            print("[OK] Pagina Electronic Exchanges carregada")
        else:
            raise Exception("Pagina nao carregou")
    except Exception as e:
        ends_timer(context, e)
        raise


# ========================================
# MY ACCOUNT (MINHA CONTA)
# ========================================

@when("Click on My Account")
def click_my_account(context):
    """Navega para My Account via menu lateral."""
    try:
        selectors = [
            "//a[contains(@href, '/my_account')]",
            "//span[contains(text(), 'Minha conta')]",
            "//*[contains(text(), 'Minha conta')]",
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado My Account: {selector}")
                break
            except:
                continue

        if element is None:
            raise Exception("Nao encontrou My Account")

        try:
            element.click()
        except:
            context.driver.execute_script("arguments[0].click();", element)

        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("My Account page should be displayed")
def my_account_page_displayed(context):
    """Verifica se a pagina My Account foi carregada."""
    try:
        selectors = [
            "//*[contains(text(), 'Minha conta')]",
            "//*[contains(text(), 'My Account')]",
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
            if "my_account" in context.driver.current_url.lower():
                found = True

        if not found:
            raise Exception("Pagina My Account nao carregou")

        print("[OK] Pagina My Account carregada")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on User Profile")
def click_user_profile(context):
    """Clica em Seu perfil de usuario."""
    try:
        selectors = [
            "//a[contains(@href, 'BasicUserProfile.edit')]",
            "//div[contains(text(), 'Seu perfil de usuário')]",
            "//*[contains(text(), 'Seu perfil de usuário')]",
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print("[OK] Clicou em User Profile")
                break
            except:
                continue

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Change Password")
def click_change_password(context):
    """Clica em Mudar senha."""
    try:
        selectors = [
            "//a[contains(@href, 'ChangePassword.openForm')]",
            "//div[contains(text(), 'Mudar senha')]",
            "//*[contains(text(), 'Mudar senha')]",
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print("[OK] Clicou em Change Password")
                break
            except:
                continue

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Two Factor Authentication")
def click_two_factor_auth(context):
    """Clica em Autenticacao em duas etapas."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/my_account/user_2fa')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em Two Factor Authentication")
    except Exception as e:
        ends_timer(context, e)
        raise


# ========================================
# QUARANTINE (QUARENTENA)
# ========================================

# Step "Click on Quarantine" ja existe em inventory.py


@then("Quarantine page should be displayed")
def quarantine_page_displayed(context):
    """Verifica se a pagina Quarantine foi carregada."""
    try:
        selectors = [
            "//*[contains(text(), 'Quarentena')]",
            "//*[contains(text(), 'Quarantine')]",
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
            if "quarantine" in context.driver.current_url.lower():
                found = True

        if not found:
            raise Exception("Pagina Quarantine nao carregou")

        print("[OK] Pagina Quarantine carregada")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Items to Quarantine")
def click_add_quarantine(context):
    """Clica em Itens de quarentena (adicionar)."""
    try:
        selectors = [
            "//a[contains(@href, 'Quarantine.Add')]",
            "//div[contains(text(), 'Itens de quarentena')]",
            "//*[contains(text(), 'Itens de quarentena')]",
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                element.click()
                print("[OK] Clicou em Add Items to Quarantine")
                break
            except:
                continue

        time.sleep(1)

    except Exception as e:
        ends_timer(context, e)
        raise


# Step "Click on Items in Quarantine" ja existe em inventory.py


@when("Click on Quarantine Events")
def click_quarantine_events(context):
    """Clica em Eventos de quarentena."""
    try:
        element = WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/quarantine/events')]"))
        )
        element.click()
        time.sleep(2)
        print("[OK] Clicou em Quarantine Events")
    except Exception as e:
        ends_timer(context, e)
        raise


# ========================================
# INVENTORY ADJUSTMENTS (AJUSTES DE INVENTARIO)
# ========================================
# Steps ja existem em inventory.py:
# - Click on Inventory Adjustments
# - Click on Destructions
# - Click on Dispenses
# - Click on Missing/Stolen


@then("Inventory Adjustments page should be displayed")
def inventory_adjustments_page_displayed(context):
    """Verifica se a pagina foi carregada."""
    try:
        selectors = [
            "//*[contains(text(), 'Ajustes de estoque')]",
            "//*[contains(text(), 'Inventory Adjustments')]",
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
            if "adjustments" in context.driver.current_url.lower():
                found = True

        if not found:
            raise Exception("Pagina nao carregou")

        print("[OK] Pagina Inventory Adjustments carregada")

    except Exception as e:
        ends_timer(context, e)
        raise
