"""
Gerador de Relatorios PDF Profissionais para Stress Test
Inclui graficos, metricas e analises detalhadas
"""

import os
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Usar matplotlib para graficos mais bonitos
import matplotlib
matplotlib.use('Agg')  # Backend sem GUI
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class StressTestPDFReport:
    """Gerador de relatorios PDF profissionais para stress test"""

    # Cores do tema
    PRIMARY_COLOR = colors.HexColor('#1a5276')
    SECONDARY_COLOR = colors.HexColor('#2980b9')
    SUCCESS_COLOR = colors.HexColor('#27ae60')
    WARNING_COLOR = colors.HexColor('#f39c12')
    DANGER_COLOR = colors.HexColor('#e74c3c')
    LIGHT_GRAY = colors.HexColor('#ecf0f1')
    DARK_GRAY = colors.HexColor('#2c3e50')

    def __init__(self, metrics_data: dict, output_dir: str = None):
        """
        Inicializa o gerador de relatorios

        Args:
            metrics_data: Dicionario com metricas do stress test
            output_dir: Diretorio de saida (opcional)
        """
        self.data = metrics_data
        self.output_dir = output_dir or os.path.join(os.getcwd(), "report", "stress_test")
        os.makedirs(self.output_dir, exist_ok=True)

        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configura estilos customizados"""
        # Titulo principal
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.PRIMARY_COLOR,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica-Bold'
        ))

        # Subtitulo
        self.styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.SECONDARY_COLOR,
            alignment=TA_CENTER,
            spaceAfter=30
        ))

        # Secao
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.PRIMARY_COLOR,
            spaceBefore=20,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))

        # Metrica grande
        self.styles.add(ParagraphStyle(
            name='BigMetric',
            fontSize=36,
            textColor=self.PRIMARY_COLOR,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Label metrica
        self.styles.add(ParagraphStyle(
            name='MetricLabel',
            fontSize=10,
            textColor=self.DARK_GRAY,
            alignment=TA_CENTER
        ))

        # Texto normal centralizado
        self.styles.add(ParagraphStyle(
            name='CenterText',
            parent=self.styles['Normal'],
            alignment=TA_CENTER
        ))

    def generate(self) -> str:
        """
        Gera o relatorio PDF completo

        Returns:
            Caminho do arquivo PDF gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = os.path.join(self.output_dir, f"stress_test_report_{timestamp}.pdf")

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
            title="Stress Test Report - Inbound File Processing",
            author="RPA Track Trace RX"
        )

        # Construir elementos do documento
        elements = []

        # Capa
        elements.extend(self._build_cover())

        # Resumo executivo
        elements.extend(self._build_executive_summary())

        # Metricas principais com graficos
        elements.extend(self._build_metrics_section())

        # Grafico de tempo por arquivo
        elements.extend(self._build_time_chart())

        # Tabela detalhada
        elements.extend(self._build_detailed_table())

        # Analise e recomendacoes
        elements.extend(self._build_analysis())

        # Rodape
        elements.extend(self._build_footer())

        # Gerar PDF
        doc.build(elements)

        print(f"[PDF] Relatorio gerado: {pdf_path}")
        return pdf_path

    def _build_cover(self) -> list:
        """Constroi a capa do relatorio"""
        elements = []

        # Espacamento superior
        elements.append(Spacer(1, 2*inch))

        # Logo/Header decorativo
        header_drawing = Drawing(400, 60)
        header_drawing.add(Rect(0, 20, 400, 40, fillColor=self.PRIMARY_COLOR, strokeColor=None))
        header_drawing.add(String(200, 35, "STRESS TEST REPORT", fontSize=20,
                                  fillColor=colors.white, textAnchor='middle',
                                  fontName='Helvetica-Bold'))
        elements.append(header_drawing)

        elements.append(Spacer(1, 0.5*inch))

        # Titulo
        elements.append(Paragraph("Inbound File Processing", self.styles['MainTitle']))

        # Subtitulo
        elements.append(Paragraph(
            f"Relatorio de Performance e Capacidade",
            self.styles['SubTitle']
        ))

        elements.append(Spacer(1, 1*inch))

        # Info box
        info_data = [
            ['ID do Teste:', self.data.get('test_id', 'N/A')],
            ['Data/Hora:', datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
            ['Ambiente:', 'QA Portal - Track Trace RX'],
            ['Tipo de Teste:', self._get_test_type()],
        ]

        info_table = Table(info_data, colWidths=[2.5*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), self.PRIMARY_COLOR),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(info_table)

        elements.append(PageBreak())
        return elements

    def _build_executive_summary(self) -> list:
        """Constroi o resumo executivo com KPIs principais"""
        elements = []

        elements.append(Paragraph("Resumo Executivo", self.styles['SectionTitle']))
        elements.append(HRFlowable(width="100%", thickness=2, color=self.PRIMARY_COLOR))
        elements.append(Spacer(1, 0.3*inch))

        # KPIs em cards
        success_rate = self.data.get('success_rate_percent', 0)
        avg_time = self.data.get('average_time_per_file', 0)
        files_per_min = self.data.get('files_per_minute', 0)
        total_files = self.data.get('total_files_processed', 0)

        # Determinar cor do status
        if success_rate >= 95:
            status_color = self.SUCCESS_COLOR
            status_text = "EXCELENTE"
        elif success_rate >= 80:
            status_color = self.WARNING_COLOR
            status_text = "BOM"
        else:
            status_color = self.DANGER_COLOR
            status_text = "ATENCAO"

        # Cards de metricas
        kpi_data = [
            [
                self._create_kpi_cell(f"{success_rate:.1f}%", "Taxa de Sucesso", status_color),
                self._create_kpi_cell(f"{avg_time:.1f}s", "Tempo Medio/Arquivo", self.SECONDARY_COLOR),
                self._create_kpi_cell(f"{files_per_min:.2f}", "Arquivos/Minuto", self.SECONDARY_COLOR),
                self._create_kpi_cell(str(total_files), "Total Processados", self.SECONDARY_COLOR),
            ]
        ]

        kpi_table = Table(kpi_data, colWidths=[1.8*inch]*4)
        kpi_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (0, 0), 1, status_color),
            ('BOX', (1, 0), (1, 0), 1, self.LIGHT_GRAY),
            ('BOX', (2, 0), (2, 0), 1, self.LIGHT_GRAY),
            ('BOX', (3, 0), (3, 0), 1, self.LIGHT_GRAY),
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#e8f6f3')),
        ]))
        elements.append(kpi_table)

        elements.append(Spacer(1, 0.3*inch))

        # Status geral
        status_paragraph = Paragraph(
            f"<b>Status Geral:</b> <font color='{status_color}'>{status_text}</font>",
            self.styles['Normal']
        )
        elements.append(status_paragraph)

        # Resumo em texto
        duration = self.data.get('total_duration_seconds', 0)
        successful = self.data.get('successful_files', 0)
        failed = self.data.get('failed_files', 0)

        summary_text = f"""
        O teste de stress processou <b>{total_files} arquivos</b> em <b>{duration:.1f} segundos</b>
        ({duration/60:.1f} minutos). A taxa de sucesso foi de <b>{success_rate:.1f}%</b>,
        com <b>{successful} arquivos processados com sucesso</b> e <b>{failed} falhas</b>.
        O tempo medio por arquivo foi de <b>{avg_time:.1f} segundos</b>, resultando em uma
        capacidade de processamento de <b>{files_per_min:.2f} arquivos por minuto</b>.
        """
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(summary_text, self.styles['Normal']))

        elements.append(Spacer(1, 0.5*inch))
        return elements

    def _create_kpi_cell(self, value: str, label: str, color) -> list:
        """Cria uma celula de KPI formatada"""
        return [
            Paragraph(f"<font color='{color}' size='24'><b>{value}</b></font>",
                     self.styles['CenterText']),
            Paragraph(f"<font size='9'>{label}</font>", self.styles['CenterText'])
        ]

    def _build_metrics_section(self) -> list:
        """Constroi secao de metricas com grafico de pizza"""
        elements = []

        elements.append(Paragraph("Distribuicao de Resultados", self.styles['SectionTitle']))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.LIGHT_GRAY))
        elements.append(Spacer(1, 0.3*inch))

        # Criar grafico de pizza com matplotlib
        successful = self.data.get('successful_files', 0)
        failed = self.data.get('failed_files', 0)

        if successful + failed > 0:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

            # Grafico de pizza
            sizes = [successful, failed] if failed > 0 else [successful]
            labels = ['Sucesso', 'Falha'] if failed > 0 else ['Sucesso']
            colors_pie = ['#27ae60', '#e74c3c'] if failed > 0 else ['#27ae60']
            explode = (0.05, 0.05) if failed > 0 else (0,)

            ax1.pie(sizes, explode=explode, labels=labels, colors=colors_pie,
                   autopct='%1.1f%%', shadow=True, startangle=90)
            ax1.set_title('Taxa de Sucesso/Falha', fontsize=12, fontweight='bold')

            # Grafico de barras - tempo por arquivo
            file_times = self.data.get('file_times', [])
            if file_times:
                indices = [f"Arq {ft['file_index']}" for ft in file_times]
                times = [ft['duration_seconds'] for ft in file_times]
                bar_colors = ['#27ae60' if ft['success'] else '#e74c3c' for ft in file_times]

                ax2.bar(indices, times, color=bar_colors)
                ax2.set_xlabel('Arquivo')
                ax2.set_ylabel('Tempo (segundos)')
                ax2.set_title('Tempo de Processamento por Arquivo', fontsize=12, fontweight='bold')
                ax2.tick_params(axis='x', rotation=45)

                # Linha media
                avg_time = sum(times) / len(times)
                ax2.axhline(y=avg_time, color='#3498db', linestyle='--', label=f'Media: {avg_time:.1f}s')
                ax2.legend()

            plt.tight_layout()

            # Salvar em buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()

            # Adicionar imagem ao PDF
            img = Image(img_buffer, width=7*inch, height=3*inch)
            elements.append(img)

        elements.append(Spacer(1, 0.3*inch))
        return elements

    def _build_time_chart(self) -> list:
        """Constroi grafico de linha do tempo de processamento"""
        elements = []

        file_times = self.data.get('file_times', [])
        if len(file_times) > 1:
            elements.append(Paragraph("Evolucao do Tempo de Processamento", self.styles['SectionTitle']))
            elements.append(HRFlowable(width="100%", thickness=1, color=self.LIGHT_GRAY))
            elements.append(Spacer(1, 0.3*inch))

            fig, ax = plt.subplots(figsize=(10, 4))

            indices = list(range(1, len(file_times) + 1))
            times = [ft['duration_seconds'] for ft in file_times]

            # Linha principal
            ax.plot(indices, times, 'b-o', linewidth=2, markersize=8, label='Tempo de Processamento')

            # Area sob a curva
            ax.fill_between(indices, times, alpha=0.3)

            # Media movel (se tiver dados suficientes)
            if len(times) >= 3:
                window = min(3, len(times))
                moving_avg = []
                for i in range(len(times)):
                    start = max(0, i - window + 1)
                    moving_avg.append(sum(times[start:i+1]) / (i - start + 1))
                ax.plot(indices, moving_avg, 'r--', linewidth=1.5, label='Media Movel')

            ax.set_xlabel('Numero do Arquivo')
            ax.set_ylabel('Tempo (segundos)')
            ax.set_title('Tempo de Processamento ao Longo do Teste', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)

            plt.tight_layout()

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()

            img = Image(img_buffer, width=7*inch, height=3*inch)
            elements.append(img)

            elements.append(Spacer(1, 0.3*inch))

        return elements

    def _build_detailed_table(self) -> list:
        """Constroi tabela detalhada de resultados"""
        elements = []

        elements.append(Paragraph("Detalhamento por Arquivo", self.styles['SectionTitle']))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.LIGHT_GRAY))
        elements.append(Spacer(1, 0.2*inch))

        file_times = self.data.get('file_times', [])

        if file_times:
            # Cabecalho
            table_data = [['#', 'Tempo (s)', 'Status', 'Timestamp', 'Observacao']]

            for ft in file_times:
                status = 'OK' if ft['success'] else 'FALHA'
                status_color = 'green' if ft['success'] else 'red'
                obs = ft.get('error', '-') if not ft['success'] else '-'
                if len(obs) > 30:
                    obs = obs[:30] + '...'

                timestamp = ft.get('timestamp', '')
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp)
                        timestamp = dt.strftime('%H:%M:%S')
                    except:
                        pass

                table_data.append([
                    str(ft['file_index']),
                    f"{ft['duration_seconds']:.2f}",
                    Paragraph(f"<font color='{status_color}'><b>{status}</b></font>",
                             self.styles['Normal']),
                    timestamp,
                    obs
                ])

            table = Table(table_data, colWidths=[0.5*inch, 1*inch, 0.8*inch, 1.2*inch, 3*inch])
            table.setStyle(TableStyle([
                # Cabecalho
                ('BACKGROUND', (0, 0), (-1, 0), self.PRIMARY_COLOR),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

                # Corpo
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (0, 1), (1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                # Bordas
                ('GRID', (0, 0), (-1, -1), 0.5, self.LIGHT_GRAY),
                ('BOX', (0, 0), (-1, -1), 1, self.PRIMARY_COLOR),

                # Linhas alternadas
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.LIGHT_GRAY]),

                # Padding
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph("Nenhum dado detalhado disponivel.", self.styles['Normal']))

        elements.append(Spacer(1, 0.3*inch))
        return elements

    def _build_analysis(self) -> list:
        """Constroi secao de analise e recomendacoes"""
        elements = []

        elements.append(PageBreak())
        elements.append(Paragraph("Analise e Recomendacoes", self.styles['SectionTitle']))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.LIGHT_GRAY))
        elements.append(Spacer(1, 0.2*inch))

        success_rate = self.data.get('success_rate_percent', 0)
        avg_time = self.data.get('average_time_per_file', 0)
        files_per_min = self.data.get('files_per_minute', 0)
        total_files = self.data.get('total_files_processed', 0)

        # Analise de performance
        elements.append(Paragraph("<b>Performance:</b>", self.styles['Normal']))

        if avg_time < 20:
            perf_analysis = f"O tempo medio de {avg_time:.1f}s por arquivo e EXCELENTE. O sistema esta performando de forma otima."
            perf_color = self.SUCCESS_COLOR
        elif avg_time < 60:
            perf_analysis = f"O tempo medio de {avg_time:.1f}s por arquivo e BOM. Performance dentro do esperado."
            perf_color = self.SUCCESS_COLOR
        elif avg_time < 120:
            perf_analysis = f"O tempo medio de {avg_time:.1f}s por arquivo e REGULAR. Considere investigar possiveis gargalos."
            perf_color = self.WARNING_COLOR
        else:
            perf_analysis = f"O tempo medio de {avg_time:.1f}s por arquivo e ALTO. Recomenda-se investigacao de performance."
            perf_color = self.DANGER_COLOR

        elements.append(Paragraph(f"<font color='{perf_color}'>{perf_analysis}</font>",
                                 self.styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))

        # Analise de confiabilidade
        elements.append(Paragraph("<b>Confiabilidade:</b>", self.styles['Normal']))

        if success_rate >= 99:
            rel_analysis = "Sistema com ALTA confiabilidade. Taxa de sucesso proxima de 100%."
            rel_color = self.SUCCESS_COLOR
        elif success_rate >= 95:
            rel_analysis = "Sistema com BOA confiabilidade. Poucas falhas detectadas."
            rel_color = self.SUCCESS_COLOR
        elif success_rate >= 80:
            rel_analysis = "Sistema com confiabilidade MODERADA. Algumas falhas detectadas que merecem atencao."
            rel_color = self.WARNING_COLOR
        else:
            rel_analysis = "Sistema com BAIXA confiabilidade. Alta taxa de falhas requer investigacao imediata."
            rel_color = self.DANGER_COLOR

        elements.append(Paragraph(f"<font color='{rel_color}'>{rel_analysis}</font>",
                                 self.styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))

        # Capacidade estimada
        elements.append(Paragraph("<b>Capacidade Estimada:</b>", self.styles['Normal']))

        if files_per_min > 0:
            hourly = files_per_min * 60
            daily = hourly * 8  # 8 horas uteis

            capacity_text = f"""
            Com base nos resultados do teste:
            - <b>Por hora:</b> ~{hourly:.0f} arquivos
            - <b>Por dia (8h):</b> ~{daily:.0f} arquivos
            """
            elements.append(Paragraph(capacity_text, self.styles['Normal']))

        elements.append(Spacer(1, 0.2*inch))

        # Recomendacoes
        elements.append(Paragraph("<b>Recomendacoes:</b>", self.styles['Normal']))

        recommendations = []

        if success_rate < 100:
            recommendations.append("Investigar causas das falhas nos arquivos que nao foram processados")

        if avg_time > 30:
            recommendations.append("Considerar otimizacoes de performance no processamento de arquivos")

        if total_files < 10:
            recommendations.append("Executar testes com volumes maiores para validar escalabilidade")

        if files_per_min < 1:
            recommendations.append("Avaliar capacidade do sistema para atender demanda de producao")

        if not recommendations:
            recommendations.append("Sistema operando dentro dos parametros esperados. Manter monitoramento regular.")

        for i, rec in enumerate(recommendations, 1):
            elements.append(Paragraph(f"{i}. {rec}", self.styles['Normal']))

        elements.append(Spacer(1, 0.3*inch))
        return elements

    def _build_footer(self) -> list:
        """Constroi rodape do relatorio"""
        elements = []

        elements.append(Spacer(1, 0.5*inch))
        elements.append(HRFlowable(width="100%", thickness=2, color=self.PRIMARY_COLOR))
        elements.append(Spacer(1, 0.1*inch))

        footer_text = f"""
        <font size='8' color='gray'>
        Relatorio gerado automaticamente pelo sistema de Stress Test - RPA Track Trace RX<br/>
        Data de geracao: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}<br/>
        Ambiente: QA Portal | Versao: 1.0
        </font>
        """
        elements.append(Paragraph(footer_text, self.styles['CenterText']))

        return elements

    def _get_test_type(self) -> str:
        """Retorna o tipo de teste baseado nos resultados"""
        results = self.data.get('results', [])
        if results:
            types = [r.get('test_type', '') for r in results]
            return ', '.join(set(types))
        return 'Manual Upload'


def generate_pdf_report(metrics_dict: dict, output_dir: str = None) -> str:
    """
    Funcao helper para gerar relatorio PDF

    Args:
        metrics_dict: Dicionario com metricas do stress test
        output_dir: Diretorio de saida (opcional)

    Returns:
        Caminho do arquivo PDF gerado
    """
    report = StressTestPDFReport(metrics_dict, output_dir)
    return report.generate()


# Para testes
if __name__ == "__main__":
    # Dados de exemplo
    sample_data = {
        "test_id": "test123",
        "total_duration_seconds": 120.5,
        "average_time_per_file": 12.05,
        "success_rate_percent": 100.0,
        "files_per_minute": 4.98,
        "total_files_processed": 10,
        "successful_files": 10,
        "failed_files": 0,
        "file_times": [
            {"file_index": 1, "duration_seconds": 11.2, "success": True, "timestamp": "2025-01-01T10:00:00"},
            {"file_index": 2, "duration_seconds": 12.5, "success": True, "timestamp": "2025-01-01T10:00:12"},
            {"file_index": 3, "duration_seconds": 10.8, "success": True, "timestamp": "2025-01-01T10:00:25"},
            {"file_index": 4, "duration_seconds": 13.1, "success": True, "timestamp": "2025-01-01T10:00:38"},
            {"file_index": 5, "duration_seconds": 11.9, "success": True, "timestamp": "2025-01-01T10:00:51"},
        ],
        "results": [
            {"test_type": "Manual Upload", "batch_size": 5, "metrics": {}}
        ]
    }

    pdf_path = generate_pdf_report(sample_data)
    print(f"PDF gerado: {pdf_path}")
