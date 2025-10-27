@Manufacture
Feature: Manufacture

  Scenario: Manufacture Serials
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Click on Manufacture Lot and Serial Request
    And Click on Add Serialized Lot
    And Select an RPA Product from Dropdown
    And Add Lot Number - Manufacturer
    And Add Expiration Date - Manufacturer
    And Click on OK - Add Serialized Lot
    And Click on Pencil
    And Click on Serials Tab
    And Click on New Serials Request
    And Add Quantity to generate
    And Click on Add - Add Serial Request
    And Click on OK - Edit Manufacturer Lot
    Then Serials should be Manufactured
    And End test

  Scenario: Delete Manufactured Serials
    Given User exists
    And Is Logged In
    And There is a Manufactured Serial
    When Go back to dashboard page
    And Click on Manufacture Lot and Serial Request
    And Save Amount of Records
    And Click on Delete button
    And Click on Yes - Confirmation
    Then Serials should be Deleted
    And End test

  Scenario: Commission Serial Numbers
    Given User exists
    And Is Logged In
    And There is a Manufactured Serial
    When Go back to dashboard page
    And Click on Commission Serial Numbers
    And Save Amount of Records
    And Select Last Created Serials' Product
    And Click on Select Serials Numbers
    And Select Serial
    And Click on Select Serials Numbers - Select Serial
    And Click on Close the lot after commissioning the serials
    And Select Storage Area
    And Click on OK - Commission
    Then Serials should be Commissioned
    And End test