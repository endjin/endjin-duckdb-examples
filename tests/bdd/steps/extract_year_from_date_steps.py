from behave import when
from data_wrangler import DataWrangler


@when('I extract the year from the date')
def step_when_extract_year_from_date(context):
    context.rel = DataWrangler.extract_year_from_date(context.rel)
