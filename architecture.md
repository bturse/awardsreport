**validate parameter formats**
- validate psc is 4 characters
- validate ym, y params
- validate cfda ##.###

**add additional data elements**
- solicitation_id, funding_opportunity_number
- PPop and recipient county name/fips
- assistance type descriptions
- recipient socioeconomic/demographic categories
- elements from contrct opportunity and NOFO

**load additional data sets**
- sam.gov contract opportunities (join w solicitation ID)
- grants.gov NOFO (join w FON)
- ACS 5 year county level data (join w county FIPS)

**Improve loader and API performance**
- add indexes to assistance_transactions, procurement_transactions, and transactions
to load data more quickly, try to do so before adding indexes:
    1. `alembic upgrade` to create tables without indexes
    2. load data
    3. `alembic upgrade head` (add indexes)
- replace set_award_summary_unique_key with a more performant solution, perhaps
update copy from statement
- request all downloads at once in seed.py
- implement incremental backoff for loaders

write seed.py tests

change type hints to MappedClassProtocol
https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html

use consistent langauge (summary_table not summary_tables) 
