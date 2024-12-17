from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import os
import json
from datetime import datetime


def generate_pdf():
    # Get Test Data
    with open("report/output/results.json", "r") as file:
        results_json = json.load(file)

    with open("report/test_times.json", "r") as file:
        times_json = json.load(file)

    has_failures = False

    # Texts for the PDF
    portal: str = "QA Assurance"
    reference_report: str = "ReportRPA_01"
    current_date: str = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    author: str = "Violeta Carvalho"
    output_path: str = "report/output/Track_Validation.pdf"

    for feature in results_json:
        for scenario in feature["elements"]:
            if scenario["status"] == "failed":
                has_failures = True

    # PDF styles
    font_name = "Arial"
    small_font = 12
    medium_small_font = 13.5
    medium_font = 16
    big_font = 24
    left_margin = 50

    # Create First Document Page
    cnv = canvas.Canvas(output_path, pagesize=A4)
    pdfmetrics.registerFont(
        TTFont("Arial", "report/arial.ttf")
    )  # Replace 'arial.ttf' with the actual path to your Arial font file

    # Add Logo
    image_path = os.path.join("report", "Logo_TrackTraceRX.png")
    cnv.drawImage(image_path, 300, 690, width=250, height=40)

    # Add Document Title
    cnv.setFont(font_name, big_font)
    cnv.drawString(left_margin, 550, "TrackRX Validation Report for")
    cnv.drawString(left_margin, 525, portal)

    # Add Document Metadata
    cnv.setFont(font_name, medium_small_font)
    cnv.drawString(left_margin, 350, f"Report Reference Number: {reference_report}")
    cnv.drawString(left_margin, 330, f"Date of Issue: {current_date}")
    cnv.drawString(left_margin, 310, f"Author: {author}")

    # Save First Document Page
    cnv.showPage()

    # Add Description
    cnv.setFont(font_name, medium_font)
    cnv.drawString(left_margin, 750, "1. Executive Summary")

    cnv.setFont(font_name, small_font)
    cnv.drawString(
        left_margin,
        720,
        "This report details the validation activities performed from "
        + current_date
        + " for the Customers",
    )
    cnv.drawString(left_margin, 700, "Portal capturing findings from the RPA phases.")

    cnv.setFont(font_name, medium_font)
    cnv.drawString(left_margin, 620, "2. Introduction")

    cnv.setFont(font_name, small_font)
    cnv.drawString(
        left_margin,
        590,
        "The validation activities are intended to confirm that the TrackRX Portal is installed, operates,",
    )
    cnv.drawString(
        left_margin,
        570,
        "and performs according to manufacturer specifications and company requirements.",
    )

    cnv.setFont(font_name, medium_font)
    cnv.drawString(left_margin, 510, "3. Deviations and Corrective Actions")

    cnv.setFont(font_name, small_font)
    if has_failures == False:
        cnv.drawString(
            left_margin,
            480,
            "No deviations were observed during the validation process.",
        )
    else:
        cnv.drawString(
            left_margin, 480, "Deviations were observed during the validation process."
        )

    cnv.setFont(font_name, medium_font)
    cnv.drawString(left_margin, 420, "4. Methodology")

    cnv.setFont(font_name, small_font)
    cnv.drawString(
        left_margin,
        390,
        "You can find the entire detailed process that was performed by Track Trace RPA on the",
    )
    cnv.drawString(left_margin, 370, "next page.")

    # Save Second Document Page
    cnv.showPage()

    # Add Detailed Process Title
    cnv.setFont(font_name, medium_font)
    y = 750
    cnv.drawString(left_margin, y, "5. Detailed RPA Process")

    index = 0
    last_module = None
    for result in results_json:
        # Module
        if result["tags"][0] == "Ignore":
            continue
        tag = result["tags"][0].replace("_", " ")

        y -= 10

        # If current module is different from last, add as header
        if last_module != tag:
            y -= 30
            if y <= 70:
                cnv.showPage()
                y = 750

            cnv.setFont(font_name, medium_small_font)
            cnv.drawString(left_margin, y, f"Module: {tag}")

        # If last module still not set, set it
        if last_module is None:
            last_module = tag

        cnv.setFont(font_name, small_font)

        # Run through each test from a module
        for element in result["elements"]:
            y -= 30
            if y <= 70:
                cnv.showPage()
                y = 750

            report = element["name"]
            result = element["status"].capitalize()
            cnv.drawString(left_margin, y, f"Report: {report} - {result}")

            y -= 20
            time_json = times_json[index]
            index += 1

            cnv.drawString(
                left_margin,
                y,
                f"Start Time: {time_json["start"]} / End Time: {time_json["end"]}",
            )
            if result == "Failed":
                y -= 20
                for step in element["steps"]:
                    try:
                        if step["result"]["status"] == "failed":
                            cnv.drawString(
                                left_margin, y, f"Error in Step: {step["name"]}"
                            )
                    except KeyError:
                        pass

    cnv.save()

    # Reset Test Times json
    with open("report/test_times.json", "w") as file:
        file.write("[]")


generate_pdf()
