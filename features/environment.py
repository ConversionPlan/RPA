"""
Environment hooks for Behave tests
Fixes monitoring system Status object serialization issues and Unicode encoding
"""

import json
import os
import sys
import codecs
from datetime import datetime
from behave.model_core import Status

# Fix Unicode encoding issues on Windows
if sys.platform == 'win32':
    # Configure stdout to handle Unicode properly
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')


def after_scenario(context, scenario):
    """
    Hook executado após cada cenário.
    Corrige o problema de serialização do objeto Status.
    """
    try:
        # Se o cenário tem status, converte para string
        if hasattr(scenario, 'status'):
            # Status é um enum no Behave, precisamos converter para string
            if isinstance(scenario.status, Status):
                status_str = scenario.status.name.lower()  # 'passed', 'failed', etc.
            else:
                status_str = str(scenario.status).lower()

            # Se houver algum sistema de monitoramento tentando processar o status
            # garantimos que ele receba uma string
            scenario._status_str = status_str

        # Log básico do resultado
        print(f"\n[Environment Hook] Cenário '{scenario.name}' finalizado: {getattr(scenario, '_status_str', 'unknown')}")

    except Exception as e:
        # Captura qualquer erro para não quebrar o teste
        print(f"[Environment Hook] Aviso em after_scenario: {e}")
        pass


def after_all(context):
    """
    Hook executado após todos os testes.
    Corrige problemas de serialização JSON com objetos Status.
    """
    try:
        # Se houver dados de monitoramento para salvar
        monitoring_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'report', 'monitoring')

        if os.path.exists(monitoring_dir):
            # Processa arquivos JSON existentes para corrigir Status
            for filename in os.listdir(monitoring_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(monitoring_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Corrige representações de Status no JSON
                        content = content.replace('"Status.passed"', '"passed"')
                        content = content.replace('"Status.failed"', '"failed"')
                        content = content.replace('"Status.error"', '"error"')
                        content = content.replace('"Status.skipped"', '"skipped"')

                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)

                    except Exception as e:
                        print(f"[Environment Hook] Não foi possível processar {filename}: {e}")
                        pass

        print("\n[Environment Hook] Testes finalizados com sucesso")

    except Exception as e:
        # Captura qualquer erro para não quebrar o relatório final
        print(f"[Environment Hook] Aviso em after_all: {e}")
        pass


def before_all(context):
    """
    Hook executado antes de todos os testes.
    """
    print("\n" + "=" * 80)
    print("INICIANDO SUITE DE TESTES")
    print("=" * 80)

    # Garante que o diretório de monitoramento existe
    monitoring_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'report', 'monitoring')
    os.makedirs(monitoring_dir, exist_ok=True)


def before_scenario(context, scenario):
    """
    Hook executado antes de cada cenário.
    """
    try:
        # Safe print with encoding handling
        scenario_name = scenario.name.encode('ascii', 'ignore').decode('ascii')
        print(f"\n[Environment Hook] Iniciando cenário: {scenario_name}")
        context.scenario_start_time = datetime.now()
    except Exception as e:
        print(f"[Environment Hook] Aviso em before_scenario: {e}")


def before_step(context, step):
    """
    Hook executado antes de cada step.
    Corrige problemas de encoding Unicode.
    """
    try:
        # Captura saída original do stdout para evitar problemas de encoding
        import io
        if not hasattr(context, '_original_stdout'):
            context._original_stdout = sys.stdout
            # Cria um wrapper que lida com Unicode
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer,
                encoding='utf-8',
                errors='replace',
                line_buffering=True
            )
    except Exception:
        # Se falhar, continua sem fazer nada
        pass