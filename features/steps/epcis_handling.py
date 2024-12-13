from behave import *
from selenium.webdriver.common.by import By
from features.steps.utils import *
from features.steps.auth import ends_timer
from datetime import datetime, timedelta
import os


@given("User has an Inbound file")
def user_has_inbound_file(context):
    try:
        context.xml = read_xml("dummy_inbound_epcis.xml")
    except:
        ends_timer(context)
        raise

@when("File's creation date and time is before now")
def file_creation_datetime_before_now(context):
    try:
        current_time = datetime.now()
        biggest_delta = timedelta(days=20)
        medium_delta = timedelta(days=10)
        shortest_delta = timedelta(days=5)
        context.creation_time = current_time - biggest_delta
        context.first_step_time = current_time - medium_delta
        context.last_step_time = current_time - shortest_delta
        context.timezone = "-04:00"

        creation_time = context.creation_time.isoformat()
        creation_time += context.timezone
        context.xml[1] = change_xml_attribute_value(context.xml[1], "creationDate", creation_time)
        context.xml[16] = change_xml_tag_value(context.xml[16], creation_time)
    except:
        ends_timer(context)
        raise

@when("File's sbdh:Sender SGLN is from saved vendor")
def file_sender_sgln_from_registered_vendor(context):
    try:
        context.xml[6] = change_xml_tag_value(context.xml[6], context.vendor_sgln)
    except:
        ends_timer(context)
        raise

@when("File's sbdh:Receiver SGLN is from saved location")
def file_receiver_sgln_from_registered_location(context):
    try:
        context.xml[9] = change_xml_tag_value(context.xml[9], context.receiver_sgln)
    except:
        ends_timer(context)
        raise

@when("File's Item LGTIN is from saved product's GTIN")
def file_item_lgtin_from_gtin(context):
    try:
        context.product_lot = generate_x_length_number(22)
        context.lgtin = f"urn:epc:class:lgtin:{context.product_gtin}.{context.product_lot}"
        context.xml[23] = change_xml_attribute_value(context.xml[23], "id", context.lgtin)
        context.xml[101] = change_xml_tag_value(context.xml[101], context.lgtin)
    except:
        ends_timer(context)
        raise

@when("File's Item Expiration Date is a valid date in format YYYY-MM-DD")
def file_item_expiration_in_format(context):
    try:
        expiration_delta = timedelta(weeks=100)
        expiration_date = context.current_time + expiration_delta
        context.expiration_date = context.expiration_date.strftime("%Y-%m-%d")
        context.xml[24] = change_xml_tag_value(context.xml[24], context.expiration_date)
    except:
        ends_timer(context)
        raise

@when("File's Item SGTIN is from saved product's GTIN")
def file_item_sgtin_from_gtin(context):
    try:
        sgtin = f"urn:epc:idpat:sgtin:{context.product_gtin}.*"
        context.xml[26] = change_xml_attribute_value(context.xml[26], "id", sgtin)
    except:
        ends_timer(context)
        raise

@when("File's Item additionalTradeItemIdentification is a valid NDC")
def file_receiver_ndc_from_registered_product(context):
    try:
        context.xml[27] = change_xml_tag_value(context.xml[27], context.product_sku)
    except:
        ends_timer(context)
        raise

@when("File's Item Name from saved product")
def file_item_name_from_saved_product(context):
    try:
        context.xml[29] = change_xml_tag_value(context.xml[29], context.product_sku)
    except:
        ends_timer(context)
        raise


@when("File's Sender Location matches the one in sbdh:Sender")
def file_sender_location_vendor_location(context):
    try:
        context.xml[39] = change_xml_attribute_value(context.xml[39], "id", context.vendor_sgln)
    except:
        ends_timer(context)
        raise

@when("File's Sender Name matches the saved vendor")
def file_sender_name(context):
    try:
        context.xml[40] = change_xml_tag_value(context.xml[40], context.vendor_name)
    except:
        ends_timer(context)
        raise


@when("File's Sender Address matches the saved vendor")
def file_sender_address(context):
    try:
        context.xml[41] = change_xml_tag_value(context.xml[41], context.vendor_address)
    except:
        ends_timer(context)
        raise


@when("File's Sender City matches the saved vendor")
def file_sender_city(context):
    try:
        context.xml[42] = change_xml_tag_value(context.xml[42], context.vendor_city)
    except:
        ends_timer(context)
        raise


@when("File's Sender State matches the saved vendor")
def file_sender_state(context):
    try:
        context.xml[43] = change_xml_tag_value(context.xml[43], context.vendor_state)
    except:
        ends_timer(context)
        raise


@when("File's Sender Zip matches the saved vendor")
def file_sender_zip(context):
    try:
        context.xml[44] = change_xml_tag_value(context.xml[44], context.vendor_zip)
    except:
        ends_timer(context)
        raise


@when("File's Receiver Location matches the one in sbdh:Receiver")
def file_receiver_location_receiver_location(context):
    try:
        context.xml[47] = change_xml_attribute_value(context.xml[47], "id", context.receiver_sgln)
    except:
        ends_timer(context)
        raise

@when("File's Receiver Name matches the saved location")
def file_location_name(context):
    try:
        context.xml[48] = change_xml_tag_value(context.xml[48], context.location_name)
    except:
        ends_timer(context)
        raise


@when("File's Receiver Address matches the saved location")
def file_location_address(context):
    try:
        context.xml[49] = change_xml_tag_value(context.xml[49], context.location_address)
    except:
        ends_timer(context)
        raise


@when("File's Receiver City matches the saved location")
def file_location_city(context):
    try:
        context.xml[50] = change_xml_tag_value(context.xml[50], context.location_city)
    except:
        ends_timer(context)
        raise


@when("File's Receiver State matches the saved location")
def file_location_state(context):
    try:
        context.xml[51] = change_xml_tag_value(context.xml[51], context.location_state)
    except:
        ends_timer(context)
        raise


@when("File's Receiver Zip matches the saved location")
def file_location_zip(context):
    try:
        context.xml[52] = change_xml_tag_value(context.xml[52], context.location_zip)
    except:
        ends_timer(context)
        raise


@when("top ObjectEvent/eventTime and ObjectEvent/eventTimeZoneOffset are after the one in top ObjectEvent")
def top_eventTime(context):
    try:
        last_step_time = context.last_step_time.isoformat()
        context.xml[67] = change_xml_tag_value(context.xml[67], last_step_time)
        context.xml[68] = change_xml_tag_value(context.xml[68], context.timezone)
    except:
        ends_timer(context)
        raise


@when("top ObjectEvent/epcList/epc is a serialized version of File's Item SGTIN")
def top_SGTIN(context):
    try:
        serial = generate_x_length_number(12)
        sgtin = f"urn:epc:id:sgtin:{context.product_gtin}.{serial}"
        context.xml[70] = change_xml_tag_value(context.xml[70], sgtin)
    except:
        ends_timer(context)
        raise


@when("top ObjectEvent/readPoint and ObjectEvent/bizLocation are valid SGLNs not necessarily registered on Portal")
def top_readpoint_bizlocation(context):
    try:
        gcp = generate_company_prefix()
        gln = generate_gln(gcp)
        context.manufacturer_sgln = generate_sgln_from_gln(gln)

        context.xml[77] = change_xml_tag_value(context.xml[77], context.manufacturer_sgln)
        context.xml[79] = change_xml_tag_value(context.xml[79], context.manufacturer_sgln)

    except:
        ends_timer(context)
        raise


@when("ilmd/cbvmda:lotNumber is a valid lot number")
def top_lotnumber(context):
    try:
        context.xml[83] = change_xml_tag_value(context.xml[83], context.product_lot)
    except:
        ends_timer(context)
        raise


@when("ilmd/cbvmda:itemExpirationDate is a valid date in format YYYY-MM-DD")
def top_expiration_date(context):
    try:
        context.xml[84] = change_xml_tag_value(context.xml[84], context.expiration_date)
    except:
        ends_timer(context)
        raise


@when("bottom ObjectEvent/eventTime and ObjectEvent/eventTimeZoneOffset are after the one in creation date")
def bottom_eventtime(context):
    try:
        first_step_time = context.first_step_time.isoformat()
        context.xml[89] = change_xml_tag_value(context.xml[89], first_step_time)
        context.xml[90] = change_xml_tag_value(context.xml[90], context.timezone)
    except:
        ends_timer(context)
        raise


@when("bottom ObjectEvent/readPoint is the SGLN from sbdh:Sender")
def bottom_readpoint(context):
    try:
        context.xml[96] = change_xml_tag_value(context.xml[96], context.vendor_sgln)
    except:
        ends_timer(context)
        raise


@when("bottom ObjectEvent/sourceList/source is the SGLN from sbdh:Sender")
def bottom_source_sgln(context):
    try:
        context.xml[106] = change_xml_tag_value(context.xml[106], context.vendor_sgln)
    except:
        ends_timer(context)
        raise


@when("bottom ObjectEvent/destinationList/destination is the SGLN from sbdh:Receiver")
def bottom_destion_sgln(context):
    try:
        context.xml[109] = change_xml_tag_value(context.xml[109], context.receiver_sgln)
        context.filename = "created_inbound_epcis.xml"
        save_xml(context.xml, context.filename)
    except:
        ends_timer(context)
        raise



@when("Click on Utilities")
def click_utilities(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//a[@href='/utilities/']").click()
    except:
        ends_timer(context)
        raise


@when("Click on Manual EPCIS (XML) / X12 EDI (XML) File Upload")
def click_manual_epcis(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//label[text()='Manual EPCIS (XML) / X12 EDI (XML) File Upload']").click()
    except:
        ends_timer(context)
        raise


@when("Upload the EPCIS file")
def upload_epcis_file(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//input[@name='file']").send_keys(f"{os.getcwd()}/files/{context.filename}")
    except:
        ends_timer(context)
        raise


@then("Manual EPCIS File Upload success message should appear")
def epcis_should_upload(context):
    try:
        context.driver.find_element(by=By.XPATH, value="//div[text()='File uploading']")
    except:
        ends_timer(context)
        raise