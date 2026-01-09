@Ignore
Feature: Performance Test

  @skip
  Scenario: Auth Page Performance Tests
    Given User exists
    And Launching Chrome browser
    When Open Portal Login page https://qualityportal.qa-test.tracktraceweb.com/auth
    And Perform Test on Auth https://qualityportal.qa-test.tracktraceweb.com/auth

  @skip
  Scenario: Dashboard Page Performance Tests
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Perform Test on Dashboard https://qualityportal.qa-test.tracktraceweb.com/