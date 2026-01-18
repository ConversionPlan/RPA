@Utilities
Feature: Utilities (Servicos de Utilidade)

  # Testes para a funcionalidade de Servicos de Utilidade
  # URL: /utilities/
  #
  # OTIMIZACOES IMPLEMENTADAS:
  # - Background: Login e navegacao executados uma vez por cenario
  # - Navegacao direta via URL (3x mais rapido que menu)
  # - Tags para execucao paralela por grupo funcional

  Background:
    Given User exists
    And Is Logged In
    And User is on Utilities page

  # ========================================
  # Navegacao Principal
  # ========================================

  @smoke_utilities @parallel_group_1
  Scenario: Navigate to Utilities
    Then Utilities page should be displayed

  # ========================================
  # Upload Manual EPCIS/EDI
  # ========================================

  @manual_upload_epcis @parallel_group_1 @skip
  Scenario: Upload EPCIS XML file manually
    When Click on Manual EPCIS XML Upload
    And Select EPCIS file to upload
    And Click on Upload button
    Then EPCIS file should be processed successfully

  @manual_upload_edi @parallel_group_1 @skip
  Scenario: Upload EDI XML file manually
    When Click on Manual EPCIS XML Upload
    And Select EDI file to upload
    And Click on Upload button
    Then EDI file should be processed successfully

  # ========================================
  # Painel de Trocas Eletronicas
  # ========================================

  @electronic_exchanges @parallel_group_2
  Scenario: View Electronic Exchanges Dashboard
    When Click on Electronic Exchanges Dashboard
    Then Electronic Exchanges Dashboard should be displayed

  @electronic_exchanges_received @parallel_group_2
  Scenario: View received electronic messages
    When Click on Electronic Exchanges Dashboard
    And Click on Received tab
    Then Received messages should be displayed

  @electronic_exchanges_sent @parallel_group_2
  Scenario: View sent electronic messages
    When Click on Electronic Exchanges Dashboard
    And Click on Sent tab
    Then Sent messages should be displayed

  @electronic_exchanges_filter @parallel_group_2
  Scenario: Filter electronic exchanges by date
    When Click on Electronic Exchanges Dashboard
    And Set date filter
    And Apply filter
    Then Messages should be filtered by date

  @electronic_exchanges_details @parallel_group_2
  Scenario: View electronic exchange details
    When Click on Electronic Exchanges Dashboard
    And Click on first exchange record
    Then Exchange Details modal should be displayed

  # ========================================
  # Ferramenta VRS Manual
  # ========================================

  @vrs_manual_query @parallel_group_3 @skip
  Scenario: Perform manual VRS query
    When Click on Manual VRS Query Tool
    And Enter product serial number
    And Click on Query button
    Then VRS query results should be displayed

  # ========================================
  # Busca de Licenca
  # ========================================

  @license_search @parallel_group_3
  Scenario: Search for licenses
    When Click on License Search
    Then License Search page should be displayed

  @license_search_by_number @parallel_group_3
  Scenario: Search license by number
    When Click on License Search
    And Enter license number
    And Click on Search button
    Then License search results should be displayed

  @license_search_by_partner @parallel_group_3
  Scenario: Search license by trading partner
    When Click on License Search
    And Select trading partner
    And Click on Search button
    Then Licenses for partner should be displayed

  # ========================================
  # Tarefas com Falha de Autorizacao
  # ========================================

  @authorization_failed_tasks @parallel_group_4
  Scenario: View authorization failed tasks
    When Click on Authorization Failed Tasks
    Then Authorization Failed Tasks page should be displayed

  @authorization_failed_retry @parallel_group_4
  Scenario: Retry authorization failed task
    When Click on Authorization Failed Tasks
    And Click on first failed task
    And Click on Retry button
    Then Task should be retried
