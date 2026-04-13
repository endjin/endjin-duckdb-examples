from behave import when
from data_wrangler import DataWrangler


@when('I rename old_new values')
def step_when_rename_old_new(context):
    context.rel = DataWrangler.rename_old_new(context.rel)
