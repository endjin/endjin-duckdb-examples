from behave import when, then
from common_steps import behave_table_to_duckdb_relation, compare_duckdb_relations_ordered
from data_wrangler import DataWrangler


@when('I sort by year and property type')
def step_when_sort_by_year_and_property_type(context):
    context.rel = DataWrangler.sort_by_year_and_property_type(context.rel)


@then('the resulting dataset should be in the following order')
def step_then_ordered(context):
    expected = behave_table_to_duckdb_relation(context.table)
    compare_duckdb_relations_ordered(expected, context.rel)
