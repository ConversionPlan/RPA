@Outbound
Feature: Outbound

  Scenario: Create a SO by Picking and Shipping at Once
    Given User exists
    And Is Logged In
    And There is an Inbound done
    When Return to dashboard page
    And Click on Create sales order by picking
    And Select Type Customer
    And Search for an RPA Customer
    And Select a Customer
    And Click on Yes
    And Click on Change Location
    And Search for Location with Inbound
    And Select a Location
    And Add SO Number
    And Click on Bought By/Ship To Tab
    And Select Bought By Location as Main Address
    And Select Ship To as Ship To
    And Click on Picking Tab
    And Click on Inventory Lookup
    And Select Shown Product
    And Select Shown Serial
    And Click on Add Selection
    And Click on Save
    And Click on Shipped - Status
    And Click on Save - Confirm Products Quantity
    And Click on Shipped - Dashboard
    Then Outbound should be saved
    And End test