@InventoryAdjustments
Feature: Inventory Adjustments (Ajustes de Estoque)

  # Testes para a funcionalidade de Ajustes de Estoque
  # URL: /adjustments/
  # Inclui: Destruicoes, Distribuicao, Desaparecido/Roubado

  # ========================================
  # Navegacao Principal
  # ========================================

  @smoke_adjustments
  Scenario: Navigate to Inventory Adjustments
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    Then Inventory Adjustments page should be displayed

  # ========================================
  # Destruicoes
  # ========================================

  @destructions_list
  Scenario: View Destructions list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Destructions
    Then Destructions page should be displayed
    And Destructions table should have columns

  @destructions_add
  Scenario: Add inventory destruction
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Destructions
    And Click on Add Destruction button
    And Select destruction location
    And Scan or enter serial numbers for destruction
    And Fill destruction reason
    And Fill destruction date
    And Click on Save Destruction
    Then Destruction should be recorded successfully

  @destructions_search
  Scenario: Search Destructions
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Destructions
    And Search destruction by serial number
    Then Search results should be filtered

  @destructions_details
  Scenario: View Destruction details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Destructions
    And Click on first destruction record
    Then Destruction Details modal should be displayed
    And Destruction Details should show all information

  @destructions_export
  Scenario: Export Destructions to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Destructions
    And Click on Save As button
    And Select CSV option from Save As menu
    Then CSV file should be downloaded

  # ========================================
  # Distribuicao (Dispense)
  # ========================================

  @dispense_list
  Scenario: View Dispense list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Dispense
    Then Dispense page should be displayed
    And Dispense table should have columns

  @dispense_add
  Scenario: Add inventory dispense
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Dispense
    And Click on Add Dispense button
    And Select dispense location
    And Scan or enter serial numbers for dispense
    And Fill dispense reason
    And Fill dispense date
    And Click on Save Dispense
    Then Dispense should be recorded successfully

  @dispense_search
  Scenario: Search Dispense records
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Dispense
    And Search dispense by serial number
    Then Search results should be filtered

  @dispense_details
  Scenario: View Dispense details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Dispense
    And Click on first dispense record
    Then Dispense Details modal should be displayed
    And Dispense Details should show all information

  @dispense_export
  Scenario: Export Dispense to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Dispense
    And Click on Save As button
    And Select CSV option from Save As menu
    Then CSV file should be downloaded

  # ========================================
  # Desaparecido / Roubado (Missing/Stolen)
  # ========================================

  @missing_stolen_list
  Scenario: View Missing/Stolen list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Missing Stolen
    Then Missing Stolen page should be displayed
    And Missing Stolen table should have columns

  @missing_stolen_add
  Scenario: Report missing/stolen inventory
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Missing Stolen
    And Click on Add Missing Stolen button
    And Select adjustment location
    And Scan or enter serial numbers
    And Select adjustment type Missing or Stolen
    And Fill adjustment reason
    And Fill adjustment date
    And Click on Save Adjustment
    Then Missing Stolen adjustment should be recorded successfully

  @missing_stolen_search
  Scenario: Search Missing/Stolen records
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Missing Stolen
    And Search by serial number
    Then Search results should be filtered

  @missing_stolen_details
  Scenario: View Missing/Stolen details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Missing Stolen
    And Click on first record
    Then Missing Stolen Details modal should be displayed
    And Missing Stolen Details should show all information

  @missing_stolen_export
  Scenario: Export Missing/Stolen to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Missing Stolen
    And Click on Save As button
    And Select CSV option from Save As menu
    Then CSV file should be downloaded

  # ========================================
  # Cenarios Adicionais
  # ========================================

  @adjustment_filter_by_date
  Scenario: Filter adjustments by date range
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Destructions
    And Set date filter from last 30 days
    And Apply date filter
    Then Records should be filtered by date range

  @adjustment_filter_by_location
  Scenario: Filter adjustments by location
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Destructions
    And Select location filter
    And Apply location filter
    Then Records should be filtered by location

  @adjustment_bulk_action
  Scenario: Perform bulk destruction
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inventory Adjustments
    And Click on Destructions
    And Click on Add Destruction button
    And Select destruction location
    And Scan multiple serial numbers
    And Fill destruction reason
    And Click on Save Destruction
    Then All items should be destroyed successfully
