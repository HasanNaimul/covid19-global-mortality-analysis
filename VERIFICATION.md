# Verification notes — 21 October 2026

## Before and after

Both runs used the original preparation and summary functions with temporary output paths. Each processed 7,506 records into six country summaries. Reproduced UK and US cumulative sums: 3,347.9 and 3,318.7 deaths per million respectively (rounded in the README). France's recovery-threshold interval was 171 days. The source and calculations were not edited.

## Added tests

Command: `python -m unittest discover -s tests -v` from the repository root.

Seven test methods passed: source schema/nonempty input, required keys and duplicate dates, daily spacing per country, finite mortality values, country-isolated rolling averages and sums, cumulative total/recovery threshold, and missing recovery when the threshold is not reached.

Small synthetic fixtures are confined to tests; they are not substitutes for the source dataset or published results. Test-generated CSVs use temporary directories.

## Limits

The notebook, HTML dashboard and all figures were preserved, not regenerated. SQL examples were not executed; their required field mapping and dialect-specific QUALIFY use are documented. Source provenance and reuse terms remain unverified. No causal interpretation or complete coverage claim is made.

Environment: Python 3.12.14, pandas 2.2.3, NumPy 2.3.5, SciPy 1.17.0 and scikit-learn 1.8.0. These record the review environment, not a newly imposed lockfile.
