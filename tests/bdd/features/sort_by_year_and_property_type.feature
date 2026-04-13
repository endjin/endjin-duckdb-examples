@unit
Feature: Sort by year and property type

  Scenario: Rows are sorted ascending by year then property type
    Given a dataset with the following rows
      | year:int | property_type:string | total_sales:int |
      |     2024 | T                    |               3 |
      |     2022 | D                    |               5 |
      |     2023 | S                    |               2 |
      |     2024 | D                    |               7 |
      |     2022 | S                    |               1 |
      |     2023 | D                    |               4 |
    When I sort by year and property type
    Then the resulting dataset should be in the following order
      | year:int | property_type:string | total_sales:int |
      |     2022 | D                    |               5 |
      |     2022 | S                    |               1 |
      |     2023 | D                    |               4 |
      |     2023 | S                    |               2 |
      |     2024 | D                    |               7 |
      |     2024 | T                    |               3 |
