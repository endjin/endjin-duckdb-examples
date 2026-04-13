@unit
Feature: Rename property type

  Scenario: Rename property types including handling null values
    Given a dataset with the following rows
      | id:int | property_type:string |
      |      1 | D                    |
      |      2 | S                    |
      |      3 | O                    |
      |      4 | T                    |
      |      5 | null                 |
    When I rename property types
    Then the resulting dataset should include the following rows
      | id:int | property_type:string |
      |      1 | Detached             |
      |      2 | Semi-Detached        |
      |      3 | Other                |
      |      4 | Terraced             |
      |      5 | null                 |
