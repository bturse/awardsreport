requires:
python3.11
psql

update variables in .env.example and save as .env

create and activate virtual environment:\
`python3 -m venv .venv`\
`source .venv/bin/activate`

install packages:\
`pip install -r requirements.txt`

install the awardsreport package:\
`pip install -e .`

set up and seed the database:\
`python src/awardsreport/seed.py`
