@Inventory
Feature: Inventory

  # Cenários simplificados - apenas navegação

  @smoke_inventory_adjustments
  Scenario: Navigate to Inventory Adjustments
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    Then End test

  @smoke_quarantine
  Scenario: Navigate to Quarantine
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    Then End test

  # Cenários completos - dependem de Inbound (temporariamente desabilitados)

  @skip
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

  @skip
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

  @skip
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
    And End test

  @skip
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
    And End test

  @skip
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
    And End test
