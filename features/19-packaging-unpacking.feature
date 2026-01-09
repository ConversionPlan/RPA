@PackagingUnpacking
Feature: Packaging and Unpacking (Embalagem e Desempacotamento)

  # Testes para as funcionalidades de Embalagem e Desempacotamento
  # URLs: /packaging/ e /unpacking/

  # ========================================
  # EMBALAGEM (Packaging)
  # ========================================

  @smoke_packaging
  Scenario: Navigate to Packaging
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Packaging
    Then Packaging page should be displayed

  @packaging_list
  Scenario: View packaging sessions list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Packaging
    Then Packaging sessions table should be displayed
    And Packaging table should have columns

  @packaging_create_session
  Scenario: Create new packaging session
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Packaging
    And Click on New Packaging Session button
    And Select packaging location
    And Select container type
    And Click on Start Session
    Then Packaging session should be created

  @packaging_add_items
  Scenario: Add items to package
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Packaging
    And Click on New Packaging Session button
    And Select packaging location
    And Select container type
    And Click on Start Session
    And Scan item serial numbers
    And Click on Add to Package
    Then Items should be added to package

  @packaging_close_container
  Scenario: Close packaging container
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Packaging
    And Click on active packaging session
    And Click on Close Container button
    And Enter container serial number
    And Confirm close
    Then Container should be closed successfully

  @packaging_print_label
  Scenario: Print package label
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Packaging
    And Click on completed package
    And Click on Print Label button
    Then Label should be generated for printing

  @packaging_view_history
  Scenario: View packaging history
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Packaging
    And Click on first packaging record
    Then Packaging Details modal should be displayed
    And Packaging history should show all items

  # ========================================
  # DESEMPACOTAMENTO (Unpacking)
  # ========================================

  @smoke_unpacking
  Scenario: Navigate to Unpacking
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Unpacking
    Then Unpacking page should be displayed

  @unpacking_list
  Scenario: View unpacking sessions list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Unpacking
    Then Unpacking sessions table should be displayed
    And Unpacking table should have columns

  @unpacking_create_session
  Scenario: Create new unpacking session
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Unpacking
    And Click on New Unpacking Session button
    And Select unpacking location
    And Click on Start Session
    Then Unpacking session should be created

  @unpacking_scan_container
  Scenario: Scan container for unpacking
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Unpacking
    And Click on New Unpacking Session button
    And Select unpacking location
    And Click on Start Session
    And Scan container serial number
    Then Container contents should be displayed

  @unpacking_remove_items
  Scenario: Remove items from container
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Unpacking
    And Click on active unpacking session
    And Select items to remove
    And Click on Remove from Container
    Then Items should be removed from container

  @unpacking_complete
  Scenario: Complete unpacking session
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Unpacking
    And Click on active unpacking session
    And Remove all items from container
    And Click on Complete Unpacking button
    Then Unpacking should be completed successfully

  @unpacking_partial
  Scenario: Partial unpacking
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Unpacking
    And Click on active unpacking session
    And Select some items to remove
    And Click on Remove from Container
    And Click on Save and Close
    Then Partial unpacking should be saved

  # ========================================
  # Pesquisa e Filtros
  # ========================================

  @packaging_search
  Scenario: Search packaging by container serial
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Packaging
    And Search by container serial number
    Then Search results should be filtered

  @unpacking_search
  Scenario: Search unpacking by container serial
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Unpacking
    And Search by container serial number
    Then Search results should be filtered

  # ========================================
  # Exportacao
  # ========================================

  @packaging_export
  Scenario: Export packaging data to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Packaging
    And Click on Save As button
    And Select CSV option
    Then CSV file should be downloaded

  @unpacking_export
  Scenario: Export unpacking data to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Unpacking
    And Click on Save As button
    And Select CSV option
    Then CSV file should be downloaded
