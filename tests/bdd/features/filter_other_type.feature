@unit
Feature: Filter other type

  Scenario: Filter out rows with 'Other' property type
    Given a dataset with the following rows
      | property_type:string | price:float |
      | O                    |    500000.0 |
      | D                    |    300000.0 |
      | O                    |    100000.0 |
    When I filter out rows where property_type is other
    Then the resulting dataset should include the following rows
      | property_type:string | price:float |
      | D                    |    300000.0 |

  Scenario: Filter out no rows when 'Other' property type is not present
    Given a dataset with the following rows
      | property_type:string | price:float |
      | D                    |    500000.0 |
      | D                    |    300000.0 |
      | D                    |    100000.0 |
    When I filter out rows where property_type is other
    Then the resulting dataset should include the following rows
      | property_type:string | price:float |
      | D                    |    500000.0 |
      | D                    |    300000.0 |
      | D                    |    100000.0 |
