import duckdb
from datetime import date
from functools import reduce

RelationType = duckdb.DuckDBPyRelation


class DataWrangler:

    COLUMN_NAMES = [
        "id", "price", "date", "postcode", "property_type",
        "old_new", "duration", "paon", "saon", "street",
        "locality", "town_city", "district", "county",
        "ppd_category", "record_type",
    ]

    @staticmethod
    def load_data(data_folder: str) -> RelationType:
        """
        Reads all pp-*.csv files in data_folder, naming columns per the Land
        Registry positional schema and casting price/date to their native types.
        """
        return duckdb.sql(f"""
            SELECT
                column00 AS id,
                CAST(column01 AS BIGINT) AS price,
                strptime(column02, '%Y-%m-%d %H:%M')::DATE AS date,
                NULLIF(column03, '') AS postcode,
                column04 AS property_type,
                column05 AS old_new,
                column06 AS duration,
                column07 AS paon,
                column08 AS saon,
                column09 AS street,
                column10 AS locality,
                column11 AS town_city,
                column12 AS district,
                column13 AS county,
                column14 AS ppd_category,
                column15 AS record_type
            FROM read_csv(
                '{data_folder}/pp-*.csv',
                header = false,
                all_varchar = true
            )
        """)

    @classmethod
    def run_pipeline(cls, data_folder: str) -> RelationType:
        """
        Loads all CSVs from data_folder and runs the full transformation and
        summarisation pipeline.
        """
        steps = [
            cls.drop_records_without_postcode,
            cls.drop_records_without_date,
            cls.filter_other_property_types,
            cls.extract_year_from_date,
            cls.rename_property_type,
            cls.rename_duration,
            cls.rename_old_new,
            cls.extract_postcode_area,
            cls.summarise_by_year_and_property_type,
            cls.sort_by_year_and_property_type,
        ]
        return reduce(lambda rel, fn: fn(rel), steps, cls.load_data(data_folder))

    @staticmethod
    def filter_other_property_types(rel: RelationType) -> RelationType:
        """Filters out rows where property_type is 'O' (Other)."""
        return duckdb.sql("SELECT * FROM rel WHERE property_type != 'O'")

    @staticmethod
    def extract_year_from_date(rel: RelationType) -> RelationType:
        """Extracts the year from the 'date' column as a new 'year' column."""
        return duckdb.sql("SELECT *, EXTRACT(YEAR FROM date)::INTEGER AS year FROM rel")

    @staticmethod
    def build_date_dimension_table(start_date: date, end_date: date) -> RelationType:
        """
        Builds a date dimension table for the inclusive range [start_date, end_date].
        """
        return duckdb.sql(f"""
            SELECT
                d::DATE AS date,
                EXTRACT(YEAR FROM d)::INTEGER AS year,
                EXTRACT(MONTH FROM d)::INTEGER AS month,
                EXTRACT(DAY FROM d)::INTEGER AS day,
                isodow(d)::INTEGER AS weekday,
                (isodow(d) >= 6) AS is_weekend,
                (EXTRACT(YEAR FROM d) % 4 = 0
                    AND (EXTRACT(YEAR FROM d) % 100 != 0
                         OR EXTRACT(YEAR FROM d) % 400 = 0)) AS is_leap_year,
                monthname(d) AS month_name,
                dayname(d) AS day_name
            FROM generate_series('{start_date}'::DATE, '{end_date}'::DATE, INTERVAL 1 DAY) AS t(d)
        """)

    @staticmethod
    def extract_postcode_area(rel: RelationType) -> RelationType:
        """
        Extracts the postcode area (outward code) from the 'postcode' column.
        Returns null for any postcode that does not match the standard UK format.
        """
        return duckdb.sql("""
            SELECT *,
                NULLIF(
                    regexp_extract(postcode, '^([A-Z]{1,2}[0-9R][0-9A-Z]?) [0-9][ABD-HJLNP-UW-Z]{2}$', 1),
                    ''
                ) AS postcode_area
            FROM rel
        """)

    @staticmethod
    def extract_postcode_district(rel: RelationType) -> RelationType:
        """
        Extracts the postcode district from the 'postcode' column.
        """
        return duckdb.sql(r"""
            SELECT *,
                NULLIF(
                    regexp_extract(postcode, '^([A-Z]{1,2}[0-9R][0-9A-Z]?)\s', 1),
                    ''
                ) AS postcode_district
            FROM rel
        """)

    @staticmethod
    def drop_records_without_postcode(rel: RelationType) -> RelationType:
        """Drops records where the 'postcode' column is null or empty."""
        return duckdb.sql("SELECT * FROM rel WHERE postcode IS NOT NULL AND postcode != ''")

    @staticmethod
    def drop_records_without_date(rel: RelationType) -> RelationType:
        """Drops records where the 'date' column is null."""
        return duckdb.sql("SELECT * FROM rel WHERE date IS NOT NULL")

    @staticmethod
    def rename_property_type(rel: RelationType) -> RelationType:
        """Renames property_type codes to descriptive labels."""
        return duckdb.sql("""
            SELECT * REPLACE (
                CASE property_type
                    WHEN 'D' THEN 'Detached'
                    WHEN 'S' THEN 'Semi-Detached'
                    WHEN 'T' THEN 'Terraced'
                    WHEN 'F' THEN 'Flat'
                    WHEN 'O' THEN 'Other'
                    ELSE property_type
                END AS property_type
            ) FROM rel
        """)

    @staticmethod
    def rename_duration(rel: RelationType) -> RelationType:
        """Renames duration codes to descriptive labels."""
        return duckdb.sql("""
            SELECT * REPLACE (
                CASE duration
                    WHEN 'F' THEN 'Freehold'
                    WHEN 'L' THEN 'Leasehold'
                    WHEN 'U' THEN 'Unknown'
                    ELSE duration
                END AS duration
            ) FROM rel
        """)

    @staticmethod
    def rename_old_new(rel: RelationType) -> RelationType:
        """Renames old_new codes to descriptive labels."""
        return duckdb.sql("""
            SELECT * REPLACE (
                CASE old_new
                    WHEN 'Y' THEN 'New'
                    WHEN 'N' THEN 'Old'
                    ELSE old_new
                END AS old_new
            ) FROM rel
        """)

    @staticmethod
    def sort_by_year_and_property_type(rel: RelationType) -> RelationType:
        """Sorts ascending by year then property_type."""
        return duckdb.sql("SELECT * FROM rel ORDER BY year, property_type")

    @staticmethod
    def summarise_by_year_and_property_type(rel: RelationType) -> RelationType:
        """
        Summarises sales by year and property type, calculating total unique
        sales and max, min and median price per group.
        """
        return duckdb.sql("""
            SELECT
                year,
                property_type,
                COUNT(DISTINCT id)::INTEGER AS total_sales,
                MAX(price) AS max_price,
                MIN(price) AS min_price,
                MEDIAN(price) AS median_price
            FROM rel
            GROUP BY year, property_type
        """)
