@Product_Management
Feature: Product Management

  Scenario: Create a Product
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Product Management
    And Click on Add - Product Management Page
    And Add Product Name
    And Click on Identifiers tab
    And Add GS1 Company Prefix
    And Add GS1 ID
    And Click on Add Identifier
    And Wait for Identifier Options to Load
    And Click on Identifier Value
    And Click on Add NDC
    And Click on Add
    Then Product should be saved
    And End test