@Product_Management
Feature: Product Management

  Scenario: Create an Each Product
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Product Management
    And Click on Add - Product Management Page
    And Add Product Name
    And Click on Identifiers tab
    And Add SKU
    And Add UPC
    And Add GS1 Company Prefix
    And Add GS1 ID
    And Click on Add Identifier
    And Wait for Identifier Options to Load
    And Click on Identifier Value
    And Click on Add NDC
    And Click on Requirements Tab
    And Add Generic Name
    And Add Strength
    And Add Net Content Description
    And Add Notes
    And Click on Add
    Then Product should be saved
    And End test