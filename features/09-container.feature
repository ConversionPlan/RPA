@Container
Feature: Container Management
  Como um usuário do sistema
  Eu quero gerenciar containers de inventário
  Para controlar e rastrear os containers do estoque

  # ============================================================
  # CENÁRIO DE SMOKE TEST - Navegação básica
  # ============================================================

  @smoke_container
  Scenario: Navigate to Container Management
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Container Management
    Then End test
