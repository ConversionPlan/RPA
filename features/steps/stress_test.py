"""
Stress Test Steps para Inbound File Processing
Mede tempo de processamento e volume maximo de arquivos
"""

from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.steps.utils import (
    wait_and_find, wait_and_click, wait_and_send_keys,
    generate_x_length_number, generate_company_prefix, generate_gs1_id,
    generate_gtin_with_cp_id, generate_sgtin_with_gtin, generate_sgln_from_gln,
    generate_gln
)
from features.steps.auth import ends_timer
from datetime import datetime
import time
import os
import json
import uuid
import sys


def log(msg):
    """Print com flush para garantir saida imediata"""
    print(msg)
    sys.stdout.flush()


# =============================================================================
# CLASSE DE METRICAS DO STRESS TEST
# =============================================================================

class StressTestMetrics:
    """Classe para coletar e calcular metricas do stress test"""

    def __init__(self):
        self.test_id = str(uuid.uuid4())[:8]
        self.start_time = None
        self.end_time = None
        self.results = []
        self.errors = []
        self.file_times = []  # Tempo individual por arquivo

    def start_timer(self):
        self.start_time = datetime.now()

    def stop_timer(self):
        self.end_time = datetime.now()

    def record_file_time(self, file_index, duration_seconds, success=True, error_msg=None):
        """Registra o tempo de processamento de um arquivo individual"""
        self.file_times.append({
            "file_index": file_index,
            "duration_seconds": duration_seconds,
            "success": success,
            "error": error_msg,
            "timestamp": datetime.now().isoformat()
        })

    def get_total_duration(self):
        """Retorna duracao total em segundos"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0

    def get_average_time_per_file(self):
        """Retorna tempo medio por arquivo"""
        if self.file_times:
            successful_times = [f["duration_seconds"] for f in self.file_times if f["success"]]
            if successful_times:
                return sum(successful_times) / len(successful_times)
        return 0

    def get_success_rate(self):
        """Retorna taxa de sucesso (0-100)"""
        if self.file_times:
            successful = len([f for f in self.file_times if f["success"]])
            return (successful / len(self.file_times)) * 100
        return 0

    def get_files_per_minute(self):
        """Retorna arquivos processados por minuto"""
        total_duration = self.get_total_duration()
        if total_duration > 0:
            successful = len([f for f in self.file_times if f["success"]])
            return (successful / total_duration) * 60
        return 0

    def add_result(self, test_type, batch_size, metrics_dict):
        """Adiciona resultado de um teste"""
        self.results.append({
            "test_type": test_type,
            "batch_size": batch_size,
            "metrics": metrics_dict,
            "timestamp": datetime.now().isoformat()
        })

    def to_dict(self):
        """Converte metricas para dicionario"""
        return {
            "test_id": self.test_id,
            "total_duration_seconds": self.get_total_duration(),
            "average_time_per_file": self.get_average_time_per_file(),
            "success_rate_percent": self.get_success_rate(),
            "files_per_minute": self.get_files_per_minute(),
            "total_files_processed": len(self.file_times),
            "successful_files": len([f for f in self.file_times if f["success"]]),
            "failed_files": len([f for f in self.file_times if not f["success"]]),
            "file_times": self.file_times,
            "results": self.results,
            "errors": self.errors
        }


# =============================================================================
# STEPS DE INICIALIZACAO
# =============================================================================

@given("Stress test metrics are initialized")
def init_stress_metrics(context):
    """Inicializa o objeto de metricas do stress test"""
    context.stress_metrics = StressTestMetrics()
    context.epcis_files = []
    context.current_batch_size = 0
    print(f"[STRESS TEST] Metricas inicializadas - ID: {context.stress_metrics.test_id}")


@when("Start stress test timer")
def start_timer(context):
    """Inicia o timer do stress test"""
    context.stress_metrics.start_timer()
    print(f"[STRESS TEST] Timer iniciado: {context.stress_metrics.start_time}")


@when("Stop stress test timer")
def stop_timer(context):
    """Para o timer do stress test"""
    context.stress_metrics.stop_timer()
    duration = context.stress_metrics.get_total_duration()
    print(f"[STRESS TEST] Timer parado: {context.stress_metrics.end_time}")
    print(f"[STRESS TEST] Duracao total: {duration:.2f} segundos")


# =============================================================================
# STEPS DE GERACAO DE ARQUIVOS EPCIS
# =============================================================================

@when("Prepare {batch_size:d} EPCIS files for upload")
def prepare_epcis_files(context, batch_size):
    """Gera arquivos EPCIS XML para upload em lote"""
    try:
        context.current_batch_size = batch_size
        context.epcis_files = []

        # Criar diretorio para arquivos de teste
        test_dir = os.path.join(os.getcwd(), "stress_test_files")
        os.makedirs(test_dir, exist_ok=True)

        print(f"[STRESS TEST] Gerando {batch_size} arquivos EPCIS...")

        for i in range(batch_size):
            file_content = generate_epcis_xml_content(i)
            file_path = os.path.join(test_dir, f"epcis_stress_{i+1}.xml")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)

            context.epcis_files.append(file_path)

            if (i + 1) % 10 == 0:
                print(f"[STRESS TEST] {i + 1}/{batch_size} arquivos gerados...")

        print(f"[STRESS TEST] {batch_size} arquivos EPCIS prontos para upload")

    except Exception as e:
        context.stress_metrics.errors.append(f"Erro ao gerar arquivos: {str(e)}")
        ends_timer(context, e)
        raise


def generate_epcis_xml_content(index):
    """Gera conteudo XML EPCIS com dados unicos"""

    # Gerar identificadores unicos
    company_prefix = generate_company_prefix()
    gs1_id = generate_gs1_id()
    gtin = generate_gtin_with_cp_id(company_prefix, gs1_id)

    # Gerar GLN e SGLN para localizacoes
    sender_gln = generate_gln(company_prefix)
    receiver_gln = generate_gln(generate_company_prefix())

    sender_sgln = generate_sgln_from_gln(sender_gln)
    receiver_sgln = generate_sgln_from_gln(receiver_gln)

    # Gerar SGTIN
    sgtin = f"urn:epc:id:sgtin:{generate_sgtin_with_gtin(gtin)}.{generate_x_length_number(10)}"

    # Gerar timestamps
    event_time = datetime.now().isoformat() + "Z"

    # Gerar lote e expiracao
    lot = f"LOT{generate_x_length_number(8)}"
    exp_date = "2030-12-31"

    epcis_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<epcis:EPCISDocument xmlns:epcis="urn:epcglobal:epcis:xsd:1"
    xmlns:cbvmda="urn:epcglobal:cbv:mda"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    schemaVersion="1.2" creationDate="{event_time}">
    <EPCISBody>
        <EventList>
            <ObjectEvent>
                <eventTime>{event_time}</eventTime>
                <eventTimeZoneOffset>-03:00</eventTimeZoneOffset>
                <epcList>
                    <epc>{sgtin}</epc>
                </epcList>
                <action>ADD</action>
                <bizStep>urn:epcglobal:cbv:bizstep:receiving</bizStep>
                <disposition>urn:epcglobal:cbv:disp:in_progress</disposition>
                <readPoint>
                    <id>{receiver_sgln}</id>
                </readPoint>
                <bizLocation>
                    <id>{receiver_sgln}</id>
                </bizLocation>
                <bizTransactionList>
                    <bizTransaction type="urn:epcglobal:cbv:btt:po">PO-STRESS-{index:05d}</bizTransaction>
                </bizTransactionList>
                <extension>
                    <sourceList>
                        <source type="urn:epcglobal:cbv:sdt:owning_party">{sender_sgln}</source>
                    </sourceList>
                    <destinationList>
                        <destination type="urn:epcglobal:cbv:sdt:owning_party">{receiver_sgln}</destination>
                    </destinationList>
                    <ilmd>
                        <cbvmda:lotNumber>{lot}</cbvmda:lotNumber>
                        <cbvmda:itemExpirationDate>{exp_date}</cbvmda:itemExpirationDate>
                    </ilmd>
                </extension>
            </ObjectEvent>
        </EventList>
    </EPCISBody>
</epcis:EPCISDocument>'''

    return epcis_xml


# =============================================================================
# STEPS DE PROCESSAMENTO - MANUAL UPLOAD
# =============================================================================

@when("Process batch of {batch_size:d} files via Manual Upload")
def process_batch_manual_upload(context, batch_size):
    """Processa lote de arquivos via Manual Upload"""
    try:
        log(f"[STRESS TEST] Iniciando processamento de {batch_size} arquivos via Manual Upload...")

        # Navegar para Utilities
        navigate_to_utilities(context)

        for i, file_path in enumerate(context.epcis_files):
            file_start_time = datetime.now()
            success = True
            error_msg = None

            try:
                # Upload do arquivo
                upload_single_file(context, file_path, i + 1, batch_size)

            except Exception as e:
                success = False
                error_msg = str(e)
                context.stress_metrics.errors.append(f"Arquivo {i+1}: {error_msg}")
                log(f"[STRESS TEST] ERRO no arquivo {i+1}: {error_msg[:100]}")

            finally:
                file_duration = (datetime.now() - file_start_time).total_seconds()
                context.stress_metrics.record_file_time(i + 1, file_duration, success, error_msg)

            # Progress update
            avg_time = context.stress_metrics.get_average_time_per_file()
            success_rate = context.stress_metrics.get_success_rate()
            log(f"[STRESS TEST] Progresso: {i+1}/{batch_size} "
                  f"| Tempo medio: {avg_time:.2f}s "
                  f"| Taxa sucesso: {success_rate:.1f}%")

    except Exception as e:
        ends_timer(context, e)
        raise


def close_release_info_modal(context):
    """Fecha o modal de release info se estiver presente - OTIMIZADO"""
    try:
        # Tentar fechar via JavaScript direto (mais rapido)
        context.driver.execute_script("""
            // Fechar botoes de Close/Dismiss
            var closeButtons = document.querySelectorAll(
                'span[class*="Close"], button[class*="close"], .tt_utils_ui_dlg_modal-close'
            );
            closeButtons.forEach(function(btn) {
                if (btn.offsetParent !== null) btn.click();
            });

            // Esconder overlays
            var overlays = document.querySelectorAll(
                '.tt_utils_ui_dlg_modal-overlay, #release_info, [class*="modal-backdrop"]'
            );
            overlays.forEach(function(el) {
                el.style.display = 'none';
            });
        """)
        return True
    except:
        return False


def navigate_to_utilities(context):
    """Navega para a pagina de Utilities - OTIMIZADO"""
    try:
        # Verificar se ja estamos em utilities
        if "/utilities" in context.driver.current_url:
            close_release_info_modal(context)
            return

        # Navegar direto
        context.driver.get("https://qualityportal.qa-test.tracktraceweb.com/utilities/")

        # Aguardar pagina carregar - usar WebDriverWait em vez de sleep fixo
        WebDriverWait(context.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Upload manual')]"))
        )

        # Fechar modal se apareceu
        close_release_info_modal(context)

    except Exception as e:
        log(f"[STRESS TEST] Erro navegar Utilities: {e}")
        raise


def upload_single_file(context, file_path, file_index, total_files):
    """Faz upload de um unico arquivo EPCIS - OTIMIZADO para velocidade"""
    try:
        log(f"[STRESS TEST] Upload arquivo {file_index}/{total_files}")

        # Fechar modais primeiro (rapido)
        close_release_info_modal(context)

        # Seletores para o botao de upload (PT e EN)
        upload_selectors = [
            "//a[contains(., 'Upload manual de arquivo EPCIS')]",
            "//*[contains(text(), 'Upload manual de arquivo EPCIS')]",
            "//a[contains(., 'Manual EPCIS')]"
        ]

        # Clicar em Upload manual de arquivo EPCIS
        for selector in upload_selectors:
            try:
                upload_option = context.driver.find_element(By.XPATH, selector)
                if upload_option.is_displayed():
                    context.driver.execute_script("arguments[0].click();", upload_option)
                    break
            except:
                continue

        # Aguardar modal abrir com WebDriverWait - OTIMIZADO
        file_input = None
        try:
            # Usar WebDriverWait em vez de loop com sleep
            file_input = WebDriverWait(context.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
        except:
            # Fallback: tentar encontrar diretamente
            try:
                file_input = context.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            except:
                raise Exception(f"[FALHA] Input file nao encontrado")

        # Enviar arquivo - SEM sleep adicional
        file_input.send_keys(file_path)

        # Aguardar botao OK ficar disponivel e clicar
        ok_selectors = [
            ".tt_utils_ui_dlg_modal-default-enabled-button",
            "[class*='tt_utils_ui_dlg_modal-button']"
        ]

        ok_clicked = False
        for selector in ok_selectors:
            try:
                ok_btn = WebDriverWait(context.driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                context.driver.execute_script("arguments[0].click();", ok_btn)
                ok_clicked = True
                break
            except:
                continue

        if not ok_clicked:
            # Tentar via JavaScript direto
            context.driver.execute_script("""
                var okBtn = document.querySelector('.tt_utils_ui_dlg_modal-default-enabled-button');
                if (okBtn) okBtn.click();
            """)

        # Aguardar processamento - REDUZIDO de 5s para 2s
        time.sleep(2)

        # Verificar erro rapidamente
        try:
            error_el = context.driver.find_element(By.CSS_SELECTOR, ".error, .alert-danger")
            if error_el.is_displayed() and error_el.text:
                raise Exception(f"Erro: {error_el.text[:50]}")
        except:
            pass

        # Fechar modal de resultado
        close_release_info_modal(context)

        log(f"[STRESS TEST] Arquivo {file_index} OK")

    except Exception as e:
        log(f"[STRESS TEST] ERRO arquivo {file_index}: {e}")
        raise


# =============================================================================
# STEPS DE PROCESSAMENTO - ELECTRONIC FILE
# =============================================================================

@when("Generate and process {batch_size:d} electronic files")
def generate_and_process_electronic_files(context, batch_size):
    """Gera e processa arquivos via EPCIS Generator"""
    try:
        context.current_batch_size = batch_size
        print(f"[STRESS TEST] Iniciando geracao de {batch_size} electronic files...")

        for i in range(batch_size):
            file_start_time = datetime.now()
            success = True
            error_msg = None

            try:
                # Gerar e processar um arquivo via EPCIS Generator
                generate_single_electronic_file(context, i + 1, batch_size)

            except Exception as e:
                success = False
                error_msg = str(e)
                context.stress_metrics.errors.append(f"Electronic file {i+1}: {error_msg}")
                print(f"[STRESS TEST] ERRO no electronic file {i+1}: {error_msg[:100]}")

            finally:
                file_duration = (datetime.now() - file_start_time).total_seconds()
                context.stress_metrics.record_file_time(i + 1, file_duration, success, error_msg)

            # Progress update
            if (i + 1) % 5 == 0 or i == batch_size - 1:
                avg_time = context.stress_metrics.get_average_time_per_file()
                success_rate = context.stress_metrics.get_success_rate()
                print(f"[STRESS TEST] Progresso: {i+1}/{batch_size} "
                      f"| Tempo medio: {avg_time:.2f}s "
                      f"| Taxa sucesso: {success_rate:.1f}%")

    except Exception as e:
        ends_timer(context, e)
        raise


def generate_single_electronic_file(context, file_index, total_files):
    """Gera um unico arquivo via EPCIS Generator e processa"""
    try:
        # Abrir nova aba
        context.driver.execute_script("window.open('');")
        context.driver.switch_to.window(context.driver.window_handles[-1])

        # Abrir EPCIS Generator
        context.driver.get("https://epcis-file-generator.tracktracenetwork.com/")
        time.sleep(3)

        # Clicar em Generate Random Data
        wait_and_click(context.driver, By.XPATH, "//p[text()='Generate Random Data']", timeout=15)
        time.sleep(2)

        # Clicar em Submit para gerar
        wait_and_click(context.driver, By.XPATH, "//p[text()='Submit']", timeout=10)
        time.sleep(2)

        # Download do arquivo EPCIS
        wait_and_click(context.driver, By.XPATH, "//p[text()='Download EPCIS file']", timeout=10)
        time.sleep(3)

        # Fechar a aba
        context.driver.close()
        context.driver.switch_to.window(context.driver.window_handles[0])

        # Agora fazer upload do arquivo baixado
        # Encontrar o arquivo mais recente na pasta de downloads
        download_dir = os.getcwd()
        epcis_files = [f for f in os.listdir(download_dir) if f.endswith('.xml') and 'epcis' in f.lower()]

        if epcis_files:
            # Ordenar por data de modificacao
            epcis_files.sort(key=lambda x: os.path.getmtime(os.path.join(download_dir, x)), reverse=True)
            latest_file = os.path.join(download_dir, epcis_files[0])

            # Navegar para utilities e fazer upload
            navigate_to_utilities(context)
            upload_single_file(context, latest_file, file_index, total_files)

            # Limpar arquivo apos upload
            try:
                os.remove(latest_file)
            except:
                pass
        else:
            raise Exception("Arquivo EPCIS nao foi baixado")

        print(f"[STRESS TEST] Electronic file {file_index}/{total_files} processado com sucesso")

    except Exception as e:
        # Garantir que voltamos para a aba principal
        try:
            if len(context.driver.window_handles) > 1:
                context.driver.close()
                context.driver.switch_to.window(context.driver.window_handles[0])
        except:
            pass
        raise


# =============================================================================
# STEPS DE LIMITE DO SISTEMA
# =============================================================================

@when("Find system limit for {test_type} starting from {start_size:d} files")
def find_system_limit(context, test_type, start_size):
    """Descobre o limite maximo de arquivos que o sistema suporta"""
    try:
        current_size = start_size
        max_successful_size = 0
        consecutive_failures = 0
        max_consecutive_failures = 3

        print(f"[STRESS TEST] Buscando limite do sistema para {test_type}...")
        print(f"[STRESS TEST] Iniciando com {start_size} arquivos...")

        while consecutive_failures < max_consecutive_failures:
            context.stress_metrics = StressTestMetrics()  # Reset metricas
            batch_success = True

            try:
                if test_type == "Manual Upload":
                    prepare_epcis_files(context, current_size)
                    context.stress_metrics.start_timer()
                    process_batch_manual_upload(context, current_size)
                    context.stress_metrics.stop_timer()
                else:
                    context.stress_metrics.start_timer()
                    generate_and_process_electronic_files(context, current_size)
                    context.stress_metrics.stop_timer()

                # Verificar taxa de sucesso
                success_rate = context.stress_metrics.get_success_rate()

                if success_rate >= 90:  # 90% de sucesso minimo
                    print(f"[STRESS TEST] Batch de {current_size} arquivos: SUCESSO ({success_rate:.1f}%)")
                    max_successful_size = current_size
                    consecutive_failures = 0

                    # Aumentar tamanho progressivamente
                    if current_size < 50:
                        current_size += 10
                    elif current_size < 100:
                        current_size += 25
                    else:
                        current_size += 50
                else:
                    print(f"[STRESS TEST] Batch de {current_size} arquivos: PARCIAL ({success_rate:.1f}%)")
                    consecutive_failures += 1

            except Exception as e:
                print(f"[STRESS TEST] Batch de {current_size} arquivos: FALHA - {str(e)[:100]}")
                consecutive_failures += 1
                batch_success = False

            # Aguardar entre tentativas
            time.sleep(5)

        context.system_limit = max_successful_size
        context.limit_test_type = test_type
        print(f"[STRESS TEST] Limite encontrado para {test_type}: {max_successful_size} arquivos")

    except Exception as e:
        ends_timer(context, e)
        raise


# =============================================================================
# STEPS DE RELATORIO
# =============================================================================

@then("Record stress test metrics for \"{test_type}\" with {batch_size:d} files")
def record_metrics(context, test_type, batch_size):
    """Registra as metricas do teste"""
    metrics = {
        "total_duration": context.stress_metrics.get_total_duration(),
        "average_time_per_file": context.stress_metrics.get_average_time_per_file(),
        "success_rate": context.stress_metrics.get_success_rate(),
        "files_per_minute": context.stress_metrics.get_files_per_minute(),
        "total_processed": len(context.stress_metrics.file_times),
        "successful": len([f for f in context.stress_metrics.file_times if f["success"]]),
        "failed": len([f for f in context.stress_metrics.file_times if not f["success"]])
    }

    context.stress_metrics.add_result(test_type, batch_size, metrics)

    print("\n" + "=" * 60)
    print(f"[STRESS TEST] METRICAS - {test_type} ({batch_size} arquivos)")
    print("=" * 60)
    print(f"  Duracao total:        {metrics['total_duration']:.2f} segundos")
    print(f"  Tempo medio/arquivo:  {metrics['average_time_per_file']:.2f} segundos")
    print(f"  Taxa de sucesso:      {metrics['success_rate']:.1f}%")
    print(f"  Arquivos/minuto:      {metrics['files_per_minute']:.2f}")
    print(f"  Total processados:    {metrics['total_processed']}")
    print(f"  Sucesso:              {metrics['successful']}")
    print(f"  Falhas:               {metrics['failed']}")
    print("=" * 60 + "\n")


@then("Generate stress test report")
def generate_report(context):
    """Gera relatorio do stress test em JSON, TXT e PDF profissional"""
    try:
        # Criar diretorio de relatorios
        report_dir = os.path.join(os.getcwd(), "report", "stress_test")
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Relatorio JSON
        json_report = context.stress_metrics.to_dict()
        json_path = os.path.join(report_dir, f"stress_test_{timestamp}.json")

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)

        # Relatorio TXT
        txt_path = os.path.join(report_dir, f"stress_test_{timestamp}.txt")

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RELATORIO DE STRESS TEST - INBOUND FILE PROCESSING\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"ID do Teste:     {json_report['test_id']}\n")
            f.write(f"Data/Hora:       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n")
            f.write("-" * 70 + "\n")
            f.write("RESUMO\n")
            f.write("-" * 70 + "\n")
            f.write(f"Duracao Total:           {json_report['total_duration_seconds']:.2f} segundos\n")
            f.write(f"Tempo Medio/Arquivo:     {json_report['average_time_per_file']:.2f} segundos\n")
            f.write(f"Taxa de Sucesso:         {json_report['success_rate_percent']:.1f}%\n")
            f.write(f"Arquivos/Minuto:         {json_report['files_per_minute']:.2f}\n")
            f.write(f"Total Processados:       {json_report['total_files_processed']}\n")
            f.write(f"Arquivos com Sucesso:    {json_report['successful_files']}\n")
            f.write(f"Arquivos com Falha:      {json_report['failed_files']}\n")
            f.write("\n")

            if json_report['results']:
                f.write("-" * 70 + "\n")
                f.write("RESULTADOS POR TESTE\n")
                f.write("-" * 70 + "\n")
                for result in json_report['results']:
                    f.write(f"\n{result['test_type']} ({result['batch_size']} arquivos):\n")
                    m = result['metrics']
                    f.write(f"  - Duracao: {m['total_duration']:.2f}s\n")
                    f.write(f"  - Media/arquivo: {m['average_time_per_file']:.2f}s\n")
                    f.write(f"  - Taxa sucesso: {m['success_rate']:.1f}%\n")

            if json_report['errors']:
                f.write("\n")
                f.write("-" * 70 + "\n")
                f.write("ERROS ENCONTRADOS\n")
                f.write("-" * 70 + "\n")
                for error in json_report['errors']:
                    f.write(f"  - {error}\n")

            f.write("\n" + "=" * 70 + "\n")
            f.write("FIM DO RELATORIO\n")
            f.write("=" * 70 + "\n")

        print(f"[STRESS TEST] Relatorio JSON salvo em: {json_path}")
        print(f"[STRESS TEST] Relatorio TXT salvo em: {txt_path}")

        # Gerar relatorio PDF profissional com graficos
        try:
            from report.stress_report_pdf import generate_pdf_report
            pdf_path = generate_pdf_report(json_report, report_dir)
            print(f"[STRESS TEST] Relatorio PDF salvo em: {pdf_path}")
        except Exception as pdf_error:
            print(f"[STRESS TEST] Aviso: Nao foi possivel gerar PDF: {pdf_error}")

    except Exception as e:
        print(f"[STRESS TEST] Erro ao gerar relatorio: {e}")


@then("Generate comparative stress test report")
def generate_comparative_report(context):
    """Gera relatorio comparativo entre metodos"""
    try:
        report_dir = os.path.join(os.getcwd(), "report", "stress_test")
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_path = os.path.join(report_dir, f"stress_test_comparison_{timestamp}.txt")

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RELATORIO COMPARATIVO - MANUAL UPLOAD vs ELECTRONIC FILE\n")
            f.write("=" * 70 + "\n\n")

            results = context.stress_metrics.results

            if len(results) >= 2:
                manual = next((r for r in results if "Manual" in r['test_type']), None)
                electronic = next((r for r in results if "Electronic" in r['test_type']), None)

                if manual and electronic:
                    f.write("-" * 70 + "\n")
                    f.write("COMPARACAO\n")
                    f.write("-" * 70 + "\n\n")

                    f.write(f"{'Metrica':<30} {'Manual Upload':<20} {'Electronic File':<20}\n")
                    f.write("-" * 70 + "\n")

                    mm = manual['metrics']
                    em = electronic['metrics']

                    f.write(f"{'Duracao Total (s)':<30} {mm['total_duration']:<20.2f} {em['total_duration']:<20.2f}\n")
                    f.write(f"{'Tempo Medio/Arquivo (s)':<30} {mm['average_time_per_file']:<20.2f} {em['average_time_per_file']:<20.2f}\n")
                    f.write(f"{'Taxa de Sucesso (%)':<30} {mm['success_rate']:<20.1f} {em['success_rate']:<20.1f}\n")
                    f.write(f"{'Arquivos/Minuto':<30} {mm['files_per_minute']:<20.2f} {em['files_per_minute']:<20.2f}\n")

                    f.write("\n")
                    f.write("-" * 70 + "\n")
                    f.write("CONCLUSAO\n")
                    f.write("-" * 70 + "\n")

                    # Determinar qual metodo e mais rapido
                    if mm['average_time_per_file'] < em['average_time_per_file']:
                        faster = "Manual Upload"
                        diff = ((em['average_time_per_file'] - mm['average_time_per_file']) / em['average_time_per_file']) * 100
                    else:
                        faster = "Electronic File"
                        diff = ((mm['average_time_per_file'] - em['average_time_per_file']) / mm['average_time_per_file']) * 100

                    f.write(f"\nMetodo mais rapido: {faster} ({diff:.1f}% mais rapido)\n")

            f.write("\n" + "=" * 70 + "\n")

        print(f"[STRESS TEST] Relatorio comparativo salvo em: {txt_path}")

        # Tambem gerar relatorio padrao
        generate_report(context)

    except Exception as e:
        print(f"[STRESS TEST] Erro ao gerar relatorio comparativo: {e}")


@then("Generate system limit report for \"{test_type}\"")
def generate_limit_report(context, test_type):
    """Gera relatorio do teste de limite do sistema"""
    try:
        report_dir = os.path.join(os.getcwd(), "report", "stress_test")
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_path = os.path.join(report_dir, f"system_limit_{test_type.lower().replace(' ', '_')}_{timestamp}.txt")

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"RELATORIO DE LIMITE DO SISTEMA - {test_type.upper()}\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"Data/Hora:              {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Tipo de Teste:          {test_type}\n")
            f.write(f"Limite Encontrado:      {getattr(context, 'system_limit', 'N/A')} arquivos\n")
            f.write("\n")
            f.write("-" * 70 + "\n")
            f.write("INTERPRETACAO\n")
            f.write("-" * 70 + "\n")

            limit = getattr(context, 'system_limit', 0)

            if limit >= 100:
                f.write("EXCELENTE: O sistema suporta mais de 100 arquivos por lote.\n")
            elif limit >= 50:
                f.write("BOM: O sistema suporta entre 50-100 arquivos por lote.\n")
            elif limit >= 25:
                f.write("REGULAR: O sistema suporta entre 25-50 arquivos por lote.\n")
            else:
                f.write("ATENCAO: O sistema suporta menos de 25 arquivos por lote.\n")
                f.write("Considere investigar possiveis gargalos de performance.\n")

            f.write("\n" + "=" * 70 + "\n")

        print(f"[STRESS TEST] Relatorio de limite salvo em: {txt_path}")

    except Exception as e:
        print(f"[STRESS TEST] Erro ao gerar relatorio de limite: {e}")


# =============================================================================
# PROCESSAMENTO PARALELO - MULTIPLAS SESSOES
# =============================================================================

from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import threading

# Lock para sincronizar acesso às métricas
_metrics_lock = Lock()


def create_parallel_browser_session(session_id, headless_mode=True):
    """Cria uma nova sessão de browser para processamento paralelo"""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    import tempfile

    options = Options()

    if headless_mode:
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-software-rasterizer")

    # Diretório temporário único para cada sessão
    temp_dir = tempfile.mkdtemp(prefix=f"chrome_parallel_{session_id}_")
    options.add_argument(f"--user-data-dir={temp_dir}")

    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--lang=en-US")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-setuid-sandbox")

    prefs = {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "profile.default_content_setting_values.notifications": 2,
        "credentials_enable_service": False,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    driver.implicitly_wait(10)

    return driver, temp_dir


def login_parallel_session(driver, session_id):
    """Faz login em uma sessão paralela"""
    try:
        driver.get("https://qualityportal.qa-test.tracktraceweb.com/auth")

        # Aguardar formulário
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "auth__login_form__username"))
        )

        # Username
        driver.find_element(By.ID, "auth__login_form__username").send_keys("teste@teste.com")
        driver.find_element(By.ID, "auth__login_form__step1_next_btn").click()

        # Password
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "auth__login_form__password"))
        )
        driver.find_element(By.ID, "auth__login_form__password").send_keys("Mudar@12345342")
        driver.find_element(By.ID, "auth__login_form__step2_next_btn").click()

        # Aguardar redirect
        WebDriverWait(driver, 15).until(
            lambda d: "/auth" not in d.current_url
        )

        # Fechar modal se aparecer
        try:
            close_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Close']"))
            )
            close_btn.click()
        except:
            pass

        log(f"[PARALLEL] Sessao {session_id} logada com sucesso")
        return True

    except Exception as e:
        log(f"[PARALLEL] ERRO login sessao {session_id}: {e}")
        return False


def process_files_in_session(session_id, driver, files, metrics, total_files):
    """Processa uma lista de arquivos em uma sessão específica"""
    session_results = []

    try:
        # Navegar para utilities
        driver.get("https://qualityportal.qa-test.tracktraceweb.com/utilities/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Upload manual')]"))
        )

        # Fechar modal se aparecer
        try:
            driver.execute_script("""
                var closeButtons = document.querySelectorAll('span[class*="Close"], .tt_utils_ui_dlg_modal-close');
                closeButtons.forEach(function(btn) { if (btn.offsetParent !== null) btn.click(); });
            """)
        except:
            pass

        for i, file_path in enumerate(files):
            file_start_time = datetime.now()
            success = True
            error_msg = None

            try:
                # Upload do arquivo
                upload_file_parallel(driver, file_path, session_id, i + 1, len(files))

            except Exception as e:
                success = False
                error_msg = str(e)
                log(f"[PARALLEL S{session_id}] ERRO arquivo {i+1}: {error_msg[:50]}")

            finally:
                file_duration = (datetime.now() - file_start_time).total_seconds()

                # Registrar métricas de forma thread-safe
                with _metrics_lock:
                    metrics.record_file_time(
                        f"S{session_id}-{i+1}",
                        file_duration,
                        success,
                        error_msg
                    )

                session_results.append({
                    "session": session_id,
                    "file_index": i + 1,
                    "duration": file_duration,
                    "success": success
                })

                # Log de progresso
                processed = len(metrics.file_times)
                log(f"[PARALLEL] Total: {processed}/{total_files} | S{session_id}: {i+1}/{len(files)} | {file_duration:.1f}s")

    except Exception as e:
        log(f"[PARALLEL] ERRO na sessao {session_id}: {e}")

    return session_results


def upload_file_parallel(driver, file_path, session_id, file_index, total_in_session):
    """Upload de arquivo em sessão paralela"""
    try:
        # Fechar modais
        try:
            driver.execute_script("""
                var overlays = document.querySelectorAll('.tt_utils_ui_dlg_modal-overlay');
                overlays.forEach(function(el) { el.style.display = 'none'; });
            """)
        except:
            pass

        # Clicar em Upload manual de arquivo EPCIS
        upload_selectors = [
            "//a[contains(., 'Upload manual de arquivo EPCIS')]",
            "//*[contains(text(), 'Upload manual de arquivo EPCIS')]",
        ]

        for selector in upload_selectors:
            try:
                el = driver.find_element(By.XPATH, selector)
                if el.is_displayed():
                    driver.execute_script("arguments[0].click();", el)
                    break
            except:
                continue

        # Aguardar input file
        file_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )

        # Enviar arquivo
        file_input.send_keys(file_path)

        # Clicar OK
        ok_btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".tt_utils_ui_dlg_modal-default-enabled-button"))
        )
        driver.execute_script("arguments[0].click();", ok_btn)

        # Aguardar processamento
        time.sleep(2)

        # Fechar modal de resultado
        try:
            driver.execute_script("""
                var closeButtons = document.querySelectorAll('span[class*="Close"], .tt_utils_ui_dlg_modal-close');
                closeButtons.forEach(function(btn) { if (btn.offsetParent !== null) btn.click(); });
                var overlays = document.querySelectorAll('.tt_utils_ui_dlg_modal-overlay');
                overlays.forEach(function(el) { el.style.display = 'none'; });
            """)
        except:
            pass

    except Exception as e:
        raise Exception(f"Upload falhou: {e}")


@when("Process {total_files:d} files in parallel with {num_sessions:d} sessions")
def process_files_parallel(context, total_files, num_sessions):
    """Processa arquivos em paralelo usando múltiplas sessões de browser"""
    try:
        log(f"\n{'='*60}")
        log(f"[PARALLEL] INICIANDO STRESS TEST PARALELO")
        log(f"[PARALLEL] Total de arquivos: {total_files}")
        log(f"[PARALLEL] Sessoes paralelas: {num_sessions}")
        log(f"[PARALLEL] Arquivos por sessao: {total_files // num_sessions}")
        log(f"{'='*60}\n")

        # Verificar se temos arquivos suficientes
        if len(context.epcis_files) < total_files:
            raise Exception(f"Apenas {len(context.epcis_files)} arquivos disponiveis, necessario {total_files}")

        # Dividir arquivos entre sessões
        files_per_session = total_files // num_sessions
        file_batches = []
        for i in range(num_sessions):
            start_idx = i * files_per_session
            end_idx = start_idx + files_per_session
            if i == num_sessions - 1:  # Última sessão pega arquivos restantes
                end_idx = total_files
            file_batches.append(context.epcis_files[start_idx:end_idx])

        headless_mode = os.environ.get("HEADLESS", "True").lower() == "true"

        # Criar sessões em paralelo
        log("[PARALLEL] Criando sessoes de browser...")
        sessions = []
        temp_dirs = []

        for i in range(num_sessions):
            driver, temp_dir = create_parallel_browser_session(i + 1, headless_mode)
            sessions.append((i + 1, driver))
            temp_dirs.append(temp_dir)
            log(f"[PARALLEL] Sessao {i + 1} criada")

        # Login em todas as sessões
        log("[PARALLEL] Fazendo login nas sessoes...")
        for session_id, driver in sessions:
            if not login_parallel_session(driver, session_id):
                raise Exception(f"Falha no login da sessao {session_id}")

        log("[PARALLEL] Todas as sessoes logadas! Iniciando processamento paralelo...\n")

        # Processar em paralelo usando ThreadPoolExecutor
        all_results = []

        with ThreadPoolExecutor(max_workers=num_sessions) as executor:
            futures = []
            for (session_id, driver), files in zip(sessions, file_batches):
                future = executor.submit(
                    process_files_in_session,
                    session_id,
                    driver,
                    files,
                    context.stress_metrics,
                    total_files
                )
                futures.append(future)

            # Coletar resultados
            for future in as_completed(futures):
                try:
                    results = future.result()
                    all_results.extend(results)
                except Exception as e:
                    log(f"[PARALLEL] ERRO em thread: {e}")

        # Fechar todas as sessões
        log("\n[PARALLEL] Fechando sessoes...")
        for session_id, driver in sessions:
            try:
                driver.quit()
            except:
                pass

        # Limpar diretórios temporários
        import shutil
        for temp_dir in temp_dirs:
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

        # Estatísticas finais
        successful = len([r for r in all_results if r["success"]])
        failed = len([r for r in all_results if not r["success"]])

        log(f"\n{'='*60}")
        log(f"[PARALLEL] PROCESSAMENTO PARALELO CONCLUIDO")
        log(f"[PARALLEL] Arquivos processados: {len(all_results)}")
        log(f"[PARALLEL] Sucesso: {successful}")
        log(f"[PARALLEL] Falhas: {failed}")
        log(f"{'='*60}\n")

    except Exception as e:
        log(f"[PARALLEL] ERRO FATAL: {e}")
        # Cleanup em caso de erro
        if 'sessions' in locals():
            for _, driver in sessions:
                try:
                    driver.quit()
                except:
                    pass
        raise


# =============================================================================
# LIMPEZA
# =============================================================================

def cleanup_stress_test_files():
    """Remove arquivos temporarios do stress test"""
    try:
        test_dir = os.path.join(os.getcwd(), "stress_test_files")
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir)
            print("[STRESS TEST] Arquivos temporarios removidos")
    except Exception as e:
        print(f"[STRESS TEST] Erro ao limpar arquivos: {e}")
