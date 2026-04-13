from behave import when
from data_wrangler import DataWrangler


@when('I rename property types')
def step_when_rename_property_types(context):
    context.rel = DataWrangler.rename_property_type(context.rel)
