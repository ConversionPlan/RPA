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
