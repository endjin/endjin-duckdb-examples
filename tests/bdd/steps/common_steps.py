import duckdb
import polars as pl
import polars.testing as pl_testing
from typing import Any


def behave_table_to_duckdb_relation(table: Any) -> duckdb.DuckDBPyRelation:
    """Convert a Behave table to a DuckDB Relation via Polars intermediary."""
    if ":" in table.headings[0]:
        df = _behave_table_to_polars_dataframe_with_explicit_schema(table)
    else:
        df = _behave_table_to_polars_dataframe_with_inferred_schema(table)
    return duckdb.sql("SELECT * FROM df")


def compare_duckdb_relations(expected: duckdb.DuckDBPyRelation, actual: duckdb.DuckDBPyRelation):
    """Compare two DuckDB Relations by converting to Polars and asserting equality."""
    expected_pl = expected.pl()
    actual_pl = actual.pl()
    cols = sorted(expected_pl.columns)
    expected_pl = expected_pl.select(cols).sort(by=cols)
    actual_pl = actual_pl.select(cols).sort(by=cols)
    pl_testing.assert_frame_equal(expected_pl, actual_pl, check_dtypes=False)


def compare_duckdb_relations_ordered(expected: duckdb.DuckDBPyRelation, actual: duckdb.DuckDBPyRelation):
    """Compare two DuckDB Relations preserving row order (for sort tests)."""
    expected_pl = expected.pl()
    actual_pl = actual.pl()
    cols = expected_pl.columns
    actual_pl = actual_pl.select(cols)
    pl_testing.assert_frame_equal(expected_pl, actual_pl, check_dtypes=False)


def _behave_table_to_polars_dataframe_with_explicit_schema(table: Any) -> pl.DataFrame:
    cols = [h.split(":") for h in table.headings]
    if any(len(c) != 2 for c in cols):
        raise ValueError("field_name:field_type expected in table headings")

    schema = {name: _string_to_polars_type(field_type) for name, field_type in cols}
    rows = [{name: (None if cell in ("", "null") else cell) for (name, _), cell in zip(cols, row.cells)} for row in table]

    if not rows:
        return pl.DataFrame(schema=schema)

    df = pl.DataFrame(rows)

    for name, field_type in cols:
        df = df.with_columns(
            pl.when(pl.col(name) == "nan")
              .then(None)
              .otherwise(pl.col(name))
              .alias(name)
        )

        if field_type.lower() == "date":
            df = df.with_columns(pl.col(name).str.to_date())
        elif field_type.lower().startswith("date("):
            format_str = (
                field_type.split("(")[1]
                .strip(")")
                .replace("yyyy", "%Y")
                .replace("MM", "%m")
                .replace("dd", "%d")
            )
            df = df.with_columns(pl.col(name).str.to_date(format=format_str))
        elif field_type.lower() in ["datetime", "timestamp"]:
            df = df.with_columns(
                pl.col(name).str.replace(" ", "T", literal=True).str.strptime(
                    pl.Datetime(time_zone='UTC'), format="%Y-%m-%dT%H:%M:%S%.f", strict=False
                )
            )
        elif schema[name] == pl.Boolean:
            df = df.with_columns(
                pl.when(pl.col(name).str.to_lowercase() == "true").then(True)
                .when(pl.col(name).str.to_lowercase() == "false").then(False)
                .otherwise(None).alias(name).cast(pl.Boolean)
            )
        elif schema[name] == pl.Decimal:
            df = df.with_columns(pl.col(name).cast(pl.Decimal(scale=2)))
        elif schema[name] is not None and schema[name] != pl.Object:
            df = df.with_columns(pl.col(name).cast(schema[name]))

    return df


def _behave_table_to_polars_dataframe_with_inferred_schema(table: Any) -> pl.DataFrame:
    headings = table.headings
    rows = [{headings[i]: cell for i, cell in enumerate(row.cells)} for row in table]
    for row in rows:
        for key, value in row.items():
            if value == "":
                row[key] = None
    return pl.DataFrame(rows)


def _string_to_polars_type(type_name: str):
    type_name_lower = type_name.lower()
    if type_name_lower.startswith("date"):
        return pl.Date

    type_map = {
        "integer": pl.Int64,
        "int": pl.Int64,
        "long": pl.Int64,
        "integer8": pl.Int8,
        "integer32": pl.Int32,
        "float": pl.Float64,
        "double": pl.Float64,
        "boolean": pl.Boolean,
        "bool": pl.Boolean,
        "timestamp": pl.Datetime(time_zone="UTC"),
        "string": pl.Utf8,
        "str": pl.Utf8,
        "object": pl.Object,
        "decimal": pl.Decimal,
    }
    return type_map.get(type_name_lower)
