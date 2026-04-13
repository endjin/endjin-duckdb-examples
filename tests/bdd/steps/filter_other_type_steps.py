from behave import given, when, then
from common_steps import behave_table_to_duckdb_relation, compare_duckdb_relations
from data_wrangler import DataWrangler


@given('a dataset with the following rows')
def step_given_dataset(context):
    context.rel = behave_table_to_duckdb_relation(context.table)


@when('I filter out rows where property_type is other')
def step_when_filter_other(context):
    context.rel = DataWrangler.filter_other_property_types(context.rel)


@then('the resulting dataset should include the following rows')
def step_then_resulting_dataset(context):
    expected = behave_table_to_duckdb_relation(context.table)
    compare_duckdb_relations(expected, context.rel)
