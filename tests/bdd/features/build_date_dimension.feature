@unit
Feature: Build a date dimension

  Scenario: Date dimension is built correctly for a given date range
    Given the date dimension start date is '2026-03-01' and the end date is '2026-03-03'
    When I build the date dimension
    Then the date dimension should include the following dates
      | date:date  | year:int | month:int | day:int | weekday:int | is_weekend:bool | is_leap_year:bool | month_name:string | day_name:string |
      | 2026-03-01 |     2026 |         3 |       1 |           7 | true            | false             | March             | Sunday          |
      | 2026-03-02 |     2026 |         3 |       2 |           1 | false           | false             | March             | Monday          |
      | 2026-03-03 |     2026 |         3 |       3 |           2 | false           | false             | March             | Tuesday         |

  Scenario: Date dimension handles leap years correctly
    Given the date dimension start date is '2020-02-27' and the end date is '2020-03-01'
    When I build the date dimension
    Then the date dimension should include the following dates
      | date:date  | year:int | month:int | day:int | weekday:int | is_weekend:bool | is_leap_year:bool | month_name:string | day_name:string |
      | 2020-02-27 |     2020 |         2 |      27 |           4 | false           | true              | February          | Thursday        |
      | 2020-02-28 |     2020 |         2 |      28 |           5 | false           | true              | February          | Friday          |
      | 2020-02-29 |     2020 |         2 |      29 |           6 | true            | true              | February          | Saturday        |
      | 2020-03-01 |     2020 |         3 |       1 |           7 | true            | true              | March             | Sunday          |
