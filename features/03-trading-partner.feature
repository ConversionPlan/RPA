@Trading_Partners
Feature: Trading Partners

  # Cenário simplificado - apenas criar o Trading Partner básico (sem endereços)
  Scenario: Create a Vendor (Basic)
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Trading Partners
    And Click on Add - Trading Partner Page
    And Add Trading Partner Name
    And Add Trading Partner GS1 ID (GLN)
    And Add Trading Partner GS1 Company Prefix
    And Add Trading Partner GS1 ID (SGLN)
    And Click on Add
    Then Trading Partner should be created
    And End test

  # Cenário simplificado - apenas criar Customer básico (sem endereços)
  Scenario: Create a Customer (Basic)
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Trading Partners
    And Click on Add - Trading Partner Page
    And Add Trading Partner Name
    And Select Trading Partner Type as Customer
    And Add Trading Partner GS1 ID (GLN)
    And Add Trading Partner GS1 Company Prefix
    And Add Trading Partner GS1 ID (SGLN)
    And Click on Add
    Then Trading Partner should be created
    And End test
