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
    And Add Pack Size 1
    And Click on Identifiers tab
    And Add SKU
    And Add UPC
    And Add GS1 Company Prefix
    And Add GS1 ID
    And Click on Add Identifier
    And Wait for Identifier Options to Load
    And Add Identifier Value
    And Click on Add NDC
    And Click on Requirements Tab
    And Add Generic Name
    And Add Strength
    And Add Net Content Description
    And Add Notes
    And Click on Add
    Then Product should be saved
    And End test

  Scenario: Create an Aggregation Product
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Product Management
    And Click on Add - Product Management Page
    And Click on Aggregation Tab
    And Click on Add Product
    And Input Name of Each Product into Product Name
    And Click on Product Name
    And Add Product Quantity
    And Click on Add Child Product
    And Click on General Tab
    And Add Saved Product Name
    And Add Pack Size 2
    And Select Pack Size Case
    And Click on Identifiers tab
    And Add Saved SKU
    And Add Saved UPC
    And Add GS1 Company Prefix
    And Add GS1 ID
    And Click on Add Identifier
    And Add Identifier Value
    And Wait for Identifier Options to Load
    And Click on Add NDC
    And Click on Requirements Tab
    And Add Generic Name
    And Add Strength
    And Add Net Content Description
    And Add Notes
    And Click on Misc Tab
    And Disable Leaf Product
    And Click on Add
    Then Product should be saved
    And End test