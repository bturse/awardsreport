## About
The USAspending Monthly Awards Report uses federal prime award transaction data
from USAspending.gov to provide information on the top categories receiving
spending by various elements for each month.

## Required
Docker (with Docker Compose v2)

## Setup and Installation
```
1. Build images: `docker compose build`
2. Start the database: `docker compose up -d postgres`
3. Run database migrations: `docker compose run --rm app alembic upgrade head`
4. Seed the database with USAspending data: ex: `docker compose run --rm app \
  python src/awardsreport/setup/seed.py --year 2025 --month 12 --no_months 3` (see: `docker compose run --rm app python src/awardsreport/setup/seed.py -h`)
5. Run derivation and populate transactions table: `docker compose run --rm app python src/awardsreport/setup/transaction_derivations.py
docker compose run --rm app python src/awardsreport/setup/seed_transactions_table.py`
6. Start the API server `docker compose up app`

## Running Tests
`docker compose -p awards-test run --rm app pytest`

## Example Usage
Using the `summary_tables` GET endpoint to populate a pandas DataFrame:
```
import json
import pandas as pd
import requests

r = requests.get("http://localhost:8000/summary_tables/?gb=naics&gb=ppopct&gb=awag&limit=500")

df = pd.read_json(json.dumps(r.json()), orient='table')
```

Study the response metadata using the [JSON Table Schema](https://dataprotocols.org/json-table-schema/):
```
r.json()['schema']
```


## Project Structure
- `/src/awardsreport/` main functionality of the API, including: business logic,
routers, setup scripts, models.
  - `/src/awardsreport/logic/` business logic
  - `src/awardsreport/routers/` FastAPI routers to implement logic
  - `src/awardsreport/schemas/` Pydantic models to support validation and
  documentation
  - `src/awwardsreport/services` Format API response
  - `src/awardsreport/database.py` SQLAlchemy base classes and boilerplate
  - `src/awardsreport/main.py` uvicorn run command to start server for API
  - `src/awardsreport/models.py` SQLAlchemy models
  - `src/awardsreport/setup/` scripts to seed database and perform derivations
- `/src/tests` unit tests and pytest configuration
  - `src/tests/logic` tests for scripts in `src/awardsreport/logic`
  - `src/tests/setup` tests for scripts in `src/awardsreport/setup`
  - `src/tests/services` tests for scripts in `src/awardsreport/services`
- `/.env.example` sample database connection information. To be saved as `/.env`
for python dotenv package.


## Contributing
- black formatting, available through `/.vscode/settings.json`
- Pylance with Type Checking Mode = basic
### Add new column from a raw USAs download
This section describes how to add new columns to the project from a raw USAs
download file. This section does not cover adding new derived columns. Adding
new columns is necessary to support grouping or filtering by elements available
in USAs downloads, but not awardsreport.

1. Update `expected_results` in `test_get_raw_columns_assistance` and/or
`test_get_raw_columns_procurement` in `src/tests/setup/test_seed_helpers.py`.
Add raw column name from USAs download to list in alphabetical order.
    - If the column appears in Assistance download files, add to
    `test_get_raw_columns_assistance`.
    - If the column appears in Contract download files, add to
    `test_get_raw_columns_procurement`.
2. Add new column header as it appears in the download to the appropriate model
in `src/awardsreport/models.py`. 
    - If the column only appears in Assistance download files, add to
    `AssistanceTransactionsMixin`
    - If the column only appears in Contract download files, add to
    `ProcurementTransactionsMixin`
    - If the column appears in both Assistance and Contract download files, add
    to `TransactionsMixin`
    - Provide a `doc` attribute to descibe the element. Take langauge from
    USAspending data dictionary.
3. Generate new alembic revision using updated model: `alembic revision --autogenerate -m "brief description of change"`
4. Run alembic migrations, seed the database, run derivations, populate
`transactions` table. (See `Setup and Installation`)
5. run tests: `pytest`
### support summary table group by new column
This section describes how to allow the path GET `/summary_tables/` to accept
new `gb` parameter key values.
1. Add any necessary unit tests to `src/tests/logic/test_summary_tables.py`.
2. Add brief key to `gb_values` Literal in
`src/awardsreport/schemas/summary_tables_schemas.py`.
    - `src/tests/logic/test_summary_tables.py test_create_group_by_col_list_each` 
    will test this element when added to `gb_values`.
3. Add item to `group_by_key_col` dict in
`src/awardsreport/logic/summary_tables.py`. Use the same key from previous step.
4. Add attribute to `TableSchemaData` in `src/awardsreport/schemas/summary_tables_schemas` using same name from step 2.
5. run tests: `pytest`
### support summary table filter by new column
This section describes how to allow the path GET `/summary_tables/` to accept
new filter parameters.
1. Add any necessary unit tests to `src/tests/logic/test_summary_tables.py`.
    - test function names should take the form: `test_create_filter_statement_`
2. Add item to `filter_key_op` dict in
`src/awardsreport/logic/summary_tables.py`. If the filter merely checks for
equality with an element that can be grouped by, use the same key from
`group_by_key_col`.
3. Add attribute to `FilterStatementSchema` in
`src/awardsreport/schemas/summary_tables_schemas.py`. The attribute name should
match the key of the dict item from the previous set. If the filter merely
checks for equality, the Query description should call the SQLAlchemy model
element doc.
4. run tests: `pytest`


## License
MIT