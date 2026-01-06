"""
Environment hooks for Behave tests
Otimizado para reutilizar browser por feature (reduz tempo de login)
"""

import sys
import codecs
import time

# Fix Unicode encoding issues on Windows
if sys.platform == 'win32':
    # Configure stdout to handle Unicode properly
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')


def before_all(context):
    """
    Hook executado antes de todos os testes.
    """
    print("\n" + "=" * 80)
    print("INICIANDO SUITE DE TESTES")
    print("=" * 80)

    # Inicializar flags globais no _root (persistente entre cenarios)
    context._root_driver = None
    context._root_browser_ready = False
    context._root_logged_in = False


def after_all(context):
    """
    Hook executado apos todos os testes.
    """
    print("\n" + "=" * 80)
    print("TESTES FINALIZADOS")
    print("=" * 80)

    # Garantir que browser seja fechado no final
    _close_browser_safe(context, use_root=True)


def before_feature(context, feature):
    """
    Hook executado UMA VEZ antes de todos os cenarios da feature.
    """
    print(f"\n{'=' * 60}")
    print(f"FEATURE: {feature.name}")
    print(f"{'=' * 60}")

    # Resetar flags para nova feature (fecha browser da feature anterior)
    _close_browser_safe(context, use_root=True)
    context._root_browser_ready = False
    context._root_logged_in = False
    context.feature_name = feature.name


def after_feature(context, feature):
    """
    Hook executado UMA VEZ apos todos os cenarios da feature.
    Browser sera fechado no before_feature da proxima feature ou no after_all.
    """
    print(f"\n<<< Feature '{feature.name}' finalizada")
    # NAO fechar browser aqui - sera fechado no before_feature da proxima feature


def before_scenario(context, scenario):
    """
    Hook executado antes de cada cenario.
    """
    print(f"\n>>> Iniciando cenario: {scenario.name}")

    # Se cenario tem tag @skip, nao fazer nada
    if 'skip' in scenario.effective_tags:
        print(f"    [SKIP] Cenario marcado como @skip")
        return

    # Copiar driver do _root para o contexto do cenario (para compatibilidade)
    if hasattr(context, '_root_driver') and context._root_driver:
        context.driver = context._root_driver

    # Limpar modais que possam ter ficado abertos do cenario anterior
    if hasattr(context, '_root_driver') and context._root_driver and context._root_browser_ready:
        _close_modals_safe(context)


def after_scenario(context, scenario):
    """
    Hook executado apos cada cenario.
    NAO fecha o browser aqui - sera fechado no before_feature da proxima feature.
    """
    status = "PASSED" if scenario.status.name == "passed" else "FAILED"
    print(f"<<< Cenario '{scenario.name}' finalizado: {status}")

    # Sincronizar driver do cenario com _root (caso tenha sido criado/modificado)
    if hasattr(context, 'driver') and context.driver:
        context._root_driver = context.driver

    # Se cenario falhou, capturar screenshot e logs para diagnóstico
    if scenario.status.name != "passed":
        print(f"    [!] Cenario falhou - capturando diagnostico")
        _capture_failure_diagnostics(context, scenario)
        context._root_logged_in = False
        # Fechar browser para garantir estado limpo no proximo cenario
        _close_browser_safe(context, use_root=True)
        context._root_browser_ready = False


def _capture_failure_diagnostics(context, scenario):
    """
    Captura screenshot e informacoes de diagnostico quando um cenario falha.
    """
    import os
    from datetime import datetime

    driver = getattr(context, 'driver', None) or getattr(context, '_root_driver', None)
    if not driver:
        print("    [WARN] Driver nao disponivel para captura de diagnostico")
        return

    try:
        # Criar diretorio para screenshots
        screenshot_dir = os.path.join(os.getcwd(), "report", "output", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        # Nome do arquivo baseado no cenario e timestamp
        safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in scenario.name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)

        # Capturar screenshot
        driver.save_screenshot(filepath)
        print(f"    [DIAG] Screenshot salvo: {filepath}")

        # Capturar URL atual
        current_url = driver.current_url
        print(f"    [DIAG] URL atual: {current_url}")

        # Capturar titulo da pagina
        page_title = driver.title
        print(f"    [DIAG] Titulo da pagina: {page_title}")

        # Capturar tamanho da janela
        window_size = driver.get_window_size()
        print(f"    [DIAG] Tamanho da janela: {window_size['width']}x{window_size['height']}")

        # Verificar se ha alertas
        try:
            alert = driver.switch_to.alert
            print(f"    [DIAG] Alerta presente: {alert.text}")
        except:
            pass

        # Capturar HTML da pagina para analise (apenas primeiros 2000 chars)
        try:
            page_source = driver.page_source[:2000]
            html_file = filepath.replace('.png', '_source.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"    [DIAG] HTML salvo: {html_file}")
        except Exception as e:
            print(f"    [WARN] Falha ao salvar HTML: {e}")

    except Exception as e:
        print(f"    [WARN] Falha ao capturar diagnostico: {e}")


def _close_browser_safe(context, use_root=False):
    """
    Fecha o browser de forma segura com retry logic.
    """
    # Determinar qual driver usar
    if use_root:
        driver = getattr(context, '_root_driver', None)
    else:
        driver = getattr(context, 'driver', None)

    if driver is not None:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                time.sleep(0.3)
                driver.quit()
                print(f"[OK] Browser fechado com sucesso")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    print(f"[WARN] Falha ao fechar browser: {e}")

        # Limpar referencias
        if use_root:
            context._root_driver = None
            context._root_browser_ready = False
            context._root_logged_in = False
        context.driver = None


def _close_modals_safe(context):
    """
    Tenta fechar modais que possam estar abertos.
    """
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Tentar fechar modal de dismiss
        try:
            dismiss_btn = WebDriverWait(context.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Dismiss']"))
            )
            dismiss_btn.click()
            print("    [OK] Modal Dismiss fechado")
        except:
            pass

        # Tentar fechar modal de close
        try:
            close_btn = WebDriverWait(context.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Close']"))
            )
            close_btn.click()
            print("    [OK] Modal Close fechado")
        except:
            pass

        # Tentar fechar botao X generico
        try:
            x_buttons = context.driver.find_elements(By.XPATH, "//span[contains(@class, 'modal-close')]")
            for btn in x_buttons:
                if btn.is_displayed():
                    btn.click()
                    print("    [OK] Modal X fechado")
                    break
        except:
            pass

    except Exception as e:
        pass  # Ignorar erros ao fechar modais
