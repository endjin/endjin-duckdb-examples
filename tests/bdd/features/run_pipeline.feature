@e2e
Feature: Run data wrangler pipeline end-to-end

  Scenario: Load, transform and summarise Land Registry data from CSV files
    Given land registry CSV files exist in the test data folder
    When I run the pipeline
    Then the result should be a non-empty summary DataFrame
    And the summary should contain the columns year, property_type, total_sales, max_price, min_price, median_price
    And all property_type values should be from the renamed set Detached, Semi-Detached, Terraced, Flat
    And all year values should be positive integers
    And all total_sales values should be greater than zero
    And all max_price values should be greater than or equal to min_price
