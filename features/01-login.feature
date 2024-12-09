@Authentication
Feature: Portal Login

  Scenario: Login to Portal with valid parameters
    Given User exists
    And Launching Chrome browser
    When Open Portal Login page https://demopharmacoltd.qa-test.tracktraceweb.com/auth
    And  Enter Username rpa-user@tracktracerx.com
    And Click Next to Login
    And  Enter Password Rpa!1234
    And  click on the Login button
    Then User must login successfully
    And End test