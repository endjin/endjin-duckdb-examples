# endjin-duckdb-examples

A set of worked examples loading and transforming data using DuckDB.

## Pre-requisites

- Git: to pull down this repository to allow you to run it locally.
- VS Code: to view and interactively run the code.
- Docker (or equivalent): to create a containerized Python environment to which VS Code can connect to execute the code.

## Steps

Pull down the repo locally:

```
git clone https://github.com/endjin/endjin-duckdb-examples.git
```

Open the repo in VS Code.
```
cd endjin-duckdb-examples
code .
```

You should be prompted by VS Code to open the project in a Dev Container as soon as VS Code launches.

if not: `CRTL + SHIFT + P` then select "Reopen in Container" from command menu.

The Dev Container may take a few minutes to build first time.  This sets up everything you need to run the code: Python environment, Python packages required and Azure CLI.

Once you are running inside the Dev Container, navigate to the `notebooks` folder where you will find a series Jupyter notebooks, each providing an example of using DuckDB.

Open a notebook, you may need to connect it to the Python virtual environment created by Poetry which is called: `endjin-duckdb-examples-a5MKY_F3-py3.12`.

Follow example specific instructions in notebook.

## Connecting to Cloud storage

For some of the Jupyter notebooks, you will need to connect to Azure resources or to Fabric Onelake storage.  To enable this log in to Azure to create a set of credentials:

`az login`

