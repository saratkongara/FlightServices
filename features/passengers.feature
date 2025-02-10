Feature: Passengers

  In order to validate passengers API
  As a tester
  I want to make sure that everything works as expected

  Scenario: Get passenger details
    Given I make a GET request to http://127.0.0.1:9000/flightServices/passengers/1/
    When I send the request
    Then I expect response status to be 200
