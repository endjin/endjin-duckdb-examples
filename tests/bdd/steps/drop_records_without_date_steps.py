from behave import when
from data_wrangler import DataWrangler


@when('I drop rows with no date')
def step_when_drop_rows_with_no_date(context):
    context.rel = DataWrangler.drop_records_without_date(context.rel)
