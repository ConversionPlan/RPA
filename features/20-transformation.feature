@Transformation
Feature: Transformation (Transformacao)

  # Testes para a funcionalidade de Transformacao
  # URL: /transformation/

  # ========================================
  # Navegacao Principal
  # ========================================

  @smoke_transformation
  Scenario: Navigate to Transformation
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    Then Transformation page should be displayed

  # ========================================
  # Listagem e Visualizacao
  # ========================================

  @transformation_list
  Scenario: View transformation list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    Then Transformation table should be displayed
    And Transformation table should have columns
