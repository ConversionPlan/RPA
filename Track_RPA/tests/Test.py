from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import os
import sys
from datetime import datetime
import random as r #Randomize Number Library
from reportlab.lib import colors
data_atual = datetime.now()

def add_text(output_file):

    ph_no = []
    # A loop is used to generate 5 Numbers.
    for i in range(0, 5):
        ph_no.append(r.randint(0, 9))  # Each Number from 0 to 9
    # I take the numbers from the array and put them together
    P = ''
    for i in ph_no:
        P += str(i)

    Portal = "QA Assurance"
    Reference_Report = "ReportRPA_01"
    Date = datetime.now().strftime("%m/%d/%Y")
    Author = "Victor Angelo"

    Path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    output_path = Path + "\\Archives\\Detailed\\Track_Validation_" + P + ".pdf"

    # Create 01 Page Document
    cnv = canvas.Canvas(output_path, pagesize=A4)
    Path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    pdfmetrics.registerFont(
        TTFont('Arial', 'arial.ttf'))  # Replace 'arial.ttf' with the actual path to your Arial font file

    # Add Logo
    image_path = os.path.join(Path + "\\Archives\\images\\", "Logo_TrackTraceRX.png")
    cnv.drawImage(image_path, 300, 690, width=250, height=40)

    # Text = TrackRX Validation Report for
    font_name = "Arial"
    font_size = 24
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 550, "TrackRX Validation Report for")
    cnv.drawString(50, 525, Portal)

    # Text = Reference Report
    font_size = 13.5
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 350, "Report Reference Number:")
    cnv.drawString(220, 350, Reference_Report)

    # Text = Date Report
    cnv.drawString(50, 330, "Date of Issue:")
    cnv.drawString(140, 330, Date)

    # Text = Author RPA
    cnv.drawString(50, 310, "Author:")
    cnv.drawString(100, 310, Author)

    # Save 01 Page Document
    cnv.showPage()

    # Text = Execultive Summary
    font_name = "Arial"
    font_size = 16
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 750, "1. Execultive Summary")

    # Text = Text of Execultive Summary
    font_size = 12
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 720, "This report details the validation activities performed from " + Date + " for the Customers")
    cnv.drawString(50, 700, "Portal capturing findings from the RPA phases.")
    cnv.drawString(50, 680, "The TrackRX Portal successfully met all validation criteria.")

    # Text = Introduction Summary
    font_name = "Arial"
    font_size = 16
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 620, "2. Introduction")

    # Text = Text of Introduction Summary
    font_size = 12
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 590, "The validation activities are intended to confirm that the TrackRX Portal is installed, operates,")
    cnv.drawString(50, 570, "and performs according to manufacturer specifications and company requirements.")

    # Text = Deviations and Corrective Actions Summary
    font_name = "Arial"
    font_size = 16
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 510, "3. Deviations and Corrective Actions")

    # Text = Text of Deviations and Corrective Actions Summary
    font_size = 12
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 480, "No deviations were observed during the validation process.")

    # Text = Methodology Summary
    font_name = "Arial"
    font_size = 16
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 420, "4. Methodology")

    # Text = Text of Deviations and Corrective Actions Summary
    font_size = 12
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 390, "You can find the entire detailed process that was performed by Track Trace RPA on the")
    cnv.drawString(50, 370, "next page.")

    # Save 02 Page Document
    cnv.showPage()

    # Text = Process Sub Summary
    font_name = "Arial"
    font_size = 16
    cnv.setFont(font_name, font_size)
    cnv.drawString(50, 750, "1.1 Detailed RPA Process")

    font_name = "Arial"
    font_size = 12
    cnv.setFont(font_name, font_size)

    # Definir o número de colunas e largura das colunas
    num_colunas = 3
    largura_coluna = 120

    # Definir a posição inicial da tabela
    x_inicial = 50
    y_inicial = 720

    # Definir o espaçamento entre as linhas da tabela
    espacamento_entre_linhas = 20

    # Definir os dados da tabela (pode ser uma lista de listas)
    dados_tabela = [
        ["", "", "", ""],
        ["Module", "Report", "Start and End Time", "Result"],
        ["Dado 2,1", "Dado 2,2", "Dado 2,3", "Dado 2,4"],
        # Adicione mais linhas conforme necessário
    ]

    # Definir o estilo da tabela
    estilo_tabela = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]

    # Configurar a fonte e tamanho
    font_name = "Arial"
    font_size = 12
    cnv.setFont(font_name, font_size)

    # Desenhar a tabela
    for linha, dados_linha in enumerate(dados_tabela):
        for coluna, dado in enumerate(dados_linha):
            # Calcular a posição da célula
            x = x_inicial + coluna * largura_coluna
            y = y_inicial - linha * espacamento_entre_linhas

            # Calcular as coordenadas para as bordas da célula
            x1 = x
            y1 = y
            x2 = x + largura_coluna
            y2 = y - espacamento_entre_linhas

            # Desenhar a célula
            cnv.drawString(x, y, str(dado))

            # Adicionar bordas
            cnv.rect(x1, y1, x2 - x1, y2 - y1)

    # input_txt = "C:\\Users\\Victor Angêlo\\OneDrive\\TRACK\\Development\\Python Development\\Automation\\Track_RPA\\Archives\\Output\\Output_24269.txt"
    # # Adicione o conteúdo do arquivo de texto ao novo PDF
    # with open(input_txt, 'r', encoding='latin-1') as txt_file:
    #     lines = txt_file.readlines()
    #
    #     espacamento_entre_linhas = 20
    #     y_position = 720
    #     for line in lines:
    #         cnv.drawString(50, y_position, line.strip())
    #         y_position -= espacamento_entre_linhas  # Ajuste para o próximo espaçamento entre as linhas

    # Save 03 Page Document and Save Document
    cnv.save()

add_text("Track_Validation.pdf")

