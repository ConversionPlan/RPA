@ReturnManager
Feature: Return Manager (Gerente de Retorno)

  # Testes para a funcionalidade de Gerente de Retorno
  # URL: /return_manager/
  # Inclui: RMAs, Devoluções e Serviços VRS

  # ========================================
  # RMAs - Return Merchandise Authorization
  # ========================================

  @smoke_return_manager
  Scenario: Navigate to Return Manager
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Return Manager
    Then Return Manager page should be displayed

  @rma_create
  Scenario: Create a new RMA
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Return Manager
    And Click on Create RMA
    And Fill RMA customer information
    And Fill RMA product information
    And Fill RMA reason for return
    And Click on Save RMA
    Then RMA should be created successfully

  @rma_to_approve
  Scenario: View RMAs pending approval
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Return Manager
    And Click on RMAs to Approve
    Then RMAs to Approve list should be displayed
    And RMAs to Approve table should have columns

  @rma_to_receive
  Scenario: View RMAs pending receipt
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Return Manager
    And Click on RMAs to Receive
    Then RMAs to Receive list should be displayed
    And RMAs to Receive table should have columns

  @rma_all
  Scenario: View all RMAs
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Return Manager
    And Click on All RMAs
    Then All RMAs list should be displayed
    And All RMAs table should have columns

  # ========================================
  # Devoluções
  # ========================================

  @return_suspended_sessions
  Scenario: View suspended return sessions
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Return Manager
    And Click on Suspended Return Sessions
    Then Suspended Return Sessions list should be displayed
    And Suspended Return Sessions table should have columns

  @return_events_list
  Scenario: View return events list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Return Manager
    And Click on Return Events List
    Then Return Events List should be displayed
    And Return Events table should have columns

  # ========================================
  # Serviços VRS do Fabricante
  # ========================================

  @vrs_return_requests
  Scenario: View VRS return requests
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Return Manager
    And Click on View Return Requests
    Then VRS Return Requests list should be displayed
    And VRS Return Requests table should have columns

  @vrs_gln_allow_deny
  Scenario: Manage GLN Allow/Deny list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Return Manager
    And Click on GLN Allow Deny List
    Then GLN Allow Deny List should be displayed

