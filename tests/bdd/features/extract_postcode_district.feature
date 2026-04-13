@unit
Feature: Extract postcode district

  Scenario: Extract postcode district from full postcode
    Given a dataset with the following rows
      | postcode:string |
      | SW1A 2AA        |
      | M1 1AE          |
      | EC1A 1BB        |
      | LS1 1BA         |
    When I extract the postcode district from the full postcode
    Then the resulting dataset should include the following rows
      | postcode_district:string |
      | SW1A                      |
      | M1                       |
      | EC1A                      |
      | LS1                      |

  Scenario: Handle postcodes with no numeric suffix in the district
    Given a dataset with the following rows
      | postcode:string |
      | B1 1BB          |
      | W1A 1AA         |
    When I extract the postcode district from the full postcode
    Then the resulting dataset should include the following rows
      | postcode_district:string |
      | B1                       |
      | W1A                       |

  Scenario: Handle empty or null postcodes correctly
    Given a dataset with the following rows
      | postcode:string |
      |                 |
      | null            |
    When I extract the postcode district from the full postcode
    Then the resulting dataset should include the following rows
      | postcode_district:string |
      | null                     |
      | null                     |
