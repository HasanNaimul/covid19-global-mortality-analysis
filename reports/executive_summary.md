# Executive Summary

This project analyzes daily COVID-19 deaths per million across six countries (Canada, France, Germany, India, the United Kingdom, and the United States) from 2020-01-09 to 2023-06-12.

## What this project demonstrates
- End-to-end analytics workflow: data cleaning, feature engineering, exploratory analysis, KPI design, segmentation, and storytelling.
- Portfolio-grade outputs: reproducible Python code, notebook, static visuals, processed datasets, and an interactive dashboard.
- Advanced techniques beyond basic EDA: rolling metrics, wave detection with signal processing, recovery-speed analysis, and unsupervised clustering.

## Key findings
1. **Highest cumulative mortality burden**: United Kingdom (3347.9 deaths per million) followed closely by United States (3318.7).
2. **Most severe single-wave peak**: United Kingdom reached a 7-day rolling peak of 20.14 deaths per million on 2021-01-26.
3. **Slowest recovery after the main peak**: France needed 171 days to fall below 25% of its main-peak mortality level.
4. **Most concentrated monthly shock**: United Kingdom recorded the highest single-month burden in 2021-01 with 507.5 deaths per million.
5. **Segmentation result**: clustering separates countries into high-burden repeated-wave systems, lower-burden systems, and an extreme-peak outlier.

## Business-style recommendation
If this were a public-health monitoring product, the best operational dashboard would prioritize three signals:
- 7-day rolling deaths per million for trend direction,
- days-to-recovery after major peaks for resilience,
- cumulative burden plus wave count for cross-country benchmarking.

## Limitations
- Only six countries are included.
- The dataset tracks mortality intensity, not cases, vaccination, hospital capacity, or policy interventions.
- Clustering is illustrative because the sample size is very small.
