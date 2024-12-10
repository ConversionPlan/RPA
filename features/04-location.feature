@Location_Management
Feature: Location Management

  Scenario: Create a new customer's location
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Locations Management
    And Click on Add - Location Management Page
    And Add Location Name
    And Add Location GLN 0055779
    And Add Location SGLN
    And Click on Add
    And Search Location by Name
    And Click on the Pencil next to its Name
    And Click on Address Tab - Location Management Page
    And Click on Add - Location
    And Add Customer Address Nickname
    And Add Customer Address GLN
    And Add Customer Address SGLN
    And Add Customer Address Recipient Name
    And Add Customer Address Line 1
    And Add Customer Address City
    And Add Customer Address ZIP
    And Click on Add - Save Customer Address
    And Click on Save - Location
    Then Location should be saved
    And End test