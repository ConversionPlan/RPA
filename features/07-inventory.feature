@Inventory
Feature: Inventory

  Scenario: Transfer Item
    Given User exists
    And Is Logged In
    And There is an Inbound done
    When Return to dashboard page
    And Click on Inventory button
    And Click on Item Transfer
    And Click on New Item Transfer
    And Change Current Location
    And Change New Location
    And Set Reason
    And Add Reference
    And Click on Items Tab
    And Click on Add with Item Look Up
    And Search Inbounded Item by Name
    And Click on Inbounded Item
    And Select Lot and Expiration Date
    And Select Inbounded Item
    And Click on OK - Transfer Items
    Then Item should be transferred
    And End test

  Scenario: Quarantine Item
    Given User exists
    And Is Logged In
    And There is an Inbound done
    When Return to dashboard page
    And Open sandwich menu
    And Click on Quarantine
    And Click on Quarantine Items
    And Change Current Location
    And Set Reason
    And Add Reference
    And Click on Items Tab
    And Click on Add with Item Look Up
    And Search Inbounded Item by Name
    And Click on Inbounded Item
    And Select Lot and Expiration Date
    And Select Inbounded Item
    And Click on OK - Transfer Items
    And Click on Items in Quarantine
    Then Item should be quarantined
    And End test

  Scenario: Destroy Item
    Given User exists
    And Is Logged In
    And There is an Inbound done
    When Return to dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Destructions
    And Click on Destruct Inventory
    And Change Current Location
    And Set Inventory Adjustment Reason
    And Add Reference
    And Click on Items Tab
    And Click on Add with Item Look Up
    And Search Inbounded Item by Name
    And Click on Inbounded Item
    And Select Lot and Expiration Date
    And Select Inbounded Item
    And Click on OK - Transfer Items
    Then Item should be destroyed
    And End test

  Scenario: Report Missing/Stolen Item
    Given User exists
    And Is Logged In
    And There is an Inbound done
    When Return to dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Missing/Stolen
    And Click on Add Missing/Stolen Item
    And Change Current Location
    And Set Inventory Adjustment Reason
    And Add Reference
    And Click on Items Tab
    And Click on Add with Item Look Up
    And Search Inbounded Item by Name
    And Click on Inbounded Item
    And Select Lot and Expiration Date
    And Select Inbounded Item
    And Click on Add - Report Missing/Stolen
    Then Item should be reported
    And End test

  Scenario: Dispense Item
    Given User exists
    And Is Logged In
    And There is an Inbound done
    When Return to dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Dispenses
    And Click on Dispense Inventory
    And Change Current Location
    And Add Reference
    And Click on Items Tab
    And Click on Add with Item Look Up
    And Search Inbounded Item by Name
    And Click on Inbounded Item
    And Select Lot and Expiration Date
    And Select Inbounded Item
    And Click on OK - Transfer Items
    Then Item should be dispensed
    And End test

#  Scenario: Transform Item
#    Given User exists
#    And Is Logged In
#    And There is an Inbound done
#    When Return to dashboard page
#    And Open sandwich menu
#    And Click on Transformation
#    And Click on Recipes Management
#    And Click on Add Recipe
#    And Add Recipe Name
#    And Click on Ingredients Tab
#    And Click on Add Product - Transformation Ingredient
#    And Click on OK - Add Product
#    And Search Inbounded Item by Name
#    And Click on Inbounded Item
#    And Add Quantity
#    And Click on Add - Add Product
#    And Click on Outcome Products Tab
#    And Click on Add Product - Transformation Outcome
#    And Search for an RPA Product
#    And Select an Each RPA Product
#    And Add Quantity
#    And Click on Add - Recipe Management
#    And Click on Add - Create Recipe
#    And Open sandwich menu
#    And Click on Transformation
#    And Click on Transform Inventory
#    And Select Inbounded Recipe
#    And Select Inbounded Location
#    And Click on OK - Transform Product
#    And Click on Ingredients Tab
#    And Click on Ingredient Record icon
#    And Click on Add - Transform Product Ingredient Record
#    And Click on Serial
#    And Select a Serial
#    And Click on Add Selection
#    And Click on OK - Transform Product Ingredient Record
#    And Click on Outcome Products Tab
#    And Click on Outcome Ingredient Record icon
#    And Select Area
#    And Click on OK - Outcome Products
#    And Click on OK - Transform Product
#    Then Item should be transformed
#    And End test