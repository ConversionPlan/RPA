@Utilities
Feature: Utilities (Servicos de Utilidade)

  # Testes para a funcionalidade de Servicos de Utilidade
  # URL: /utilities/

  # ========================================
  # Navegacao Principal
  # ========================================

  @smoke_utilities
  Scenario: Navigate to Utilities
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    Then Utilities page should be displayed

  # ========================================
  # Upload Manual EPCIS/EDI
  # ========================================

  @manual_upload_epcis
  Scenario: Upload EPCIS XML file manually
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on Manual EPCIS XML Upload
    And Select EPCIS file to upload
    And Click on Upload button
    Then EPCIS file should be processed successfully

  @manual_upload_edi
  Scenario: Upload EDI XML file manually
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on Manual EPCIS XML Upload
    And Select EDI file to upload
    And Click on Upload button
    Then EDI file should be processed successfully

  # ========================================
  # Painel de Trocas Eletronicas
  # ========================================

  @electronic_exchanges
  Scenario: View Electronic Exchanges Dashboard
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on Electronic Exchanges Dashboard
    Then Electronic Exchanges Dashboard should be displayed

  @electronic_exchanges_received
  Scenario: View received electronic messages
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on Electronic Exchanges Dashboard
    And Click on Received tab
    Then Received messages should be displayed

  @electronic_exchanges_sent
  Scenario: View sent electronic messages
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on Electronic Exchanges Dashboard
    And Click on Sent tab
    Then Sent messages should be displayed

  @electronic_exchanges_filter
  Scenario: Filter electronic exchanges by date
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on Electronic Exchanges Dashboard
    And Set date filter
    And Apply filter
    Then Messages should be filtered by date

  @electronic_exchanges_details
  Scenario: View electronic exchange details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on Electronic Exchanges Dashboard
    And Click on first exchange record
    Then Exchange Details modal should be displayed

  # ========================================
  # Ferramenta VRS Manual
  # ========================================

  @vrs_manual_query
  Scenario: Perform manual VRS query
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on Manual VRS Query Tool
    And Enter product serial number
    And Click on Query button
    Then VRS query results should be displayed

  # ========================================
  # Busca de Licenca
  # ========================================

  @license_search
  Scenario: Search for licenses
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on License Search
    Then License Search page should be displayed

  @license_search_by_number
  Scenario: Search license by number
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on License Search
    And Enter license number
    And Click on Search button
    Then License search results should be displayed

  @license_search_by_partner
  Scenario: Search license by trading partner
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on License Search
    And Select trading partner
    And Click on Search button
    Then Licenses for partner should be displayed

  # ========================================
  # Tarefas com Falha de Autorizacao
  # ========================================

  @authorization_failed_tasks
  Scenario: View authorization failed tasks
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on Authorization Failed Tasks
    Then Authorization Failed Tasks page should be displayed

  @authorization_failed_retry
  Scenario: Retry authorization failed task
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Utilities
    And Click on Authorization Failed Tasks
    And Click on first failed task
    And Click on Retry button
    Then Task should be retried
