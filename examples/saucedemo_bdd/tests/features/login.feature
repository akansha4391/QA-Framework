Feature: SauceDemo Login
  As a registered user
  I want to login to SauceDemo
  So that I can purchase items

  Scenario: Successful Login
    Given I am on the sauce demo login page
    When I login with valid credentials
    Then I should see the inventory page
