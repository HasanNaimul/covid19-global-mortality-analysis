# Case Study: Global COVID-19 Mortality Analysis

## 1. Business context
A public-health strategy team wants a fast way to compare mortality pressure across countries and understand whether high mortality came from repeated waves, extreme single peaks, or slower recovery after major outbreaks.

## 2. Problem statement
Raw daily mortality values are difficult to compare because they are noisy and change over time. The goal is to convert daily observations into a set of consistent analytical measures that make countries comparable.

## 3. Analytical approach
The analysis focuses on normalized daily deaths per million and uses rolling smoothing, peak detection, and country-level feature engineering to quantify:
- cumulative burden
- severity of the worst wave
- number of meaningful waves
- time required to recover after the main peak
- overall volatility

## 4. Data preparation
The source dataset was cleaned and standardized before analysis. Country names, date fields, and missing values were handled consistently so the workflow could be reproduced with scripts rather than manual edits.

## 5. Methods used
- 7-day rolling averages to reduce daily reporting noise
- cumulative mortality metrics for overall burden
- peak and wave logic to identify severe outbreak periods
- recovery-speed analysis after the main peak
- clustering for country segmentation

## 6. Main findings
- The United Kingdom and United States show the highest cumulative mortality burden in the selected sample.
- The United Kingdom experienced the most severe rolling peak.
- France recorded the slowest post-peak recovery in the sample.
- Countries do not follow one shared mortality pattern; they separate into different burden and resilience profiles.

## 7. Why this matters
This kind of analysis is useful because decision-makers often need more than a trend chart. They need a framework that explains whether a system is experiencing repeated shocks, one extreme shock, or prolonged recovery.

## 8. Limitations
The project uses six countries and focuses on deaths per million only. It does not include vaccination rates, testing, mobility, hospital capacity, demographics, or policy interventions.

## 9. Next-step improvements
- join vaccination and policy datasets
- build a Power BI or Tableau dashboard version
- extend the SQL layer with more advanced analytical queries
- test forecasting methods for short-term monitoring scenarios
