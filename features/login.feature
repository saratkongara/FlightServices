Feature: Authentication

  In order to validate authentication API
  As a tester
  I want to make sure that everything works as expected

  Scenario: Successful Login
    Given I make a POST request to http://127.0.0.1:9000/api-token-auth/
    And I set header Content-Type to application/json
    And I set body to
      """
      {
        "username": "apiuser1",
        "password": "secret123$"
      }
      """
    When I send the request
    Then I expect response status to be 200
    And I store JSON response at token as user_token

