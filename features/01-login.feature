@Authentication
Feature: Portal Login

  Scenario: Login to Portal with valid parameters
    Given User exists
    And Launching Chrome browser
    When Open Portal Login page https://qualityportal.qa-test.tracktraceweb.com/auth
    And Enter Username teste@teste.com
    And Click Next to Login
    And Enter Password Mudar@12345342
    And click on the Login button
    Then User must login successfully
    And End test