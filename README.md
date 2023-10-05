## About
The USAspending Monthly Awards Report uses federal prime award transaction data
from USAspending.gov to provide information on the top categories receiving
spending by various elements for each month.


## Requires
- python 3.10
- PostgreSQL

## Setup and Installation
1. install requirements: `pip install -r requirements.txt` and `pip install .`
2. create a psql database
3. set database information: `mv .env.example .env`, update values in `.env`
4. run alembic migrations: `alembic upgrade head`
5. seed the database with raw data from USAs: `python src/awardsreport/setup/seed.py`. Accepts optional
`--year`, `--month`, `no_months`, and `period_months` int parameters.
6. run derivations: `python src/awardsreport/setup/transaction_derivations.py`
7. insert records to `transansactions` table: `python src/awardsreport/setup/seed_transactions_table`
8. run server on localhost: `python src/awardreport/main.py`


## Project Structure
- `/src/awardsreport/` main functionality of the API, including: business logic,
routers, setup scripts, models.
  - `/src/awardsreport/logic/` business logic and helper functions
  - `src/awardsreport/routers/` FastAPI routers to implement logic
  - `src/awardsreport/schemas/` Pydantic models to support validation and
  documentation
  - `src/awardsreport/database.py` SQLAlchemy base classes and boilerplate
  - `src/awardsreport/main.py` uvicorn run command to start server for API
  - `src/awardsreport/models.py` SQLAlchemy models
  - `src/awardsreport/setup/` scripts to seed database and perform derivations
- `/src/tests` unit tests and pytest configuration
- `/.env.example` sample database connection information. To be saved as `/.env`
for python dotenv package.


## Contributing
- black formatting, available through `/.vscode/settings.json`
- Pylance with Type Checking Mode = basic
