@Inbound
Feature: Inbound

  Scenario: Create a Manual Inbound Shipment
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inbound
    And Click on Manual Inbound Shipment
    And Click on Change Location
    And Search for an RPA Location
    And Select a Location
    And Click on Change Seller
    And Select Type Vendor
    And Search for an RPA Seller
    And Select a Seller
    And Click on Yes
    And Add PO Number
    And Click on Sold By/Ship From Tab
    And Select Sold By Location as Main Address
    And Select Ship From as Ship From
    And Click on Line Items Tab
    And Click on Add Product - Manual Inbound Shipment
    And Search for an RPA Product
    And Select an RPA Product
    And Add Quantity
    And Click on OK - Product Selection
    And Click on Add Lot/Source
    And Add Lot Number
    And Click on Serial Based
    And Click on OK - Lot/Source
    And Click on OK - Product Information
    And Get Product GTIN
    And Click on Aggregation Tab - Inbound
    And Click on Add - Aggregation
    And Select Product Radio Button
    And Choose the Product
    And Choose the Lot
    And Add the Serial Numbers
    And Click on OK - Add Aggregation
    And Click on OK - Manual Inbound Shipment
    Then Inbound should be saved
    And End test