add indexes to assistance_transactions and procurement_transactions



should I have a single table that combines both procurement and assistance
transactions?

pros: 
- easier to write queries that do not regard award type (total govspending)
  - no need to join across tables, faster queries?

cons:
- more storage need to maintain 2 versions of the data
  - assistance and procurement transaction tables need to enforce different required fields.
- slower setup

alternatives:
- just check if all groupby cols are in both procurement and transactions and if
so, create a temp table with indexes.
  pros: less storage
  cons: slower


summary_table should return list of dicts:
{
  "grouping": ["cfda_number", "cfda_title"],
  "sum_generated_pragmatic_obligations": $100
}


replace set_award_summary_unique_key with a more performant solution, perhaps
update copy from statement

request all downloads at once in seed.py



type annotate seed and seed_helper functions