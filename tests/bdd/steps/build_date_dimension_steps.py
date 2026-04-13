from datetime import date

from behave import given, when, then
from common_steps import behave_table_to_duckdb_relation, compare_duckdb_relations
from data_wrangler import DataWrangler


@given("the date dimension start date is '{start_date}' and the end date is '{end_date}'")
def step_given_date_range(context, start_date, end_date):
    context.start_date = date.fromisoformat(start_date)
    context.end_date = date.fromisoformat(end_date)


@when('I build the date dimension')
def step_when_build_date_dimension(context):
    context.rel = DataWrangler.build_date_dimension_table(context.start_date, context.end_date)


@then('the date dimension should include the following dates')
def step_then_date_dimension(context):
    expected = behave_table_to_duckdb_relation(context.table)
    compare_duckdb_relations(expected, context.rel)
