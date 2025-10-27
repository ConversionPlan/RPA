@Ignore
Feature: Performance Test

  Scenario: Auth Page Performance Tests
    Given User exists
    And Launching Chrome browser
    When Open Portal Login page https://demopharmacoltd.qa-test.tracktraceweb.com/auth
    And Perform Test on Auth https://demopharmacoltd.qa-test.tracktraceweb.com/auth

  Scenario: Dashboard Page Performance Tests
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Perform Test on Dashboard https://demopharmacoltd.qa-test.tracktraceweb.com/