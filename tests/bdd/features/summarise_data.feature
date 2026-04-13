@unit
Feature: Summarise data

  Scenario: Summarise sales by year and property type
    Given a dataset with the following rows
      | id:string | year:int | property_type:string | town_city:string | county:string      | price:integer |
      | 1         |     2024 | D                    | LONDON           | GREATER LONDON     |        500000 |
      | 2         |     2024 | D                    | LONDON           | GREATER LONDON     |        300000 |
      | 3         |     2024 | S                    | LONDON           | GREATER LONDON     |        250000 |
      | 4         |     2024 | T                    | LONDON           | GREATER LONDON     |        175000 |
      | 5         |     2024 | F                    | MANCHESTER       | GREATER MANCHESTER |        180000 |
      | 6         |     2024 | F                    | MANCHESTER       | GREATER MANCHESTER |        195000 |
      | 7         |     2024 | S                    | MANCHESTER       | GREATER MANCHESTER |        220000 |
      | 8         |     2024 | D                    | LEEDS            | WEST YORKSHIRE     |        310000 |
      | 9         |     2024 | D                    | LEEDS            | WEST YORKSHIRE     |        340000 |
      | 10        |     2024 | D                    | LEEDS            | WEST YORKSHIRE     |        280000 |
      | 11        |     2023 | D                    | LONDON           | GREATER LONDON     |        400000 |
      | 12        |     2023 | D                    | LONDON           | GREATER LONDON     |        450000 |
      | 13        |     2023 | S                    | LONDON           | GREATER LONDON     |        230000 |
      | 14        |     2023 | T                    | MANCHESTER       | GREATER MANCHESTER |        160000 |
      | 15        |     2023 | F                    | MANCHESTER       | GREATER MANCHESTER |        155000 |
      | 16        |     2023 | D                    | LEEDS            | WEST YORKSHIRE     |        295000 |
      | 17        |     2022 | D                    | LONDON           | GREATER LONDON     |        480000 |
      | 18        |     2022 | S                    | LONDON           | GREATER LONDON     |        210000 |
      | 19        |     2022 | D                    | MANCHESTER       | GREATER MANCHESTER |        265000 |
      | 20        |     2022 | T                    | LEEDS            | WEST YORKSHIRE     |        145000 |
    When I summarise the data
    Then the resulting dataset should include the following rows
      | year:int | property_type:string | total_sales:int | max_price:int | min_price:int | median_price:float |
      |     2024 | D                    |               5 |        500000 |        280000 |           310000.0 |
      |     2024 | S                    |               2 |        250000 |        220000 |           235000.0 |
      |     2024 | T                    |               1 |        175000 |        175000 |           175000.0 |
      |     2024 | F                    |               2 |        195000 |        180000 |           187500.0 |
      |     2023 | D                    |               3 |        450000 |        295000 |           400000.0 |
      |     2023 | S                    |               1 |        230000 |        230000 |           230000.0 |
      |     2023 | T                    |               1 |        160000 |        160000 |           160000.0 |
      |     2023 | F                    |               1 |        155000 |        155000 |           155000.0 |
      |     2022 | D                    |               2 |        480000 |        265000 |           372500.0 |
      |     2022 | S                    |               1 |        210000 |        210000 |           210000.0 |
      |     2022 | T                    |               1 |        145000 |        145000 |           145000.0 |
