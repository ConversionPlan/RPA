from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.utils import *
from features.steps.auth import ends_timer
from features.steps.utils import (
    wait_and_click,
    wait_and_find,
    wait_and_send_keys,
    safe_parse_records_count,
    delete_outbound_by_code,
    assert_record_deleted,
    assert_record_count_changed,
)
from features.steps.inbound import (
    do_inbound,
    click_yes,
    click_change_location,
    select_location,
)
from features.steps.trading_partner import click_save_tp
import time


@given("There is an Outbound Created")
def there_is_outbound_created(context):
    try:
        do_inbound(context)
        return_dashboard_page(context)
        click_create_so_by_picking(context)
        select_type_customer(context)
        search_rpa_customer(context)
        select_customer(context)
        click_yes(context)
        click_change_location(context)
        search_location_inbound(context)
        select_location(context)
        add_so_number(context)
        click_bought_by_tab(context)
        select_bought_by_main_address(context)
        select_ship_to(context)
        click_picking_tab(context)
        click_inventory_lookup(context)
        select_shown_product(context)
        select_shown_serial(context)
        click_add_selection(context)
        time.sleep(2)
        click_save_tp(context)
        click_shipped_status(context)
        click_save_confirm_products(context)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Return to dashboard page")
def return_dashboard_page(context):
    try:
        context.driver.get("https://qualityportal.qa-test.tracktraceweb.com/")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Outbound")
def click_outbound(context):
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Tentar múltiplos seletores - Português primeiro, depois Inglês
        selectors = [
            # Português - Portal em PT-BR
            "//a[contains(@href, '/outbound')]",
            "//*[contains(text(), 'Saída')]",
            "//span[contains(text(), 'Saída')]",
            # Inglês - fallback
            "//a[@href='/shipments/outbound_shipments/']/span",
            "//span[contains(text(), 'Outbound')]",
            "//*[contains(text(), 'Outbound')]"
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado Outbound com seletor: {selector}")
                break
            except:
                continue

        if element is None:
            raise Exception("Não foi possível encontrar o elemento Outbound")

        try:
            element.click()
        except:
            context.driver.execute_script("arguments[0].click();", element)
            print("[OK] Clicou em Outbound via JavaScript")

        time.sleep(2)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Delete Created Outbound")
def delete_created_outbound(context):
    """
    Deleta um Outbound usando identificador de negócio robusto.

    ANTES (frágil):
        outbound_row = wait_and_find(..., f"//td[contains(text(), '{context.po}')]/ancestor::tr")
        delete_button = outbound_row.find_element(By.XPATH, ".//img[@alt='Delete']")
        delete_button.click()
        # Problemas:
        # - Seletor //img[@alt='Delete'] pode quebrar se UI mudar
        # - Não há confirmação automática do diálogo
        # - Sem fallback se elemento for interceptado

    DEPOIS (robusto):
        delete_outbound_by_code(context.driver, context.po, confirm_deletion=False)
        # Benefícios:
        # - Usa identificador de negócio (PO number) para encontrar linha correta
        # - Múltiplas estratégias de seletor para botão Delete
        # - Múltiplas estratégias de click (direto, scroll, JS, Actions)
        # - Screenshot automático em caso de erro
    """
    try:
        print(f"[INFO] Deletando outbound com PO: {context.po}")

        # Usar função helper robusta
        result = delete_outbound_by_code(
            driver=context.driver,
            outbound_code=context.po,
            confirm_deletion=False,  # Confirmação será feita em step separado
            timeout=15
        )

        print(f"[OK] Botão Delete clicado para outbound: {result}")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Create sales order by picking")
def click_create_so_by_picking(context):
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Tentar múltiplos seletores - Português primeiro, depois Inglês
        selectors = [
            # Português - Portal em PT-BR
            "//label[contains(text(), 'Criar pedido de vendas por picking')]",
            "//label[contains(text(), 'Criar pedido de vendas')]",
            "//*[contains(text(), 'Criar pedido de vendas por picking')]",
            # Inglês - fallback
            "//label[text()='Create sales order by picking']",
            "//label[contains(text(), 'Create sales order')]",
            "//*[contains(text(), 'Create sales order by picking')]"
        ]

        element = None
        for selector in selectors:
            try:
                element = WebDriverWait(context.driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[OK] Encontrado Create sales order com seletor: {selector}")
                break
            except:
                continue

        if element is None:
            raise Exception("Não foi possível encontrar Create sales order by picking")

        try:
            element.click()
        except:
            context.driver.execute_script("arguments[0].click();", element)

        time.sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Type Customer")
def select_type_customer(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//select[@rel='type']")
        wait_and_click(context.driver, By.XPATH, "//option[@value='CUSTOMER']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search for an RPA Customer")
def search_rpa_customer(context):
    try:
        wait_and_send_keys(
            context.driver,
            By.XPATH,
            "//input[@rel='name']",
            "[RPA]"
        )
        vendor_name = wait_and_find(context.driver, By.XPATH, "//input[@rel='name']")
        vendor_name.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select a Customer")
def select_customer(context):
    try:
        trading_partner = wait_and_find(context.driver, By.XPATH, "//td[@rel='name']")
        context.tp_name = trading_partner.text
        wait_and_click(context.driver, By.XPATH, "//td[@rel='name']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search for Location with Inbound")
def search_location_inbound(context):
    try:
        wait_and_send_keys(
            context.driver,
            By.XPATH,
            "//input[@rel='name']",
            context.inbounded_location
        )
        location_name = wait_and_find(context.driver, By.XPATH, "//input[@rel='name']")
        location_name.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add SO Number")
def add_so_number(context):
    try:
        context.po = generate_po()
        wait_and_send_keys(
            context.driver,
            By.XPATH,
            "//input[@rel='po_nbr']",
            context.po
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Bought By/Ship To Tab")
def click_bought_by_tab(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//span[text()='Bought By/Ship To']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Bought By Location as Main Address")
def select_bought_by_main_address(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "//span[contains(@id, 'billing_address_uuid')]"
        )
        sold_by_input = wait_and_find(
            context.driver,
            By.XPATH,
            "//input[@class='select2-search__field']"
        )
        sold_by_input.send_keys("Main Address")
        sold_by_input.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Ship To as Ship To")
def select_ship_to(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "//span[contains(@id, 'ship_to_address_uuid')]"
        )
        sold_by_input = wait_and_find(
            context.driver,
            By.XPATH,
            "//input[@class='select2-search__field']"
        )
        sold_by_input.send_keys("Ship To")
        sold_by_input.send_keys(Keys.ENTER)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Picking Tab")
def click_picking_tab(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//span[text()='Picking']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Inventory Lookup")
def click_inventory_lookup(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//a[text()='Inventory Lookup']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Shown Product")
def select_shown_product(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//img[@alt='Add to picking']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Shown Serial")
def select_shown_serial(context):
    try:
        # Aguardar um tempo maior para o modal carregar os serials
        time.sleep(2)
        wait_and_click(context.driver, By.ID, "_tt_checkbox_field_0", timeout=20)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Selection")
def click_add_selection(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//span[text()='Add Selection']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Shipped - Status")
def click_shipped_status(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//input[@value='SHIPPED']")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Save - Confirm Products Quantity")
def click_save_confirm_products(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "(//button[contains(@class,'tt_utils_ui_dlg_modal-default-enabled-button')]/span[text()='Save'])[2]"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Shipped - Dashboard")
def click_shipped_dashboard(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//label[text()='Shipped']")
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Outbound should be saved")
def outbound_saved(context):
    try:
        wait_and_find(
            context.driver,
            By.XPATH,
            f"//*[contains(text(),'{context.tp_name}')]"
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Outbound should be deleted")
def outbound_deleted(context):
    """
    Valida que um Outbound foi deletado corretamente.

    ANTES (frágil):
        new_total_records = safe_parse_records_count(records_text, default=context.total_records)
        assert context.total_records - new_total_records == 1
        # Problemas:
        # - Não verifica se é o outbound correto que foi deletado
        # - Pode falhar se outro processo criar/deletar em paralelo
        # - Apenas verifica contagem, não o registro específico

    DEPOIS (robusto):
        assert_record_deleted(driver, context.po, identifier_column="po_nbr", ...)
        # Benefícios:
        # - Verifica que o outbound específico não está mais visível
        # - Ou valida que o status mudou para DELETED/INACTIVE
        # - Contagem robusta com tolerância para concorrência
        # - Mensagens de erro detalhadas
    """
    try:
        # Verificar se temos o PO do outbound
        outbound_po = getattr(context, 'po', None)

        if outbound_po:
            # Usar helper robusto com verificação de PO específico
            result = assert_record_deleted(
                driver=context.driver,
                identifier_value=outbound_po,
                identifier_column="po_nbr",
                verify_count=hasattr(context, 'total_records'),
                count_before=getattr(context, 'total_records', None),
                timeout=15
            )
            print(f"[OK] Outbound deletado e validado: {result}")
        else:
            # Fallback: usar apenas contagem (menos robusto, mas compatível)
            time.sleep(2)
            context.driver.refresh()
            time.sleep(2)

            records_element = wait_and_find(
                context.driver,
                By.CLASS_NAME,
                "tt_utils_ui_search-footer-nb-results",
                timeout=15
            )
            records_text = records_element.text
            new_total_records = safe_parse_records_count(
                records_text,
                default=context.total_records
            )

            # Usar validação robusta de contagem
            assert_record_count_changed(
                count_before=context.total_records,
                count_after=new_total_records,
                expected_change=-1,
                operation="deleção de outbound",
                allow_concurrent_changes=True
            )

    except AssertionError as ae:
        ends_timer(context, ae)
        raise AssertionError(
            f"Falha na validação de deleção de outbound:\n{str(ae)}"
        )
    except Exception as e:
        ends_timer(context, e)
        raise
