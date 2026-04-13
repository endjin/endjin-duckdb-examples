@unit
Feature: Rename duration

  Scenario: Extract postcode area from full postcode
    Given a dataset with the following rows
      | id:int | duration:string |
      |      1 | F               |
      |      2 | L               |
      |      3 | U               |
      |      4 | L               |
      |      5 | null            |
    When I rename durations
    Then the resulting dataset should include the following rows
      | id:int | duration:string |
      |      1 | Freehold        |
      |      2 | Leasehold       |
      |      3 | Unknown         |
      |      4 | Leasehold       |
      |      5 | null            |
