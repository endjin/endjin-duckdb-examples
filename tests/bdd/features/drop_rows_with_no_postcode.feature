@unit
Feature: Drop rows with no postcode

  Scenario: Drop some rows with no postcode
    Given a dataset with the following rows
      | transaction_id:string | price:float | date:date  | postcode:string |
      |                     1 |    500000.0 | 2026-01-01 | SW1A 2AA        |
      |                     2 |    300000.0 | 2026-01-02 |                 |
    When I drop rows with no postcode
    Then the resulting dataset should include the following rows
      | transaction_id:string | postcode:string |
      |                     1 | SW1A 2AA        |

  Scenario: Drop no rows when all postcodes are present
    Given a dataset with the following rows
      | transaction_id:string | price:float | date:date  | postcode:string |
      |                     1 |    500000.0 | 2026-01-01 | SW1A 2AA        |
      |                     2 |    300000.0 | 2026-01-02 | M1 1AE          |
    When I drop rows with no postcode
    Then the resulting dataset should include the following rows
      | transaction_id:string | postcode:string |
      |                     1 | SW1A 2AA        |
      |                     2 | M1 1AE          |
