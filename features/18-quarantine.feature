@Quarantine
Feature: Quarantine (Quarentena)

  # Testes para a funcionalidade de Quarentena
  # URL: /quarantine/

  # ========================================
  # Navegacao Principal
  # ========================================

  @smoke_quarantine
  Scenario: Navigate to Quarantine
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    Then Quarantine page should be displayed

  # ========================================
  # Listagem e Visualizacao
  # ========================================

  @quarantine_list
  Scenario: View quarantine list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    Then Quarantine table should be displayed
    And Quarantine table should have columns

  @quarantine_details
  Scenario: View quarantine item details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    And Click on first quarantine record
    Then Quarantine Details modal should be displayed
    And Quarantine Details should show product information

  # ========================================
  # Adicionar a Quarentena
  # ========================================

  @quarantine_add
  Scenario: Add item to quarantine
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    And Click on Add to Quarantine button
    And Select quarantine location
    And Scan or enter serial number
    And Select quarantine reason
    And Add quarantine notes
    And Click on Save Quarantine
    Then Item should be added to quarantine successfully

  @quarantine_add_multiple
  Scenario: Add multiple items to quarantine
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    And Click on Add to Quarantine button
    And Select quarantine location
    And Scan multiple serial numbers
    And Select quarantine reason
    And Click on Save Quarantine
    Then All items should be added to quarantine

  # ========================================
  # Liberar da Quarentena
  # ========================================

  @quarantine_release_multiple
  Scenario: Release multiple items from quarantine
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    And Select multiple quarantine records
    And Click on Bulk Release button
    And Add release notes
    And Confirm release
    Then All selected items should be released

  # ========================================
  # Pesquisa e Filtros
  # ========================================

  @quarantine_search
  Scenario: Search quarantine by serial number
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    And Search by serial number
    Then Quarantine search results should be filtered

  @quarantine_filter_by_reason
  Scenario: Filter quarantine by reason
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    And Select reason filter
    And Apply filter
    Then Records should be filtered by reason

  @quarantine_filter_by_location
  Scenario: Filter quarantine by location
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    And Select location filter
    And Apply filter
    Then Records should be filtered by location

  @quarantine_filter_by_date
  Scenario: Filter quarantine by date range
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    And Set date range filter
    And Apply filter
    Then Records should be filtered by date range

  # ========================================
  # Exportacao
  # ========================================

  @quarantine_export
  Scenario: Export quarantine data to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Quarantine
    And Click on Save As button
    And Select CSV option from Save As menu
    Then CSV file should be downloaded
