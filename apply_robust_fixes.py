#!/usr/bin/env python3
"""
Script para aplicar correções robustas automaticamente nos testes RPA
Baseado na análise de erros, aplica melhorias em todos os arquivos problemáticos
"""

import os
import re
import glob

def add_robust_imports(file_path):
    """Adiciona imports necessários para funções robustas"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Se já tem os imports, não adicionar novamente
    if 'from features.steps.utils import wait_and_click' in content:
        return content

    # Adicionar imports após outros imports from behave
    if 'from behave import' in content:
        import_line = "from features.steps.utils import wait_and_click, wait_and_find, wait_and_send_keys\n"

        # Encontrar onde adicionar
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('from behave import'):
                # Adicionar após os imports do behave
                j = i + 1
                while j < len(lines) and (lines[j].startswith('from ') or lines[j].startswith('import ')):
                    j += 1
                lines.insert(j, import_line)
                break
        content = '\n'.join(lines)

    return content

def fix_find_element_calls(content):
    """Substitui find_element direto por wait_and_find com timeout"""

    # Pattern para find_element sem wait
    patterns = [
        # context.driver.find_element(by=By.X, value=Y)
        (r'context\.driver\.find_element\(\s*by=([^,]+),\s*value=([^)]+)\)',
         r'wait_and_find(context.driver, \1, \2, timeout=30)'),

        # context.driver.find_element(By.X, Y)
        (r'context\.driver\.find_element\(([^,]+),\s*([^)]+)\)',
         r'wait_and_find(context.driver, \1, \2, timeout=30)'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    return content

def fix_click_calls(content):
    """Substitui .click() direto por wait_and_click com timeout"""

    # Pattern para elemento.click() após find_element
    pattern = r'(.*?)\.click\(\)'

    def replace_click(match):
        line = match.group(0)
        # Se já é wait_and_click, não substituir
        if 'wait_and_click' in line:
            return line
        # Se tem find_element, substituir todo o comando
        if 'find_element' in line:
            # Extrair os parâmetros do find_element
            by_match = re.search(r'by=([^,]+),\s*value=([^)]+)', line)
            if by_match:
                return f'wait_and_click(context.driver, {by_match.group(1)}, {by_match.group(2)}, timeout=30)'

            by_match2 = re.search(r'find_element\(([^,]+),\s*([^)]+)\)', line)
            if by_match2:
                return f'wait_and_click(context.driver, {by_match2.group(1)}, {by_match2.group(2)}, timeout=30)'

        return line

    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if '.click()' in line and 'find_element' in line:
            # Linha completa com find_element e click
            new_line = re.sub(pattern, replace_click, line)
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    return '\n'.join(new_lines)

def fix_sandwich_menu_timeout(content):
    """Aumenta timeout específico do sandwich menu"""

    # Se é o arquivo product.py e tem a função open_sandwich_menu
    if '@when("Open sandwich menu")' in content:
        # Aumentar timeout dos waits dentro da função
        content = content.replace('WebDriverWait(context.driver, 2)', 'WebDriverWait(context.driver, 5)')
        content = content.replace('WebDriverWait(context.driver, 3)', 'WebDriverWait(context.driver, 10)')
        content = content.replace('WebDriverWait(context.driver, 5)', 'WebDriverWait(context.driver, 10)')

        # Adicionar mais seletores se ainda não tem
        if 'sidebar_menu_toggle_enabled' not in content:
            old_selectors = '''        selectors = [
            "//div[contains(@class, 'sidebar_menu_toggle_dis')]/a",
            "//div[contains(@class, 'sidebar_menu_toggle_en')]/a",  # Enabled state
            "//div[contains(@class, 'sidebar_menu_toggle')]/a",
            "//a[contains(@class, 'sidebar-toggle')]",
            "//*[@id='sidebar-toggle']",
            "//i[contains(@class, 'fa-bars')]/parent::a"  # Font-awesome bars icon
        ]'''

            new_selectors = '''        selectors = [
            "//div[contains(@class, 'sidebar_menu_toggle_dis')]/a",
            "//div[contains(@class, 'sidebar_menu_toggle_en')]/a",
            "//div[contains(@class, 'sidebar_menu_toggle_enabled')]/a",
            "//div[contains(@class, 'sidebar_menu_toggle')]/a",
            "//a[contains(@class, 'sidebar-toggle')]",
            "//a[@class='sidebar-toggle']",
            "//*[@id='sidebar-toggle']",
            "//i[contains(@class, 'fa-bars')]/parent::a",
            "//button[contains(@class, 'menu-toggle')]",
            "//div[@class='menu-toggle']//a"
        ]'''

            if old_selectors in content:
                content = content.replace(old_selectors, new_selectors)

    return content

def fix_login_timeout(content):
    """Aumenta timeout para login"""

    # Se tem funções de login
    if 'Is Logged In' in content or 'Enter Username' in content:
        # Aumentar timeouts
        content = content.replace('WebDriverWait(context.driver, 10)', 'WebDriverWait(context.driver, 30)')
        content = content.replace('time.sleep(1)', 'time.sleep(2)')
        content = content.replace('sleep(1)', 'sleep(2)')

        # Adicionar clear cookies se ainda não tem
        if 'delete_all_cookies' not in content and '@given("Is Logged In")' in content:
            old_login = '''@given("Is Logged In")
def step_impl(context):
    context.driver = get_driver()'''

            new_login = '''@given("Is Logged In")
def step_impl(context):
    context.driver = get_driver()
    context.driver.delete_all_cookies()  # Limpar cookies antes do login'''

            if old_login in content:
                content = content.replace(old_login, new_login)

    return content

def add_retry_logic(content):
    """Adiciona retry logic em funções críticas"""

    # Pattern para adicionar retry em funções que falham frequentemente
    functions_to_retry = [
        'click_manufacture_lot_serial_request',
        'click_list_search_containers',
        'click_create_sales_order',
        'click_add_address',
        'click_pencil_next_to_name'
    ]

    for func_name in functions_to_retry:
        if func_name in content:
            # Verificar se já tem retry
            if 'for attempt in range(3)' not in content:
                # Adicionar retry wrapper
                pattern = f'def {func_name}\\(context\\):\\n    try:'
                replacement = f'''def {func_name}(context):
    for attempt in range(3):
        try:
            print(f"Tentativa {{attempt + 1}} de 3 para {func_name}")'''

                content = content.replace(pattern, replacement)

                # Adicionar except com retry
                old_except = '''    except Exception as e:
        ends_timer(context, e)
        raise'''

                new_except = '''        except Exception as e:
            if attempt < 2:
                print(f"Erro na tentativa {{attempt + 1}}, tentando novamente...")
                sleep(3)
                continue
            else:
                ends_timer(context, e)
                raise'''

                content = content.replace(old_except, new_except)

    return content

def process_file(file_path):
    """Processa um arquivo aplicando todas as correções"""

    print(f"Processando: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Aplicar correções
    content = add_robust_imports(file_path)
    content = fix_find_element_calls(content)
    content = fix_click_calls(content)
    content = fix_sandwich_menu_timeout(content)
    content = fix_login_timeout(content)
    content = add_retry_logic(content)

    # Salvar apenas se houve mudanças
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] Arquivo atualizado com correcoes")
    else:
        print(f"  - Nenhuma mudança necessária")

    return content != original_content

def main():
    """Função principal"""

    print("="*80)
    print("APLICANDO CORREÇÕES ROBUSTAS NOS TESTES RPA")
    print("="*80)

    # Arquivos prioritários baseados na análise
    priority_files = [
        'features/steps/product.py',
        'features/steps/auth.py',
        'features/steps/inbound.py',
        'features/steps/outbound.py',
        'features/steps/inventory.py',
        'features/steps/manufacture.py',
        'features/steps/container.py',
        'features/steps/trading_partner.py',
        'features/steps/location.py'
    ]

    updated_files = []

    # Processar arquivos prioritários
    print("\nProcessando arquivos prioritários...")
    for file_path in priority_files:
        if os.path.exists(file_path):
            if process_file(file_path):
                updated_files.append(file_path)
        else:
            print(f"  ! Arquivo não encontrado: {file_path}")

    # Processar outros arquivos .py em features/steps
    print("\nProcessando outros arquivos...")
    other_files = glob.glob('features/steps/*.py')
    for file_path in other_files:
        if file_path.replace('\\', '/') not in [f.replace('\\', '/') for f in priority_files]:
            if process_file(file_path):
                updated_files.append(file_path)

    # Resumo
    print("\n" + "="*80)
    print("RESUMO DAS CORREÇÕES")
    print("="*80)
    print(f"\nTotal de arquivos atualizados: {len(updated_files)}")

    if updated_files:
        print("\nArquivos modificados:")
        for f in updated_files:
            print(f"  - {f}")

    print("\n[OK] Correcoes aplicadas com sucesso!")
    print("\nPróximos passos:")
    print("1. Revisar as mudanças com: git diff")
    print("2. Testar as correções com: python -m behave features/")
    print("3. Commit das mudanças com: git add -A && git commit -m 'Aplica correções robustas nos testes'")

if __name__ == "__main__":
    main()