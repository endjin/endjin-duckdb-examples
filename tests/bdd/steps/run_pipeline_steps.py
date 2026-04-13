import os
from behave import given, when, then
from data_wrangler import DataWrangler


TEST_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "test_data")


@given('land registry CSV files exist in the test data folder')
def step_given_test_data_exists(context):
    csv_files = [f for f in os.listdir(TEST_DATA_FOLDER) if f.endswith(".csv")]
    assert csv_files, f"No CSV files found in {TEST_DATA_FOLDER}"
    context.test_data_folder = TEST_DATA_FOLDER


@when('I run the pipeline')
def step_when_run_pipeline(context):
    rel = DataWrangler.run_pipeline(context.test_data_folder)
    context.result = rel.pl()


@then('the result should be a non-empty summary DataFrame')
def step_then_non_empty(context):
    assert context.result is not None
    assert len(context.result) > 0, "Pipeline returned an empty DataFrame"


@then('the summary should contain the columns {columns}')
def step_then_columns(context, columns):
    expected = [c.strip() for c in columns.split(",")]
    actual = context.result.columns
    missing = [c for c in expected if c not in actual]
    assert not missing, f"Missing columns: {missing}"


@then('all property_type values should be from the renamed set {values}')
def step_then_property_type_values(context, values):
    allowed = {v.strip() for v in values.split(",")}
    actual = set(context.result["property_type"].drop_nulls().to_list())
    unexpected = actual - allowed
    assert not unexpected, f"Unexpected property_type values: {unexpected}"


@then('all year values should be positive integers')
def step_then_year_positive(context):
    assert (context.result["year"] > 0).all(), "Found non-positive year values"


@then('all total_sales values should be greater than zero')
def step_then_total_sales_positive(context):
    assert (context.result["total_sales"] > 0).all(), "Found zero total_sales"


@then('all max_price values should be greater than or equal to min_price')
def step_then_max_gte_min(context):
    assert (context.result["max_price"] >= context.result["min_price"]).all(), \
        "Found rows where max_price < min_price"
