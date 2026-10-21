# SQL examples

[queries.sql](queries.sql) contains analytical examples, not a connected database pipeline. Create a `covid_data` table from the enriched CSV using this mapping before adapting the queries:

| CSV field | SQL field |
| --- | --- |
| `Day` | `date` |
| `Entity` | `country` |
| `deaths_per_million` | `new_deaths_per_million` |
| `rolling_7d` | `rolling_7d_avg` |
| `year` | `year` |
| `month` | `month` |

Use a date type for `date`, numeric types for mortality measures, and text for the `YYYY-MM` month. No database creation, loading script or credentials are included.

Query 4 uses `QUALIFY`, which is dialect-specific; adapt it to a subquery where unsupported. The October 2026 review did not execute these SQL examples against a database. Their field names differ from the Python output deliberately and require the explicit mapping above.
