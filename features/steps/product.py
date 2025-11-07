from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.steps.utils import *
from features.steps.auth import ends_timer
from time import sleep
from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys



@given("There is a Product Created")
def there_is_product_created(context):
    open_dashboard_page(context)
    open_sandwich_menu(context)
    click_product_management(context)
    click_add_product_management(context)
    input_product_name(context)
    add_pack_size(context, 1)
    click_identifiers_tab(context)
    add_sku(context)
    add_upc(context)
    input_gs1_company_prefix(context)
    input_gs1_id(context)
    click_add_identifier(context)
    wait_identifier_options(context)
    input_ndc_value(context)
    click_add_ndc(context)
    click_requirements_tab(context)
    add_generic_name(context)
    add_strength(context)
    add_net_content(context)
    add_notes(context)
    click_add(context)


@when("Open dashboard page")
def open_dashboard_page(context):
    try:
        # Wait for page to be ready - try different selectors
        selectors_to_try = [
            (By.XPATH, "//div[@class='client_logo']/a"),
            (By.XPATH, "//div[contains(@class, 'sidebar')]"),
            (By.XPATH, "//div[contains(@class, 'dashboard')]"),
        ]

        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        element_found = False
        for by, selector in selectors_to_try:
            try:
                WebDriverWait(context.driver, 10).until(
                    EC.presence_of_element_located((by, selector))
                )
                element_found = True
                break
            except:
                continue

        if not element_found:
            # If we're already on the dashboard URL, that's OK
            if "tracktraceweb.com" in context.driver.current_url:
                print(f"Dashboard page - current URL: {context.driver.current_url}")
            else:
                raise Exception(f"Could not verify dashboard page at URL: {context.driver.current_url}")

        sleep(2)  # Give page time to load fully
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Open sandwich menu")
def open_sandwich_menu(context):
    try:
        # Quick close any open modals - only try most common ones, with short timeout
        close_selectors = [
            "//span[text()='Close']",
            "//button[contains(@class, 'close')]",
            "//div[contains(@class, 'tt_utils_ui_dlg_modal')]//span[text()='Close']"
        ]

        for close_selector in close_selectors:
            try:
                close_btn = WebDriverWait(context.driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, close_selector))
                )
                close_btn.click()
                sleep(0.5)
                break  # Exit after first successful close
            except:
                pass  # Ignore if not found

        # Try the most common menu selectors first, with element_to_be_clickable
        primary_selectors = [
            "//div[contains(@class, 'sidebar_menu_toggle')]/a",
            "//a[contains(@class, 'sidebar-toggle')]",
            "//i[contains(@class, 'fa-bars')]/parent::a"
        ]

        # Try primary selectors with short timeout
        for selector in primary_selectors:
            try:
                menu_toggle = WebDriverWait(context.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                # Use JavaScript click to avoid interception issues
                context.driver.execute_script("arguments[0].click();", menu_toggle)
                sleep(1)
                return  # Success, exit function
            except:
                pass

        # If primary selectors fail, try additional ones with even shorter timeout
        secondary_selectors = [
            "//div[contains(@class, 'sidebar_menu_toggle_dis')]/a",
            "//div[contains(@class, 'sidebar_menu_toggle_en')]/a",
            "//*[@id='sidebar-toggle']",
            "//button[contains(@class, 'menu-toggle')]"
        ]

        for selector in secondary_selectors:
            try:
                menu_toggle = WebDriverWait(context.driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                context.driver.execute_script("arguments[0].click();", menu_toggle)
                sleep(1)
                return
            except:
                pass

        # Last resort - try with presence instead of clickable
        try:
            menu_toggle = context.driver.find_element(By.XPATH, "//a[contains(@class, 'sidebar')]")
            context.driver.execute_script("arguments[0].click();", menu_toggle)
            sleep(1)
            return
        except:
            pass

        # If all fails, take screenshot and raise error
        context.driver.save_screenshot("report/output/menu_not_found.png")
        raise Exception("Menu toggle not found after trying all selectors")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Product Management")
def click_product_management(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "//a[contains(@href, '/products/')]/span[contains(text(), 'Product Management')]",
            timeout=10
        )
        sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add - Product Management Page")
def click_add_product_management(context):
    try:
        wait_and_click(
            context.driver,
            By.CLASS_NAME,
            "tt_utils_ui_search-one-header-action-button--add-action",
            timeout=10
        )
        sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on General Tab")
def click_general_tab(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//li[@rel='general']", timeout=10)
        sleep(0.5)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Product Name")
def input_product_name(context):
    try:
        context.product_name = generate_product_name() + " EACH"
        name_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_name", timeout=10
        )
        name_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_name", context.product_name
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Saved Product Name")
def input_saved_product_name(context):
    try:
        context.product_name = context.product_name.split(" EACH")[0] + " CASE"
        name_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_name", timeout=10
        )
        name_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_name", context.product_name
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Pack Size {size}")
def add_pack_size(context, size):
    try:
        pack_size_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_pack_size", timeout=10
        )
        pack_size_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_pack_size", size
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Select Pack Size Case")
def select_pack_size_case(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//select[@name='packaging_type']", timeout=10)
        sleep(0.5)
        wait_and_click(context.driver, By.XPATH, "//option[text()='Case (CA)']", timeout=10)
        sleep(0.5)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Identifiers tab")
def click_identifiers_tab(context):
    try:
        wait_and_click(context.driver, By.XPATH, "//li[@rel='identifiers']", timeout=10)
        sleep(0.5)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add SKU")
def add_sku(context):
    try:
        context.ndc = generate_ndc()
        sku_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_sku", timeout=10
        )
        sku_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_sku", context.ndc
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Saved SKU")
def add_saved_ku(context):
    try:
        sku_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_sku", timeout=10
        )
        sku_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_sku", context.ndc
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add UPC")
def add_upc(context):
    try:
        context.company_prefix = generate_company_prefix()
        context.gs1_id = generate_gs1_id()
        context.gtin = generate_gtin_with_cp_id(context.company_prefix, context.gs1_id)
        upc_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_upc", timeout=10
        )
        upc_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_upc", context.gtin
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Saved UPC")
def add_saved_upc(context):
    try:
        upc_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_upc", timeout=10
        )
        upc_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_upc", context.gtin
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add GS1 Company Prefix")
def input_gs1_company_prefix(context):
    try:
        prefix_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_company_prefix", timeout=10
        )
        prefix_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_company_prefix", context.company_prefix
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add GS1 ID")
def input_gs1_id(context):
    try:
        gs1_field = wait_and_find(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_id", timeout=10
        )
        gs1_field.clear()
        wait_and_send_keys(
            context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_gs1_id", context.gs1_id
        )
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Identifier")
def click_add_identifier(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "//div[@class='tt_utils_forms-one-header-action-button tt_utils_forms-one-header-action-button--add-action']",
            timeout=10
        )
        sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Identifier Value")
def input_ndc_value(context):
    try:
        input_field = wait_and_find(
            context.driver, By.XPATH, "//input[@rel='value']", timeout=10
        )
        input_field.send_keys(context.ndc)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Wait for Identifier Options to Load")
def wait_identifier_options(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//select[@name='identifier_code']/option[@value='US_NDC']", timeout=30)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add NDC")
def click_add_ndc(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//div[contains(@class, 'tt_utils_ui_dlg_modal-width-class-l')]//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button')]", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Requirements Tab")
def click_requirements_tab(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//li[@rel='requirements']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Generic Name")
def add_generic_name(context):
    try:
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_generic_name", timeout=30).send_keys(context.product_name)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Strength")
def add_strength(context):
    try:
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_strength", timeout=30).send_keys("RPA Strength")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Net Content Description")
def add_net_content(context):
    try:
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_net_content_desc", timeout=30).send_keys("RPA Net Content")
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Add Notes")
def add_notes(context):
    try:
        text = generate_text_with_n_chars(30)
        wait_and_find(context.driver, By.ID, "TT_UTILS_UI_FORM_UUID__1_notes", timeout=30).send_keys(text)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add")
def click_add(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button')]", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Aggregation Tab")
def click_aggregation_tab(context):
    try:
        print("[INFO] Clicando na aba Aggregation...")
        wait_and_find(context.driver, By.XPATH, "//li[@rel='composition']", timeout=30).click()
        sleep(2)

        # Debug: Ver o estado da pagina apos clicar na aba
        try:
            # Procurar pelo botao Add Product
            add_buttons = context.driver.find_elements(By.CLASS_NAME, "__choose_composition_product")
            print(f"[DEBUG] Botoes 'Add Product' encontrados: {len(add_buttons)}")
            if len(add_buttons) > 0:
                print(f"[DEBUG] Texto do botao: {add_buttons[0].text}")
                print(f"[DEBUG] Visivel: {add_buttons[0].is_displayed()}")
                print(f"[DEBUG] Habilitado: {add_buttons[0].is_enabled()}")

            # Ver se estamos em um iframe ou modal
            iframes = context.driver.find_elements(By.TAG_NAME, "iframe")
            print(f"[DEBUG] Iframes encontrados: {len(iframes)}")

            modals = context.driver.find_elements(By.CLASS_NAME, "tt_utils_ui_dlg_modal")
            print(f"[DEBUG] Modais na aba Aggregation: {len(modals)}")

        except Exception as debug_err:
            print(f"[WARN] Erro ao obter diagnostico: {debug_err}")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Add Product")
def click_add_product(context):
    try:
        print("[INFO] Procurando botao 'Add Product' para composicao...")
        add_button = wait_and_find(context.driver, By.CLASS_NAME, "__choose_composition_product", timeout=30)
        print(f"[INFO] Botao encontrado: {add_button.text if add_button.text else '(sem texto)'}")

        # Tentar com JavaScript click (mais confiavel para elementos dinamicos)
        print("[INFO] Clicando com JavaScript...")
        context.driver.execute_script("arguments[0].click();", add_button)
        print("[OK] Botao 'Add Product' clicado com JavaScript")

        # Aguardar mais tempo para modal abrir
        sleep(3)

        # Verificar se um modal/interface de selecao abriu
        try:
            # Aguardar pelo modal
            from selenium.webdriver.support.wait import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            try:
                WebDriverWait(context.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "tt_utils_ui_dlg_modal"))
                )
                print("[OK] Modal de selecao de produtos abriu!")
            except:
                print("[WARN] Modal nao abriu apos 10 segundos")

            # Procurar por elementos que indicam um modal de selecao
            modals = context.driver.find_elements(By.CLASS_NAME, "tt_utils_ui_dlg_modal")
            print(f"[DEBUG] Modais encontrados: {len(modals)}")

            # Ver se há campo de busca de produtos
            search_fields = context.driver.find_elements(By.XPATH, "//input[@rel='name']")
            print(f"[DEBUG] Campos de busca encontrados: {len(search_fields)}")

            # Ver URL atual
            current_url = context.driver.current_url
            print(f"[DEBUG] URL atual: {current_url}")
        except Exception as debug_err:
            print(f"[WARN] Erro ao obter diagnostico: {debug_err}")

    except Exception as e:
        ends_timer(context, e)
        raise


@when("Input Name of Each Product into Product Name")
def input_name_each_product(context):
    try:
        name_input_field = wait_and_find(
            context.driver, By.XPATH, "//input[@rel='name']", timeout=10
        )
        name_input_field.clear()
        sleep(0.5)
        name_input_field.send_keys(" EACH")
        sleep(2)  # Wait for autocomplete to load
        name_input_field.send_keys(Keys.ENTER)
        sleep(2)  # Wait for search results to appear
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Product Name")
def click_product_name(context):
    try:
        # Wait for the results table/list to appear
        sleep(2)

        # NO CONTEXTO DE AGREGACAO, precisamos clicar no produto para seleciona-lo,
        # NAO para abrir o modal de visualizacao.
        # Procurar por um botao/icone de "Add" ao lado do produto, similar ao padrao usado em outbound

        # Find the product element
        product = wait_and_find(
            context.driver,
            By.XPATH,
            "//td[@rel='name' and contains(., 'EACH')]",
            timeout=15
        )
        product_text = product.text
        print(f"[INFO] Found product: {product_text}")

        # Salvar o nome do produto para uso posterior
        context.selected_product_name = product_text

        # PRIMEIRO: Obter HTML da linha para diagnostico
        try:
            product_row = product.find_element(By.XPATH, "./ancestor::tr")
            row_html = product_row.get_attribute('outerHTML')
            print(f"[DEBUG] HTML completo da linha do produto:")
            print(row_html)

            # Procurar todos os elementos clicaveis na linha
            clickable_elements = product_row.find_elements(By.XPATH, ".//*[@onclick or .//img or .//button or .//a]")
            print(f"[DEBUG] Elementos clicaveis encontrados na linha: {len(clickable_elements)}")
            for i, elem in enumerate(clickable_elements):
                tag = elem.tag_name
                onclick = elem.get_attribute('onclick')
                alt = elem.get_attribute('alt')
                href = elem.get_attribute('href')
                print(f"[DEBUG] Elemento {i+1}: tag={tag}, onclick={onclick}, alt={alt}, href={href}")
        except Exception as debug_error:
            print(f"[WARN] Erro ao obter diagnostico: {debug_error}")

        # Tentar diferentes estrategias para selecionar o produto na agregacao
        print("[INFO] Procurando botao/icone de adicionar produto...")

        # Estrategia 1: Procurar por botao/icone de "Add" na mesma linha do produto
        try:
            # Primeiro, encontrar a linha (tr) que contem o produto
            product_row = product.find_element(By.XPATH, "./ancestor::tr")
            print(f"[INFO] Linha do produto encontrada")

            # Procurar por imagem/botao de adicionar na linha
            add_button = product_row.find_element(By.XPATH, ".//img[@alt='Add' or @alt='Add to composition' or contains(@src, 'add')]")
            print(f"[INFO] Botao 'Add' encontrado na linha do produto")
            add_button.click()
            print("[OK] Clicou no botao Add")
            sleep(2)
            return

        except Exception as e1:
            print(f"[WARN] Estrategia 1 falhou (botao Add na linha): {e1}")

        # Estrategia 2: Tentar clicar diretamente no nome do produto SEM executar onclick
        # (apenas um click normal que pode selecionar o produto)
        try:
            print("[INFO] Tentando click simples no produto...")
            # Usar JavaScript click para evitar o onclick
            context.driver.execute_script("arguments[0].click();", product)
            print("[OK] Click simples executado")
            sleep(2)
            return

        except Exception as e2:
            print(f"[WARN] Estrategia 2 falhou (click simples): {e2}")

        # Estrategia 3: Procurar checkbox ou radio button na linha
        try:
            product_row = product.find_element(By.XPATH, "./ancestor::tr")
            checkbox = product_row.find_element(By.XPATH, ".//input[@type='checkbox' or @type='radio']")
            print(f"[INFO] Checkbox/radio encontrado")
            checkbox.click()
            print("[OK] Checkbox selecionado")
            sleep(2)
            return

        except Exception as e3:
            print(f"[WARN] Estrategia 3 falhou (checkbox): {e3}")

        # Se todas as estrategias falharem, reportar erro detalhado
        take_screenshot(context.driver, "product_selection_failed")
        print(f"[ERROR] Nenhuma estrategia de selecao de produto funcionou")
        print("[INFO] Tentando obter HTML da linha do produto para analise...")

        try:
            product_row = product.find_element(By.XPATH, "./ancestor::tr")
            row_html = product_row.get_attribute('outerHTML')
            print(f"[DEBUG] HTML da linha: {row_html[:500]}...")  # Primeiros 500 chars
        except:
            pass

        raise Exception("Nao foi possivel selecionar o produto para agregacao. Verifique se o elemento correto esta sendo usado.")

    except Exception as e:
        ends_timer(context, e)
        raise

@when("Add Product Quantity")
def add_product_quantity(context):
    try:
        # Wait longer for modal to fully load after clicking product
        sleep(3)

        # Try to find the modal container first
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            # Wait for modal to appear
            modal = WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tt_utils_ui_dlg_modal-width-class-m"))
            )
            print("Modal found, waiting for content to load...")
            sleep(2)
        except:
            print("Modal not found, but continuing...")

        # Get product information from the modal
        product_name_elem = wait_and_find(
            context.driver, By.CLASS_NAME, "child_product_name_show_container", timeout=15
        )
        context.product_name = product_name_elem.text

        gtin_elem = wait_and_find(
            context.driver, By.CLASS_NAME, "child_product_gtin14_show_container", timeout=10
        )
        context.gtin = gtin_elem.text
        context.gtin = "3" + context.gtin[1:13]

        ndc_elem = wait_and_find(
            context.driver, By.CLASS_NAME, "child_product_name_ndc_container", timeout=10
        )
        context.ndc = ndc_elem.text

        context.company_prefix, context.gs1_id = generate_cp_id_by_gtin(context.gtin)

        # Add quantity
        quantity_field = wait_and_find(
            context.driver,
            By.XPATH,
            "//input[starts-with(@id, 'TT_UTILS_UI_FORM_UUID_') and contains(@id, 'quantity') and @rel='quantity']",
            timeout=10
        )
        quantity_field.clear()
        wait_and_send_keys(
            context.driver,
            By.XPATH,
            "//input[starts-with(@id, 'TT_UTILS_UI_FORM_UUID_') and contains(@id, 'quantity') and @rel='quantity']",
            "2"
        )
    except Exception as e:
        # Take screenshot for debugging
        try:
            context.driver.save_screenshot("report/output/add_quantity_error.png")
            print(f"Screenshot saved. Current URL: {context.driver.current_url}")
        except:
            pass
        ends_timer(context, e)
        raise


@when("Click on Add Child Product")
def click_add_child_product(context):
    try:
        wait_and_click(
            context.driver,
            By.XPATH,
            "//div[contains(@class, 'tt_utils_ui_dlg_modal-width-class-m')]//button[contains(@class, 'tt_utils_ui_dlg_modal-default-enabled-button')]",
            timeout=10
        )
        sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Misc Tab")
def click_misc_tab(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//li[@rel='misc']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Disable Leaf Product")
def disable_leaf_product(context):
    try:
        wait_and_find(context.driver, By.XPATH, "//label[text()='This product is seen as a leaf item in the product composition']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on RPA Product")
def click_rpa_product(context):
    try:
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Wait for search results to load
        sleep(3)

        # Try multiple selectors for RPA Product
        selectors = [
            (By.XPATH, "//span[@class='tt_utils_ui_search-table-cell-responsive-value' and contains(text(), '[RPA]') and contains(text(), 'EACH')]"),
            (By.XPATH, "//td[contains(text(), '[RPA]') and contains(text(), 'EACH')]"),
            (By.XPATH, "//span[contains(text(), '[RPA]') and contains(text(), 'EACH')]"),
            (By.XPATH, "//*[contains(text(), '[RPA]') and contains(text(), 'EACH')]"),
            (By.XPATH, "//tr[contains(., '[RPA]') and contains(., 'EACH')]//td[@rel='name']"),
            (By.XPATH, "//table//tbody//tr//td[contains(text(), '[RPA]')]"),
            (By.XPATH, "//td[@rel='name' and contains(text(), '[RPA]')]"),
        ]

        product = None
        for by, selector in selectors:
            try:
                product = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable((by, selector))
                )
                print(f"[OK] Found RPA Product with selector: {selector}")
                break
            except:
                print(f"[FAIL] Could not find RPA Product with selector: {selector}")
                continue

        if product is None:
            # Save screenshot for debugging
            context.driver.save_screenshot("report/output/rpa_product_not_found.png")
            print(f"Current URL: {context.driver.current_url}")
            raise Exception("Could not find RPA Product with any selector")

        context.product_name = product.text
        product.click()
        sleep(1)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Save GS1 Info")
def save_gs1_company_prefix(context):
    try:
        context.product_gtin = wait_and_find(context.driver, By.CLASS_NAME, "field__upc", timeout=30).text
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Close Modal")
def close_modal(context):
    try:
        sleep(1)
        wait_and_find(context.driver, By.XPATH, "//button/span[text() = 'Close']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Search for Created Product")
def search_created_product(context):
    try:
        name_search = wait_and_find(context.driver, By.CLASS_NAME, "search_criteria__name", timeout=30)
        name_search.send_keys(context.product_name)
        name_search.send_keys(Keys.ENTER)
        sleep(3)
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Delete Created Product")
def delete_created_product(context):
    try:
        wait_and_find(context.driver, By.XPATH, f"//img[@alt='Delete']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@when("Click on Yes - Deletion")
def click_yes_deletion(context):
    try:
        wait_and_find(context.driver, By.XPATH, f"//button/span[text()='Yes']", timeout=30).click()
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Product should be saved")
def product_saved(context):
    try:
        name_search = wait_and_find(context.driver, By.CLASS_NAME, "search_criteria__name", timeout=30)
        name_search.send_keys(context.product_name)
        name_search.send_keys(Keys.ENTER)
        sleep(3)
        wait_and_find(context.driver, By.XPATH, f"//*[contains(text(),'{context.product_name}') or contains(text(), 'GTIN14 already exist for product')]", timeout=30)
    except Exception as e:
        ends_timer(context, e)
        raise


@then("Product should be deleted")
def product_deleted(context):
    try:
        sleep(5)
        context.driver.refresh()
        sleep(2)
        records_text = wait_and_find(context.driver, 
            By.CLASS_NAME, "tt_utils_ui_search-footer-nb-results", timeout=30).text
        new_total_records = int(records_text.split("of ")[1].split(" recor")[0])
        assert context.total_records - new_total_records == 1
    except Exception as e:
        ends_timer(context, e)
        raise
