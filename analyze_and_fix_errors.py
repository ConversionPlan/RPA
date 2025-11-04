#!/usr/bin/env python3
"""
Script para analisar e corrigir automaticamente erros comuns nos testes RPA
"""
import json
import os
import re
from collections import defaultdict

def analyze_test_results(json_file="all_tests_result.json"):
    """Analisa resultados dos testes e identifica padrões de erro"""
    with open(json_file, 'r') as f:
        results = json.load(f)

    errors = defaultdict(list)
    error_patterns = defaultdict(int)

    for feature in results:
        feature_name = feature.get('name', 'Unknown')
        for scenario in feature.get('elements', []):
            if scenario.get('status') == 'error':
                scenario_name = scenario.get('name', 'Unknown')

                # Encontrar o step que falhou
                for step in scenario.get('steps', []):
                    if step.get('result', {}).get('status') == 'error':
                        step_name = step.get('name', '')
                        location = step.get('match', {}).get('location', '')
                        duration = step.get('result', {}).get('duration', 0)

                        error_info = {
                            'feature': feature_name,
                            'scenario': scenario_name,
                            'step': step_name,
                            'location': location,
                            'duration': duration
                        }

                        # Categorizar por tipo de erro
                        if 'Open sandwich menu' in step_name:
                            errors['sandwich_menu'].append(error_info)
                            error_patterns['sandwich_menu'] += 1
                        elif 'Is Logged In' in step_name:
                            errors['login'].append(error_info)
                            error_patterns['login'] += 1
                        elif duration > 60:  # Timeout errors (>60s)
                            errors['timeout'].append(error_info)
                            error_patterns['timeout'] += 1
                        else:
                            errors['other'].append(error_info)
                            error_patterns['other'] += 1
                        break  # Só pegar o primeiro erro de cada cenário

    return errors, error_patterns

def print_analysis(errors, error_patterns):
    """Imprime análise dos erros"""
    print("\n" + "="*80)
    print("ANÁLISE DE ERROS DOS TESTES RPA")
    print("="*80)

    total_errors = sum(error_patterns.values())
    print(f"\nTotal de cenários com erro: {total_errors}")

    print("\nDISTRIBUICAO DE ERROS:")
    for error_type, count in sorted(error_patterns.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_errors) * 100 if total_errors > 0 else 0
        print(f"  - {error_type}: {count} ({percentage:.1f}%)")

    # Detalhes por categoria
    print("\n" + "="*80)
    print("DETALHES POR CATEGORIA DE ERRO:")
    print("="*80)

    # 1. Erros de Sandwich Menu
    if errors['sandwich_menu']:
        print(f"\n[SANDWICH MENU] SANDWICH MENU ERRORS ({len(errors['sandwich_menu'])} ocorrências):")
        for err in errors['sandwich_menu'][:3]:  # Mostrar até 3 exemplos
            print(f"  - {err['feature']} > {err['scenario']}")
            print(f"    Duration: {err['duration']:.1f}s")
        if len(errors['sandwich_menu']) > 3:
            print(f"  ... e mais {len(errors['sandwich_menu']) - 3} erros")

    # 2. Erros de Login
    if errors['login']:
        print(f"\n[LOGIN] LOGIN ERRORS ({len(errors['login'])} ocorrências):")
        for err in errors['login'][:3]:
            print(f"  - {err['feature']} > {err['scenario']}")
            print(f"    Duration: {err['duration']:.1f}s")

    # 3. Erros de Timeout
    if errors['timeout']:
        print(f"\n[TIMEOUT] TIMEOUT ERRORS ({len(errors['timeout'])} ocorrências):")
        for err in errors['timeout'][:5]:
            print(f"  - {err['feature']} > {err['scenario']}")
            print(f"    Step: {err['step']}")
            print(f"    Duration: {err['duration']:.1f}s")
            print(f"    Location: {err['location']}")

    # 4. Outros erros
    if errors['other']:
        print(f"\n[OTHER] OTHER ERRORS ({len(errors['other'])} ocorrências):")
        for err in errors['other'][:5]:
            print(f"  - {err['feature']} > {err['scenario']}")
            print(f"    Step: {err['step']}")
            print(f"    Location: {err['location']}")

def suggest_fixes(errors, error_patterns):
    """Sugere correções baseadas nos erros encontrados"""
    print("\n" + "="*80)
    print("CORRECOES SUGERIDAS:")
    print("="*80)

    fixes = []

    # 1. Sandwich Menu com muitos timeouts
    if error_patterns['sandwich_menu'] > 0:
        fixes.append({
            'priority': 'HIGH',
            'issue': 'Open sandwich menu failing with timeout',
            'occurrences': error_patterns['sandwich_menu'],
            'files': ['features/steps/product.py'],
            'solution': """
1. Aumentar timeout para 90 segundos no pior caso
2. Adicionar mais seletores para o menu
3. Implementar scroll antes de clicar
4. Adicionar retry com page refresh
"""
        })

    # 2. Login issues
    if error_patterns['login'] > 0:
        fixes.append({
            'priority': 'HIGH',
            'issue': 'Login failing',
            'occurrences': error_patterns['login'],
            'files': ['features/steps/auth.py'],
            'solution': """
1. Aumentar timeout de login
2. Adicionar verificação de redirect
3. Limpar cookies antes do login
4. Adicionar retry logic
"""
        })

    # 3. Timeout genérico
    if error_patterns['timeout'] > 0:
        avg_timeout = sum(e['duration'] for e in errors['timeout']) / len(errors['timeout'])
        fixes.append({
            'priority': 'MEDIUM',
            'issue': f'General timeout errors (avg: {avg_timeout:.1f}s)',
            'occurrences': error_patterns['timeout'],
            'files': ['features/steps/*.py'],
            'solution': """
1. Substituir find_element por wait_and_find com timeout maior
2. Adicionar wait_and_click em todas as ações
3. Implementar retry logic global
4. Adicionar page ready check antes de ações
"""
        })

    # Imprimir correções
    for fix in sorted(fixes, key=lambda x: x['occurrences'], reverse=True):
        print(f"\n[{fix['priority']}] {fix['issue']}")
        print(f"   Ocorrencias: {fix['occurrences']}")
        print(f"   Arquivos afetados: {', '.join(fix['files'])}")
        print(f"   Solucao sugerida:{fix['solution']}")

    return fixes

def generate_fix_commands(fixes):
    """Gera comandos para aplicar correções"""
    print("\n" + "="*80)
    print("COMANDOS PARA APLICAR CORRECOES:")
    print("="*80)

    if any('sandwich menu' in f['issue'].lower() for f in fixes):
        print("""
# 1. Corrigir sandwich menu com timeout aumentado e mais robustez
python apply_sandwich_menu_fix.py
""")

    if any('login' in f['issue'].lower() for f in fixes):
        print("""
# 2. Corrigir login com retry e timeouts maiores
python apply_login_fix.py
""")

    print("""
# 3. Aplicar correções gerais de robustez
python apply_general_fixes.py

# 4. Rodar testes novamente
python -m behave --format json.pretty --outfile all_tests_result.json
""")

if __name__ == "__main__":
    print("Analisando resultados dos testes...")

    # Analisar erros
    errors, error_patterns = analyze_test_results()

    # Imprimir análise
    print_analysis(errors, error_patterns)

    # Sugerir correções
    fixes = suggest_fixes(errors, error_patterns)

    # Gerar comandos
    generate_fix_commands(fixes)

    print("\nAnalise concluida!")