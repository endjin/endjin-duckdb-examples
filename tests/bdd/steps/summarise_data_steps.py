from behave import when
from data_wrangler import DataWrangler


@when('I summarise the data')
def step_when_summarise_data(context):
    context.rel = DataWrangler.summarise_by_year_and_property_type(context.rel)
