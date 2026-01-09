#!/usr/bin/env python3
"""
Script para debugar o botão de busca na página de Products
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar Chrome
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

try:
    # Login
    print("[INFO] Fazendo login...")
    driver.get("https://qualityportal.qa-test.tracktraceweb.com/auth")

    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "auth__login_form__username"))
    )
    username.send_keys("teste@teste.com")
    driver.find_element(By.ID, "auth__login_form__step1_next_btn").click()

    time.sleep(2)

    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "auth__login_form__password"))
    )
    password.send_keys("Mudar@12345342")
    driver.find_element(By.ID, "auth__login_form__step2_next_btn").click()

    time.sleep(5)

    # Ir para Products
    print("[INFO] Navegando para Products...")
    driver.get("https://qualityportal.qa-test.tracktraceweb.com/products/")
    time.sleep(5)

    # Preencher campo de busca
    print("[INFO] Preenchendo campo de busca...")
    name_field = driver.find_element(By.XPATH, "//input[@rel='name']")
    name_field.clear()
    name_field.send_keys("[RPA]")
    time.sleep(2)

    # Pegar screenshot ANTES de clicar
    driver.save_screenshot("/home/filipe/Área de trabalho/RPA/report/output/screenshots/debug_before_search.png")
    print("[SCREENSHOT] Antes da busca salvo")

    # Procurar todos os elementos que podem ser o botão de busca
    print("\n[INFO] Procurando elementos que podem ser o botão de busca...")

    # Tentar encontrar por classes do portal
    candidates = []

    try:
        elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'search') or contains(@class, 'filter') or contains(@class, 'button')]")
        print(f"\n[INFO] Encontrados {len(elements)} elementos com 'search', 'filter' ou 'button' na classe")
        for i, elem in enumerate(elements[:20]):  # Limitar a 20
            try:
                tag = elem.tag_name
                classes = elem.get_attribute('class')
                visible = elem.is_displayed()
                if visible:
                    print(f"  [{i}] {tag}.{classes} (visível)")
                    candidates.append((i, elem, f"{tag}.{classes}"))
            except:
                pass
    except Exception as e:
        print(f"[ERROR] {e}")

    # Procurar o botão de lupa - inspecionar HTML
    print("\n[INFO] Inspecionando estrutura HTML ao redor do campo de nome...")
    try:
        # Pegar o elemento pai do input de nome
        name_parent = driver.execute_script("""
            var input = arguments[0];
            var parent = input;
            for(var i = 0; i < 5; i++) {
                parent = parent.parentElement;
                if (parent.className && parent.className.includes('search-criterias')) {
                    break;
                }
            }
            return parent.outerHTML.substring(0, 3000);
        """, name_field)
        print(f"[HTML] Estrutura pai (primeiros 2000 chars):\n{name_parent[:2000]}")
    except Exception as e:
        print(f"[ERRO] {e}")

    # Procurar SVG ou ícone de lupa (magnifying glass)
    print("\n[INFO] Procurando ícone de lupa (SVG, IMG, I, etc)...")
    icon_selectors = [
        "//svg[contains(@class, 'search') or contains(@class, 'magnify')]",
        "//*[name()='svg']//parent::*[contains(@class, 'search') or contains(@class, 'filter')]",
        "//i[contains(@class, 'fa-search') or contains(@class, 'magnifying')]",
        "//img[contains(@alt, 'search') or contains(@src, 'search')]",
        # Procurar elemento clicável perto do campo de filtros
        "//div[contains(@class, 'search-criterias')]//following-sibling::*",
        "//div[contains(@class, 'search-criterias')]/parent::*//*[contains(@class, 'button')]",
    ]

    for selector in icon_selectors:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            if elements:
                print(f"  [ENCONTRADO {len(elements)} elemento(s)] {selector}")
                for elem in elements[:3]:
                    if elem.is_displayed():
                        tag = elem.tag_name
                        classes = elem.get_attribute('class') or ''
                        print(f"    -> {tag}.{classes}")
        except Exception as e:
            pass

    # Tentar clicar no botão de PESQUISAR correto
    print("\n[INFO] Tentando clicar no botão 'Pesquisar'...")
    try:
        search_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'tt_utils_ui_search-search-criterias-btns-search')]")
        print(f"[OK] Botão encontrado: {search_btn.get_attribute('class')}")
        search_btn.click()
        print(f"[OK] Botão CLICADO!")
    except Exception as e:
        print(f"[ERRO] {e}")

    time.sleep(5)

    # Screenshot DEPOIS
    driver.save_screenshot("/home/filipe/Área de trabalho/RPA/report/output/screenshots/debug_after_search.png")
    print("\n[SCREENSHOT] Depois da busca salvo")

    # Verificar se apareceu resultado
    try:
        rows = driver.find_elements(By.XPATH, "//table//tr | //tbody//tr")
        print(f"\n[INFO] Tabela tem {len(rows)} linhas após busca")

        rpa_rows = driver.find_elements(By.XPATH, "//td[contains(text(), '[RPA]')]")
        print(f"[INFO] Linhas com [RPA]: {len(rpa_rows)}")
    except Exception as e:
        print(f"[ERROR] Ao verificar tabela: {e}")

finally:
    print("\n[INFO] Fechando browser...")
    time.sleep(2)
    driver.quit()
    print("[INFO] Done!")
