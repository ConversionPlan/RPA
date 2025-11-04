from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.steps.utils import *
from features.steps.auth import ends_timer
from features.steps.product import open_dashboard_page
import time
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys



@given("There is a Manufactured Serial")
def manufactured_serial(context):
    try:
        open_dashboard_page(context)
        click_manufacture_lot_serial_request(context)
        click_add_serialized_lot(context)
        select_rpa_product_dropdown(context)
        add_lot_number_manafucturer(context)
        add_expiration_date_manafucturer(context)
        click_ok_add_serialized_lot(context)
        click_pencil(context)
        click_serials_tab(context)
        click_new_serials_request(context)
        add_quantity_generate(context)
        click_add_add_serial_request(context)
        click_ok_edit_manufacturer_lot(context)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Go back to dashboard page")
def back_dashboard_page(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//div[@class='client_logo']/a[@href='/']",
        , timeout=30).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on Commission Serial Numbers")
def click_commission_serial_numbers(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//label[text(, timeout=30)='Commission Serial Numbers']",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Select Last Created Serials' Product")
def select_last_created_serials_product(context):
    try:
        created_on_header = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//th[@rel='created_on']/span"))
        )
        created_on_header.click()

        # Aguardar o botão Select estar disponível
        select_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='Select']"))
        )
        select_button.click()
    except Exception as e:
        print(f"Erro ao selecionar produto criado: {str(e)}")
        ends_timer(context, e)
        raise


@when("Click on Select Serials Numbers")
def select_last_created_serials_product(context):
    try:
        select_serials_link = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Select Serials Numbers']"))
        )
        select_serials_link.click()
    except Exception as e:
        print(f"Erro ao clicar em 'Select Serials Numbers': {str(e)}")
        ends_timer(context, e)
        raise


@when("Click on Select Serials Numbers - Select Serial")
def select_last_created_serials_product(context):
    try:
        select_serials_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Select Serials Numbers']"))
        )
        select_serials_button.click()
    except Exception as e:
        print(f"Erro ao clicar em 'Select Serials Numbers - Select Serial': {str(e)}")
        ends_timer(context, e)
        raise


@when("Select Serial")
def select_serial(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//th/input[@name='select_all']",
        , timeout=30).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on Close the lot after commissioning the serials")
def click_close_lot_after_commissioning_serials(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//label[text(, timeout=30)='Close the lot after commissioning the serials']",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Select Storage Area")
def select_storage_area(context):
    try:
        storage_input = wait_and_find(context.driver, By.XPATH, "//select[@name='storage_area_uuid']",
        , timeout=30)
        storage_input.click()
        storage_input.send_keys(Keys.ARROW_DOWN)
        storage_input.send_keys(Keys.ENTER)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on OK - Commission")
def click_ok_commission(context):
    try:
        ok_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='OK']"))
        )
        ok_button.click()

        # Aguardar que a ação seja processada
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//span[text()='OK']"))
        )
    except Exception as e:
        print(f"Erro ao clicar em OK - Commission: {str(e)}")
        ends_timer(context, e)
        raise


@when("Click on Manufacture Lot and Serial Request")
def click_manufacture_lot_serial_request(context):
    try:
        # Tentar fechar modal Close se existir
        dismiss_modal_if_present(context.driver)

        # Usar wait_and_click com timeout aumentado
        wait_and_click(
            context.driver,
            By.XPATH,
            "//label[text()='Manufacture Lot and Serial Request']",
            timeout=20  # Aumentado de 10s para 20s
        )
    except Exception as e:
        print(f"Erro ao clicar em 'Manufacture Lot and Serial Request': {str(e)}")
        ends_timer(context, e)
        raise


@when("Click on Add Serialized Lot")
def click_add_serialized_lot(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "//span[text()='Add Serialized Lot']"
        )
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Select an RPA Product from Dropdown")
def select_rpa_product_dropdown(context):
    try:
        product_dropdown = wait_and_find(context.driver, By.XPATH, "//select[@name='product_uuid']",
        , timeout=30)
        product_dropdown.click()
        product_dropdown.send_keys(Keys.ARROW_DOWN)
        product_dropdown.send_keys(Keys.ENTER)
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Lot Number - Manufacturer")
def add_lot_number_manafucturer(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//input[@name='lot_number']",
        , timeout=30).send_keys(generate_x_length_number(10))
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Expiration Date - Manufacturer")
def add_expiration_date_manafucturer(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//input[@name='expiration_date']",
        , timeout=30).send_keys("12-12-2034")
        wait_and_find(context.driver, By.XPATH, "//label[text(, timeout=30)='Expiration Date']",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on OK - Add Serialized Lot")
def click_ok_add_serialized_lot(context):
    try:
        # Aguardar o produto estar disponível no dropdown
        product_option = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='product_uuid']/option[text() != '']"))
        )
        context.product_name = product_option.text

        # Aguardar o botão OK estar clicável
        ok_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='OK']"))
        )
        ok_button.click()
    except Exception as e:
        print(f"Erro ao clicar em OK - Add Serialized Lot: {str(e)}")
        ends_timer(context, e)
        raise


@when("Click on Pencil")
def click_pencil(context):
    try:
        # Aguardar o botão de edição estar clicável
        edit_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='Edit']"))
        )
        edit_button.click()
    except Exception as e:
        print(f"Erro ao clicar no botão de edição: {str(e)}")
        ends_timer(context, e)
        raise


@when("Click on Serials Tab")
def click_serials_tab(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//li[@rel='serials']",
        , timeout=30).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on New Serials Request")
def click_new_serials_request(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='New Serials Request']",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Add Quantity to generate")
def add_quantity_generate(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//input[@name='quantity']",
        , timeout=30).send_keys("1")
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on Add - Add Serial Request")
def click_add_add_serial_request(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='Add']",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on OK - Edit Manufacturer Lot")
def click_ok_edit_manufacturer_lot(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='Dismiss']",
        ).click()
        wait_and_find(context.driver, By.XPATH, "//span[text(, timeout=30)='OK']",
        ).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Save Amount of Records")
def save_amount_records(context):
    try:
        # Aguardar o texto de total de registros estar visível
        records_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Total of')]"))
        )
        records_text = records_element.text
        context.total_records = int(records_text.split("of ")[1].split(" recor")[0])
    except Exception as e:
        print(f"Erro ao salvar quantidade de registros: {str(e)}")
        ends_timer(context, e)
        raise


@when("Click on Delete button")
def click_delete_button(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//img[@alt='Delete']",
        , timeout=30).click()
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@when("Click on Yes - Confirmation")
def click_yes_confirmation(context):
    try:
        yes_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Yes']"))
        )
        yes_button.click()

        # Aguardar que o modal de confirmação desapareça
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//span[text()='Yes']"))
        )
    except Exception as e:
        print(f"Erro ao clicar em Yes - Confirmation: {str(e)}")
        ends_timer(context, e)
        raise


@then("Serials should be Manufactured")
def serials_should_be_manufactured(context):
    try:
        wait_and_find(context.driver, By.XPATH, f"//span[text(, timeout=30)='{context.product_name}']"
        )
        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise


@then("Serials should be Deleted")
def serials_should_be_deleted(context):
    try:
        # Aguardar a página atualizar após a exclusão
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tt_utils_ui_search-footer-nb-results"))
        )

        records_element = wait_and_find(context.driver, 
            By.CLASS_NAME, "tt_utils_ui_search-footer-nb-results"
        , timeout=30)
        records_text = records_element.text
        new_total_records = int(records_text.split("of ")[1].split(" recor")[0])
        assert context.total_records - new_total_records == 1
    except Exception as e:
        print(f"Erro ao verificar exclusão de seriais: {str(e)}")
        ends_timer(context, e)
        raise


@then("Serials should be Commissioned")
def serials_should_be_commissioned(context):
    try:
        # Aguardar um pouco antes de atualizar a página
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tt_utils_ui_search-footer-nb-results"))
        )

        context.driver.refresh()

        # Aguardar a página recarregar completamente
        records_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tt_utils_ui_search-footer-nb-results"))
        )

        records_text = records_element.text
        new_total_records = int(records_text.split("of ")[1].split(" recor")[0])
        assert context.total_records - new_total_records == 1
    except Exception as e:
        print(f"Erro ao verificar comissionamento de seriais: {str(e)}")
        ends_timer(context, e)
        raise
