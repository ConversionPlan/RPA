from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import os
import json
from datetime import datetime

def generate_pdf():
    print("PATH:", os.path.abspath(os.getcwd()))

    # Texts for the PDF
    portal: str = "QA Assurance"
    reference_report: str = "ReportRPA_01"
    cur_date: str = datetime.now().strftime("%m/%d/%Y")
    author: str = "Violeta Carvalho"
    output_path: str = "report/Track_Validation.pdf"

    # PDF styles
    font_name = "Arial"
    small_font = 12
    medium_small_font = 13.5
    medium_font = 16
    big_font = 24
    left_margin = 50

    # Create 01 Page Document
    cnv = canvas.Canvas(output_path, pagesize=A4)
    pdfmetrics.registerFont(
        TTFont('Arial', 'report/arial.ttf'))  # Replace 'arial.ttf' with the actual path to your Arial font file

    # Add Logo
    image_path = os.path.join("report", "Logo_TrackTraceRX.png")
    cnv.drawImage(image_path, 300, 690, width=250, height=40)

    # Text = TrackRX Validation Report for
    cnv.setFont(font_name, big_font)
    cnv.drawString(left_margin, 550, "TrackRX Validation Report for")
    cnv.drawString(left_margin, 525, portal)

    # Text = Reference Report
    cnv.setFont(font_name, medium_small_font)
    cnv.drawString(left_margin, 350, "Report Reference Number:")
    cnv.drawString(220, 350, reference_report)

    # Text = Date Report
    cnv.drawString(left_margin, 330, "Date of Issue:")
    cnv.drawString(140, 330, cur_date)

    # Text = Author RPA
    cnv.drawString(left_margin, 310, "Author:")
    cnv.drawString(100, 310, author)

    # Save 01 Page Document
    cnv.showPage()

    # Text = Execultive Summary
    cnv.setFont(font_name, medium_font)
    cnv.drawString(left_margin, 750, "1. Executive Summary")

    # Text = Text of Executive Summary
    cnv.setFont(font_name, small_font)
    cnv.drawString(left_margin, 720, "This report details the validation activities performed from " + cur_date + " for the Customers")
    cnv.drawString(left_margin, 700, "Portal capturing findings from the RPA phases.")
    cnv.drawString(left_margin, 680, "The TrackRX Portal successfully met all validation criteria.")

    # Text = Introduction Summary
    cnv.setFont(font_name, medium_font)
    cnv.drawString(left_margin, 620, "2. Introduction")

    # Text = Text of Introduction Summary
    cnv.setFont(font_name, small_font)
    cnv.drawString(left_margin, 590, "The validation activities are intended to confirm that the TrackRX Portal is installed, operates,")
    cnv.drawString(left_margin, 570, "and performs according to manufacturer specifications and company requirements.")

    # Text = Deviations and Corrective Actions Summary
    cnv.setFont(font_name, medium_font)
    cnv.drawString(left_margin, 510, "3. Deviations and Corrective Actions")

    # Text = Text of Deviations and Corrective Actions Summary
    cnv.setFont(font_name, small_font)
    cnv.drawString(left_margin, 480, "No deviations were observed during the validation process.")

    # Text = Methodology Summary
    cnv.setFont(font_name, medium_font)
    cnv.drawString(left_margin, 420, "4. Methodology")

    # Text = Text of Deviations and Corrective Actions Summary
    cnv.setFont(font_name, small_font)
    cnv.drawString(left_margin, 390, "You can find the entire detailed process that was performed by Track Trace RPA on the")
    cnv.drawString(left_margin, 370, "next page.")

    # Save 02 Page Document
    cnv.showPage()

    cnv.setFont(font_name, medium_font)
    cnv.drawString(left_margin, 750, "5. Detailed RPA Process")


    with open("report/results.json", "r") as file:
        results_json = json.load(file)

    for result in results_json:
        y = 710
        tag = result["tags"][0]
        cnv.setFont(font_name, medium_small_font)
        cnv.drawString(left_margin, y, f"Module: {tag}")
        cnv.setFont(font_name, small_font)

        for element in result["elements"]:
            y -= 20
            report = element["name"]
            result = element["status"].capitalize()
            cnv.drawString(left_margin, y, f"Report: {report} - {result}")

        cnv.save()


generate_pdf()

