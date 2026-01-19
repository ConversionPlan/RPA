@Smoke
Feature: Smoke Tests - Testes Simplificados

  # Teste 1: Login básico
  @smoke_login
  Scenario: Smoke Test - Login
    Given User exists
    And Is Logged In
    When Open dashboard page
    Then End test

  # Teste 2: Navegação para Products
  @smoke_product
  Scenario: Smoke Test - Navigate to Products
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Product Management
    Then End test

  # Teste 3: Navegação para Trading Partners
  @smoke_trading_partner
  Scenario: Smoke Test - Navigate to Trading Partners
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Trading Partners
    Then End test

  # Teste 4: Navegação para Inbound
  @smoke_inbound
  Scenario: Smoke Test - Navigate to Inbound
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Inbound
    Then End test

  # Teste 5: Navegação para Return Manager
  @smoke_return_manager
  Scenario: Smoke Test - Navigate to Return Manager
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Return Manager
    Then Return Manager page should be displayed
