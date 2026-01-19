@Outbound
Feature: Outbound

  # Cenário simplificado - apenas navegação

  @smoke_outbound
  Scenario: Navigate to Outbound
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Outbound
    Then End test
