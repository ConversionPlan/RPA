"""
Environment hooks for Behave tests - Simplified version
"""

import sys
import codecs

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


def after_all(context):
    """
    Hook executado após todos os testes.
    """
    print("\n" + "=" * 80)
    print("TESTES FINALIZADOS")
    print("=" * 80)


def before_scenario(context, scenario):
    """
    Hook executado antes de cada cenário.
    """
    print(f"\n>>> Iniciando cenário: {scenario.name}")


def after_scenario(context, scenario):
    """
    Hook executado após cada cenário.
    """
    status = "PASSED" if scenario.status.name == "passed" else "FAILED"
    print(f"<<< Cenário '{scenario.name}' finalizado: {status}")