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