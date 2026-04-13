@unit
Feature: Extract postcode area

  Scenario: Extract postcode area from full postcode
    Given a dataset with the following rows
      | postcode:string |
      | SW1A 2AA        |
      | M1 1AE          |
    When I extract the postcode area from the full postcode
    Then the resulting dataset should include the following rows
      | postcode_area:string |
      | SW1A                 |
      | M1                   |

  Scenario: Handle invalid postcodes correctly
    Given a dataset with the following rows
      | postcode:string |
      | SW1A2AA         |
      | EC1A1BB         |
    When I extract the postcode area from the full postcode
    Then the resulting dataset should include the following rows
      | postcode_area:string |
      | null                 |
      | null                 |

  Scenario: Handle empty or null postcodes correctly
    Given a dataset with the following rows
      | postcode:string |
      |                 |
      | null            |
    When I extract the postcode area from the full postcode
    Then the resulting dataset should include the following rows
      | postcode_area:string |
      | null                 |
      | null                 |
