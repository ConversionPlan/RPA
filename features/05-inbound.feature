@Inbound
Feature: Inbound

#  Scenario: Create a Manual Inbound Shipment
#    Given User exists
#    And Is Logged In
#    When Open dashboard page
#    And Open sandwich menu
#    And Click on Inbound
#    And Click on Manual Inbound Shipment
#    And Click on Change Location
#    And Search for an RPA Location
#    And Select a Location
#    And Click on Change Seller
#    And Select Type Vendor
#    And Search for an RPA Seller
#    And Select a Seller
#    And Click on Yes
#    And Add PO Number
#    And Click on Sold By/Ship From Tab
#    And Select Sold By Location as Main Address
#    And Select Ship From as Ship From
#    And Click on Line Items Tab
#    And Click on Add Product - Manual Inbound Shipment
#    And Search for an RPA Product
#    And Select an RPA Product
#    And Add Quantity
#    And Click on OK - Product Selection
#    And Click on Add Lot/Source
#    And Add Lot Number
#    And Click on Serial Based
#    And Add Expiration Date
#    And Click on OK - Lot/Source
#    And Click on OK - Product Information
#    And Click on Aggregation Tab - Inbound
#    And Click on Add - Aggregation
#    And Select Product Radio Button
#    And Choose the Product
#    And Choose the Lot
#    And Add the Serial Numbers
#    And Click on OK - Add Aggregation
#    And Click on OK - Manual Inbound Shipment
#    Then Inbound should be saved
#    And End test

  Scenario: Create a Manual Electronic File Inbound Shipment
    Given User has an Inbound file
    And User exists
    And Is Logged In

    # GET ALL DATA FOR EPCIS
    When Open dashboard page
    And Open sandwich menu
    And Click on Trading Partners
    And Search for an RPA Vendor
    And Save Vendor's location
    And Save Vendor's Name
    And Click on Address Tab
    And View Vendor's First Address' Details
    And Save Vendor's Address Line 1
    And Save Vendor's City
    And Save Vendor's State
    And Save Vendor's Zip
    And Click on Close
    And Open sandwich menu
    And Click on Company Management
    And Click on Locations Management
    And Search for an RPA Location
    And Save RPA location
    And Save Location's Name
    And Click on Address Tab - Location Management Page
    And View Location's First Address' Details
    And Save Location's Address Line 1
    And Save Location's City
    And Save Location's State
    And Save Location's Zip
    And Click on Close
    And Open sandwich menu
    And Click on Product Management
    And Search for an RPA Product
    And Save RPA Product Name
    And Click on Identifiers tab
    And Save RPA Product SKU
    And Save RPA Product GTIN

    # EPCIS HEADER
    And File's creation date and time is before now
    And File's sbdh:Sender SGLN is from saved vendor
    And File's sbdh:Receiver SGLN is from saved location
    And File's Item LGTIN is from saved product's GTIN
    And File's Item Expiration Date is a valid date in format YYYY-MM-DD
    And File's Item SGTIN is from saved product's GTIN
    And File's Item additionalTradeItemIdentification is a valid NDC
    And File's Item Name from saved product
    And File's Sender Location matches the one in sbdh:Sender
    And File's Sender Name matches the saved vendor
    And File's Sender Address matches the saved vendor
    And File's Sender City matches the saved vendor
    And File's Sender State matches the saved vendor
    And File's Sender Zip matches the saved vendor
    And File's Receiver Location matches the one in sbdh:Receiver
    And File's Receiver Name matches the saved location
    And File's Receiver Address matches the saved location
    And File's Receiver City matches the saved location
    And File's Receiver State matches the saved location
    And File's Receiver Zip matches the saved location

    # EPCIS BODY
    And top ObjectEvent/eventTime and ObjectEvent/eventTimeZoneOffset are after the one in top ObjectEvent
    And top ObjectEvent/epcList/epc is a serialized version of File's Item SGTIN
    And top ObjectEvent/readPoint and ObjectEvent/bizLocation are valid SGLNs not necessarily registered on Portal
    And ilmd/cbvmda:lotNumber is a valid lot number
    And ilmd/cbvmda:itemExpirationDate is a valid date in format YYYY-MM-DD
    And bottom ObjectEvent/eventTime and ObjectEvent/eventTimeZoneOffset are after the one in creation date
    And bottom ObjectEvent/readPoint is the SGLN from sbdh:Sender
    And bottom ObjectEvent/sourceList/source is the SGLN from sbdh:Sender
    And bottom ObjectEvent/destinationList/destination is the SGLN from sbdh:Receiver

    # UPLOADING TO PORTAL
    And Open sandwich menu
    And Click on Utilities
    And Click on Manual EPCIS (XML) / X12 EDI (XML) File Upload
    And Upload the EPCIS file
    And Click on OK - Transfer Items
    Then Manual EPCIS File Upload success message should appear
    And End test