@ErrorConsole
Feature: Error Console (Console de Erros)

  # Testes para a funcionalidade de Console de Erros
  # URL: /error_console/

  # ========================================
  # Navegacao Principal
  # ========================================

  @smoke_error_console
  Scenario: Navigate to Error Console
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    Then Error Console page should be displayed

  # ========================================
  # Processos em Segundo Plano
  # ========================================

  @background_tasks_view
  Scenario: View background tasks
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Background Tasks
    Then Background Tasks page should be displayed
    And Background Tasks table should have columns

  @background_tasks_details
  Scenario: View background task details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Background Tasks
    And Click on first background task
    Then Task Details modal should be displayed
    And Task Details should show execution information

  @background_tasks_filter_status
  Scenario: Filter background tasks by status
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Background Tasks
    And Select status filter Failed
    And Apply filter
    Then Only failed tasks should be displayed

  @background_tasks_retry
  Scenario: Retry failed background task
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Background Tasks
    And Filter by failed status
    And Click on first failed task
    And Click on Retry button
    Then Task should be queued for retry

  # ========================================
  # Console de Erros
  # ========================================

  @error_console_view
  Scenario: View error console messages
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Error Console Messages
    Then Error Console Messages page should be displayed
    And Error messages table should have columns

  @error_console_details
  Scenario: View error message details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Error Console Messages
    And Click on first error message
    Then Error Details modal should be displayed
    And Error Details should show full error information

  @error_console_filter_type
  Scenario: Filter errors by type
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Error Console Messages
    And Select error type filter
    And Apply filter
    Then Errors should be filtered by type

  @error_console_filter_date
  Scenario: Filter errors by date range
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Error Console Messages
    And Set date range filter
    And Apply filter
    Then Errors should be filtered by date

  @error_console_acknowledge
  Scenario: Acknowledge error message
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Error Console Messages
    And Click on first error message
    And Click on Acknowledge button
    Then Error should be marked as acknowledged

  @error_console_bulk_acknowledge
  Scenario: Bulk acknowledge error messages
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Error Console Messages
    And Select multiple error messages
    And Click on Bulk Acknowledge button
    Then All selected errors should be acknowledged

  # ========================================
  # Exportacao
  # ========================================

  @error_console_export
  Scenario: Export error messages to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Error Console Messages
    And Click on Save As button
    And Select CSV option
    Then CSV file should be downloaded

  @background_tasks_export
  Scenario: Export background tasks to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Error Console
    And Click on Background Tasks
    And Click on Save As button
    And Select CSV option
    Then CSV file should be downloaded
