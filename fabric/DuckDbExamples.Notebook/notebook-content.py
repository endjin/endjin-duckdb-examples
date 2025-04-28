# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.11"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "3881b34b-dd06-4203-a06c-0bedb6858b09",
# META       "default_lakehouse_name": "PricePaidData",
# META       "default_lakehouse_workspace_id": "f324daa0-83dc-421d-a61e-637be44b4ff5"
# META     }
# META   }
# META }

# CELL ********************

import duckdb
import polars as pl
from deltalake import DeltaTable, write_deltalake
import plotly.express as px

import plotly

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Land Registry Price Paid Data
# 
# There is no header row.  So we need to define the column names.

# MARKDOWN ********************

# ### Setting up

# CELL ********************

# A single year of data for speed for development
price_paid_data_single_year = "/lakehouse/default/Files/land_registry/pp-2023.csv"
# All ~20 years of data for testing scalability
price_paid_data_complete = "/lakehouse/default/Files/land_registry/pp-*.csv"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Start with a smaller file

# CELL ********************

duckdb.sql(f"FROM read_csv('{price_paid_data_single_year}')")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

duckdb.sql(f"DESCRIBE SELECT * FROM read_csv('{price_paid_data_single_year}')")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Add column names and features

# CELL ********************

duckdb.sql(
    f"""
    SELECT
    column00 AS 'id',
    column01 AS 'price',
    column02 AS 'date',
    column03 AS 'postcode',
    column04 AS 'property_type',
    column05 AS 'old_new',
    column06 AS 'duration',
    column07 AS 'paon',
    column08 AS 'saon',
    column09 AS 'street',
    column10 AS 'locale',
    column11 AS 'town_city',
    column12 AS 'district',
    column13 AS 'county',
    column14 AS 'ppd_category',
    column15 AS 'record_type',
    year(date) AS 'year_of_sale',
    month(date) AS 'month_of_sale'
    FROM read_csv(
        '{price_paid_data_single_year}',
        header=False
    );
    """
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

duckdb.sql(
    f"""
    SELECT
    column00 AS 'id',
    column01 AS 'price',
    column02 AS 'date',
    column03 AS 'postcode',
    column04 AS 'property_type',
    column05 AS 'old_new',
    column06 AS 'duration',
    column07 AS 'paon',
    column08 AS 'saon',
    column09 AS 'street',
    column10 AS 'locale',
    column11 AS 'town_city',
    column12 AS 'district',
    column13 AS 'county',
    column14 AS 'ppd_category',
    column15 AS 'record_type',
    year(date) AS 'year_of_sale',
    month(date) AS 'month_of_sale'
    FROM read_csv(
        '{price_paid_data_single_year}',
        header=False
    );
    """
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Setting up a database

# CELL ********************

# Connect to an in-memory DuckDB database
# db = duckdb.connect(':memory:')
# Alternatively we can persist the DuckDB database in the built-in area which is available
db = duckdb.connect('./builtin/my_local_database.duckdb')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

db.sql("DROP TABLE IF EXISTS price_paid;")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

db.sql(
    f"""
    CREATE TABLE 'price_paid' AS
    SELECT
    column00 AS 'id',
    column01 AS 'price',
    column02 AS 'date',
    column03 AS 'postcode',
    column04 AS 'property_type',
    column05 AS 'old_new',
    column06 AS 'duration',
    column07 AS 'paon',
    column08 AS 'saon',
    column09 AS 'street',
    column10 AS 'locale',
    column11 AS 'town_city',
    column12 AS 'district',
    column13 AS 'county',
    column14 AS 'ppd_category',
    column15 AS 'record_type',
    year(date) AS 'year_of_sale'
    FROM read_csv(
        '{price_paid_data_single_year}',
        header=False
    );
    """
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

db.sql("SELECT COUNT (*) FROM 'price_paid'")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

db.sql("FROM price_paid")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Aggregations over raw data

# CELL ********************

duckdb.sql(
    f"""
    SELECT year(column02) AS 'year_of_sale', COUNT(*)
    FROM read_csv(
        '{price_paid_data_complete}',
        header=False
    )
    GROUP BY ALL;
    """
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

average_prices_by_year = duckdb.sql(
    f"""
    SELECT
    avg(column01) AS 'average_price',
    column04 AS 'property_type',
    year(column02) AS 'year_of_sale'
    FROM read_csv(
        '{price_paid_data_complete}',
        header=False
    )
    WHERE property_type <> 'O'
    GROUP BY ALL;
    """
).pl()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

display(average_prices_by_year)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Setting up to write to OneLake

# CELL ********************

table_path = "abfss://DuckDbPolarsDemos@onelake.dfs.fabric.microsoft.com/PricePaidData.Lakehouse/Tables/land_registry/house_sales"

"abfss://DuckDbPolarsDemos@onelake.dfs.fabric.microsoft.com/PricePaidData.Lakehouse/Files/land_registry_parquet/"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

storage_options = {"bearer_token": notebookutils.credentials.getToken("storage"), "use_fabric_endpoint": "true"}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Writing to Delta via Polars Dataframe
# 
# Given there is no support currently to write directly to Delta from DuckDB, the recommended approach is to convert tabular data into DataFrame (such as Polars) and then write that to the lakehouse.

# MARKDOWN ********************

# Let's try first writing a single year of data (about ~700K rows) to Delta.

# CELL ********************

# duckdb.sql(
#     f"""
#     SELECT
#     column00 AS 'id',
#     column01 AS 'price',
#     column02 AS 'date',
#     column03 AS 'postcode',
#     column04 AS 'property_type',
#     column05 AS 'old_new',
#     column06 AS 'duration',
#     column07 AS 'paon',
#     column08 AS 'saon',
#     column09 AS 'street',
#     column10 AS 'locale',
#     column11 AS 'town_city',
#     column12 AS 'district',
#     column13 AS 'county',
#     column14 AS 'ppd_category',
#     column15 AS 'record_type',
#     year(date) AS 'year_of_sale'
#     FROM read_csv(
#         '{price_paid_data_single_year}',
#         header=False
#     )
#     WHERE property_type <> 'O'
#     ;
#     """
# ).pl().write_delta(
#     table_path,
#     mode='overwrite',
#     storage_options=storage_options)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# When we try to write the full dataset, DuckDB can load the data, but the operation below fails during the conversion to Polars and writing to the lake with the following error:
# 
# ```
# Kernel died: Kernel python3.11 has died, please restart the kernel.
# 
# Diagnostic Info:
# session id: eac9fb6c-83d2-480a-ae54-e89f12a7d6bc
# pid: 39
# exit code: -9 (Forced-process termination. This is often caused by insufficient memory causing the process to be killed. Please check memory usage)
# cluster name: cfc72989-b358-418b-a2e1-6c6188e0000d
# Maximum memory in 2 minutes: 14.94GB
# Maximum cpu usage in 2 minutes: 100.0%
# ```

# CELL ********************

# complete_dataset = duckdb.sql(
#     f"""
#     SELECT
#     column00 AS 'id',
#     column01 AS 'price',
#     column02 AS 'date',
#     column03 AS 'postcode',
#     column04 AS 'property_type',
#     column05 AS 'old_new',
#     column06 AS 'duration',
#     column07 AS 'paon',
#     column08 AS 'saon',
#     column09 AS 'street',
#     column10 AS 'locale',
#     column11 AS 'town_city',
#     column12 AS 'district',
#     column13 AS 'county',
#     column14 AS 'ppd_category',
#     column15 AS 'record_type',
#     year(date) AS 'year_of_sale'
#     FROM read_csv(
#         '{price_paid_data_complete}',
#         header=False
#     )
#     WHERE property_type <> 'O'
#     ;
#     """
# ).pl().write_delta(
#     table_path,
#     mode='overwrite',
#     storage_options=storage_options)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Try writing directly to Parquet
# 
# Give the operation above has failed for the full dataset, we next tried to write in parquet format using the DuckDB `COPY` command.
# 
# Unfortunately, this fails too with the following error:
# 
# ```
# NotImplementedException                   Traceback (most recent call last)
# Cell In[9], line 1
# ----> 1 duckdb.sql(
#       2     f"""
#       3     COPY
#       4     (
#       5         SELECT
#       6         column00 AS 'id',
#       7         column01 AS 'price',
#       8         column02 AS 'date',
#       9         column03 AS 'postcode',
#      10         column04 AS 'property_type',
#      11         column05 AS 'old_new',
#      12         column06 AS 'duration',
#      13         column07 AS 'paon',
#      14         column08 AS 'saon',
#      15         column09 AS 'street',
#      16         column10 AS 'locale',
#      17         column11 AS 'town_city',
#      18         column12 AS 'district',
#      19         column13 AS 'county',
#      20         column14 AS 'ppd_category',
#      21         column15 AS 'record_type',
#      22         year(date) AS 'year_of_sale'
#      23         FROM read_csv(
#      24             '{price_paid_data_complete}',
#      25             header=False
#      26         )
#      27         WHERE property_type <> 'O'
#      28     )
#      29     TO 'abfss://DuckDbPolarsDemos@onelake.dfs.fabric.microsoft.com/PricePaidData.Lakehouse/Tables/land_registry/house_sales_parquet' (FORMAT parquet);
#      30     """
#      31 )
# 
# NotImplementedException: Not implemented Error: Writing to Azure containers is currently not supported
# ```


# CELL ********************

duckdb.sql(
    f"""
    COPY
    (
        SELECT
        column00 AS 'id',
        column01 AS 'price',
        column02 AS 'date',
        column03 AS 'postcode',
        column04 AS 'property_type',
        column05 AS 'old_new',
        column06 AS 'duration',
        column07 AS 'paon',
        column08 AS 'saon',
        column09 AS 'street',
        column10 AS 'locale',
        column11 AS 'town_city',
        column12 AS 'district',
        column13 AS 'county',
        column14 AS 'ppd_category',
        column15 AS 'record_type',
        year(date) AS 'year_of_sale'
        FROM read_csv(
            '{price_paid_data_single_year}',
            header=False
        )
        WHERE property_type <> 'O'
    )
    TO 'abfss://DuckDbPolarsDemos@onelake.dfs.fabric.microsoft.com/PricePaidData.Lakehouse/Files/land_registry_parquet/' (FORMAT PARQUET);
    """
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Iterate over years and merge
# 
# The final solution is to simply iterate over the individual years in the dataset that we want to extract, on each iteration:
# 
# - Use the power of DuckDB to filter the CSV and pull all transactions for a specific year
# - Convert the resulting table to Polars DataFrame
# - Write to Delta using Polars `write_delta` method
# - Leverage Delta's merge with condition to ensure we append new years to the data and overwrite existing years if we re-run the process

# CELL ********************

# for year in [2010, 2011, 2012]:

#     print(f"Processing year {year}")

#     year_chunk = duckdb.sql(
#         f"""
#             SELECT
#             column00 AS 'id',
#             column01 AS 'price',
#             column02 AS 'date',
#             column03 AS 'postcode',
#             column04 AS 'property_type',
#             column05 AS 'old_new',
#             column06 AS 'duration',
#             column07 AS 'paon',
#             column08 AS 'saon',
#             column09 AS 'street',
#             column10 AS 'locale',
#             column11 AS 'town_city',
#             column12 AS 'district',
#             column13 AS 'county',
#             column14 AS 'ppd_category',
#             column15 AS 'record_type',
#             year(date) AS 'year_of_sale'
#             FROM read_csv(
#                 '{price_paid_data_complete}',
#                 header=False
#             )
#             WHERE property_type <> 'O' AND year_of_sale = {year}
#             ;
#         """
#     ).pl()

#     (
#         year_chunk.write_delta(
#             table_path,
#             mode="merge",
#             delta_merge_options={
#                 "predicate": "s.year_of_sale = t.year_of_sale",
#                 "source_alias": "s",
#                 "target_alias": "t",
#             },
#             storage_options=storage_options
#         )
#         .when_matched_update_all()
#         .when_not_matched_insert_all()
#         .execute()
#     )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Reading from a Table in the lakehouse

# CELL ********************

duckdb.sql(
    f"""
    SELECT year_of_sale, COUNT(*) FROM delta_scan('{table_path}') GROUP BY ALL
    """
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
