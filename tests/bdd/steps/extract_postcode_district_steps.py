from behave import when
from data_wrangler import DataWrangler


@when('I extract the postcode district from the full postcode')
def step_when_extract_postcode_district(context):
    context.rel = DataWrangler.extract_postcode_district(context.rel)
