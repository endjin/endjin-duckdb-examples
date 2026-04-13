@unit
Feature: Drop rows with no date

  Scenario: Drop some rows with no date
    Given a dataset with the following rows
      | transaction_id:string | price:float | date:date  | postcode:string |
      |                     1 |    500000.0 | 2026-01-01 | SW1A 2AA        |
      |                     2 |    300000.0 |             | M1 1AE          |
    When I drop rows with no date
    Then the resulting dataset should include the following rows
      | transaction_id:string | date:date  |
      |                     1 | 2026-01-01 |

  Scenario: Drop no rows when all dates are present
    Given a dataset with the following rows
      | transaction_id:string | price:float | date:date  | postcode:string |
      |                     1 |    500000.0 | 2026-01-01 | SW1A 2AA        |
      |                     2 |    300000.0 | 2026-01-02 | M1 1AE          |
    When I drop rows with no date
    Then the resulting dataset should include the following rows
      | transaction_id:string | date:date  |
      |                     1 | 2026-01-01 |
      |                     2 | 2026-01-02 |
