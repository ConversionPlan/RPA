@AutomaticDropship
Feature: Automatic Dropship

  # Testes para a funcionalidade de Automatic Dropship
  # Baseado na gravação de tela de 2025-12-19

  @smoke_dropship
  Scenario: Navigate to Automatic Dropship
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Automatic Dropship
    Then Automatic Dropship page should be displayed

  @dropship_list
  Scenario: Verify Automatic Dropship list is displayed
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Automatic Dropship
    Then Automatic Dropship table should have columns
    And Automatic Dropship records should be displayed

  @dropship_details
  Scenario: View Dropship Details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Automatic Dropship
    And Click on first dropship record
    Then Dropship Details modal should be displayed
    And Dropship Details should show shipment information

  @dropship_search
  Scenario: Search Automatic Dropship by PO number
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Automatic Dropship
    And Search dropship by PO number "PO"
    Then Search results should be filtered

  @dropship_export
  Scenario: Export Automatic Dropship data to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Automatic Dropship
    And Click on Save As button
    And Select CSV option from Save As menu
    Then CSV file should be downloaded
