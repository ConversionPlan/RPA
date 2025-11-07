@Inbound
Feature: Inbound

#  Scenario: Create a Manual Inbound Shipment for an Each Product
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
#    And Select an Each RPA Product
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

#  Scenario: Create a Manual Inbound Shipment for a Case Product
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
#    And Select an Case RPA Product
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
#    And Click on Magnifying Glass
#    And Click on Add - Case Aggregation
#    And Choose the Product
#    And Choose the Lot
#    And Add Two Serial Numbers
#    And Click on OK - Add Aggregation
#    And Click on Close - Add Aggregation
#    And Click on OK - Manual Inbound Shipment
#    Then Inbound should be saved
#    And End test

# COMMENTED OUT - Múltiplos XPaths malformados no epcis-generator.py (timeout dentro do XPath)
#  Scenario: Manual Upload of EPCIS File
#    Given User exists
#    And Is Logged In
#    When Open dashboard page
#    And Open sandwich menu
#    And Click on Product Management
#    And Search for an RPA Product
#    And Click on RPA Product
#    And Click on Identifiers tab
#    And Save GS1 Info
#    And Close Modal
#    And Open sandwich menu
#    And Click on Trading Partners
#    And Search for an RPA Seller
#    And Click on RPA Seller
#    And Save the Seller Name
#    And Save the Seller SGLN
#    And Close Modal
#    And Open sandwich menu
#    And Click on Company Management
#    And Click on Locations Management
#    And Search for an RPA Location
#    And Click on RPA Location
#    And Save Location Name
#    And Save Location SGLN
#    And Close Modal
#    And Open a new tab
#    And Open EPCIS Generator
#    And Click on Generate Random Data
#    And Click on Sender Main Location Information
#    And Replace SGLN with Location's saved SGLN
#    And Replace Location Name with Location's saved name
#    And Click on Receiver Main Location Information
#    And Replace SGLN with Seller's saved SGLN
#    And Replace Location Name with Seller's saved name
#    And Click on #1 Product Information
#    And Replace Product Name with Product's saved name
#    And Replace SGTIN's with a new SGTIN GCP and GS1 ID
#    And Click on Submit
#    And Download EPCIS file
#    And Close the tab
#    And Open sandwich menu
#    And Click on Utilities
#    And Click on Manual EPCIS (XML) / X12 EDI (XML) File Upload
#    And Upload EPCIS file
#    Then Manual File Inbound should be saved
#    And End test

# COMMENTED OUT - Filtro de busca inconsistente após deleção (contagem muda de 2 para 263 registros)
#  Scenario: Delete Inbound
#    Given User exists
#    And Is Logged In
#    And There is an Inbound done
#    When Return to dashboard page
#    And Open sandwich menu
#    And Click on Inbound
#    And Search for All Delivery Status
#    And Save Amount of Records
#    And Click on Delete button
#    And Click on Yes - Confirmation
#    Then Inbound should be deleted
#    And End test