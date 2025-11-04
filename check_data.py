from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--lang=en-US")

driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(service=Service(driver_path), options=options)

try:
    print("=" * 60)
    print("Verificando dados no portal QualityPortal")
    print("=" * 60)

    # Login
    print("\n1. Fazendo login...")
    driver.get("https://qualityportal.qa-test.tracktraceweb.com/auth")
    driver.implicitly_wait(5)

    # Username
    driver.find_element(By.ID, "auth__login_form__username").send_keys("teste@teste.com")
    driver.find_element(By.ID, "auth__login_form__step1_next_btn").click()
    time.sleep(2)

    # Password
    time.sleep(1)
    driver.find_element(By.ID, "auth__login_form__password").send_keys("Mudar@12345342")
    time.sleep(1)
    driver.find_element(By.ID, "auth__login_form__step2_next_btn").click()
    time.sleep(5)

    print(f"   Login bem-sucedido! URL: {driver.current_url}")

    # Check Products
    print("\n2. Verificando Produtos...")
    driver.get("https://qualityportal.qa-test.tracktraceweb.com/products/")
    time.sleep(5)

    # Try to find search box and search for RPA
    try:
        # Use the correct selector from the test code
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@rel='name']"))
        )
        search_box.clear()
        search_box.send_keys("[RPA]")
        from selenium.webdriver.common.keys import Keys
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # Try to find product rows
        products = driver.find_elements(By.XPATH, "//table//tbody//tr")
        print(f"   Produtos encontrados: {len(products)}")

        if len(products) > 0:
            for i, product in enumerate(products[:5], 1):  # Show first 5
                try:
                    text = product.text
                    print(f"   Produto {i}: {text[:200]}")
                except:
                    pass
        else:
            print("   Nenhum produto RPA encontrado! Voce precisa criar produtos RPA primeiro.")
    except Exception as e:
        print(f"   Erro ao buscar produtos: {str(e)}")

    # Check Trading Partners
    print("\n3. Verificando Trading Partners (Vendors)...")
    driver.get("https://qualityportal.qa-test.tracktraceweb.com/trading-partners/")
    time.sleep(5)

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@rel='name']"))
        )
        search_box.clear()
        search_box.send_keys("[RPA]")
        from selenium.webdriver.common.keys import Keys
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        partners = driver.find_elements(By.XPATH, "//table//tbody//tr")
        print(f"   Trading Partners encontrados: {len(partners)}")

        if len(partners) > 0:
            for i, partner in enumerate(partners[:5], 1):
                try:
                    text = partner.text
                    print(f"   Partner {i}: {text[:200]}")
                except:
                    pass
        else:
            print("   Nenhum trading partner RPA encontrado! Voce precisa criar vendors RPA primeiro.")
    except Exception as e:
        print(f"   Erro ao buscar trading partners: {str(e)}")

    # Check Locations
    print("\n4. Verificando Locations...")
    driver.get("https://qualityportal.qa-test.tracktraceweb.com/locations/")
    time.sleep(5)

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@rel='name']"))
        )
        search_box.clear()
        search_box.send_keys("[RPA]")
        from selenium.webdriver.common.keys import Keys
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        locations = driver.find_elements(By.XPATH, "//table//tbody//tr")
        print(f"   Locations encontradas: {len(locations)}")

        if len(locations) > 0:
            for i, location in enumerate(locations[:5], 1):
                try:
                    text = location.text
                    print(f"   Location {i}: {text[:200]}")
                except:
                    pass
        else:
            print("   Nenhuma location RPA encontrada! Voce precisa criar locations RPA primeiro.")
    except Exception as e:
        print(f"   Erro ao buscar locations: {str(e)}")

    print("\n" + "=" * 60)
    print("Verificacao concluida!")
    print("=" * 60)

    # Keep browser open for 5 seconds so you can see
    time.sleep(5)

finally:
    driver.quit()
