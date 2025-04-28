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

import polars as pl


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

raw_data_file = "/lakehouse/default/Files/ny_taxi_data/puYear=2015/puMonth=1/*.snappy.parquet"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

df = pl.read_parquet(raw_data_file)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

df

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
