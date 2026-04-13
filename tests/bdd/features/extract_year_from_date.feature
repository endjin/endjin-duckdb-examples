@unit
Feature: Extract year from date

  Scenario: Extract year from a date column
    Given a dataset with the following rows
      | id:int | date:date  |
      |      1 | 2022-03-15 |
      |      2 | 2023-07-04 |
      |      3 | 2024-11-28 |
    When I extract the year from the date
    Then the resulting dataset should include the following rows
      | id:int | year:int |
      |      1 |     2022 |
      |      2 |     2023 |
      |      3 |     2024 |

  Scenario: Multiple sales in the same year produce the same year value
    Given a dataset with the following rows
      | id:int | date:date  |
      |      1 | 2024-01-10 |
      |      2 | 2024-06-22 |
      |      3 | 2024-12-31 |
    When I extract the year from the date
    Then the resulting dataset should include the following rows
      | id:int | year:int |
      |      1 |     2024 |
      |      2 |     2024 |
      |      3 |     2024 |
