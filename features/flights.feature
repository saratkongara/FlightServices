Feature: Flights

  In order to validate flights API
  As a tester
  I want to make sure that everything works as expected

  Scenario: Get flight details
    Given I authenticate as user apiuser1
    And I make a GET request to http://127.0.0.1:9000/flightServices/flights/1/
    When I send the request
    Then I expect response status to be 200
