@unit
Feature: Rename old new

  Scenario: Rename the old_new column including handling null values
    Given a dataset with the following rows
      | id:int | old_new:string |
      |      1 | Y              |
      |      2 | N              |
      |      3 | Y              |
      |      4 | N              |
      |      5 | null           |
    When I rename old_new values
    Then the resulting dataset should include the following rows
      | id:int | old_new:string |
      |      1 | New            |
      |      2 | Old            |
      |      3 | New            |
      |      4 | Old            |
      |      5 | null           |
