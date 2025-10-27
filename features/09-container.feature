@Container
Feature: Container

  Scenario: Create a Container
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Container Management
    And Click on Create New Container
    And Click on Save
    And Click on Dismiss
    And Click on List/Search Containers in Inventory
    Then Container should be created
    And End test

  Scenario: Delete a Container
    Given User exists
    And Is Logged In
    And There is a Container Created
    When Click on List/Search Containers in Inventory
    And Save Amount of Records
    And Save Container Serial
    And Open sandwich menu
    And Click on Container Management
    And Click on Delete container
    And Input Saved Serial
    And Click on OK - Deletion
    And Click on List/Search Containers in Inventory
    Then Container should be deleted
    And End test