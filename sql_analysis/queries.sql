-- SQL portfolio queries for interview prep and GitHub presentation
-- Assumes a table named covid_data with columns:
-- date, country, new_deaths_per_million, rolling_7d_avg, year, month

-- 1. Average daily deaths per million by country
SELECT
    country,
    ROUND(AVG(new_deaths_per_million), 3) AS avg_daily_deaths_per_million
FROM covid_data
GROUP BY country
ORDER BY avg_daily_deaths_per_million DESC;

-- 2. Maximum rolling 7-day mortality by country
SELECT
    country,
    ROUND(MAX(rolling_7d_avg), 3) AS max_rolling_7d_deaths_per_million
FROM covid_data
GROUP BY country
ORDER BY max_rolling_7d_deaths_per_million DESC;

-- 3. Total mortality burden by year and country
SELECT
    year,
    country,
    ROUND(SUM(new_deaths_per_million), 1) AS annual_deaths_per_million
FROM covid_data
GROUP BY year, country
ORDER BY year, annual_deaths_per_million DESC;

-- 4. Highest single-month mortality shock by country
SELECT
    country,
    year,
    month,
    ROUND(SUM(new_deaths_per_million), 1) AS monthly_deaths_per_million
FROM covid_data
GROUP BY country, year, month
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY country
    ORDER BY SUM(new_deaths_per_million) DESC
) = 1
ORDER BY monthly_deaths_per_million DESC;

-- 5. Rank countries by cumulative burden
SELECT
    country,
    ROUND(SUM(new_deaths_per_million), 1) AS cumulative_deaths_per_million,
    RANK() OVER (ORDER BY SUM(new_deaths_per_million) DESC) AS burden_rank
FROM covid_data
GROUP BY country
ORDER BY burden_rank;

-- 6. Compare pre- and post-2021 average mortality
SELECT
    country,
    ROUND(AVG(CASE WHEN date < '2021-01-01' THEN new_deaths_per_million END), 3) AS avg_before_2021,
    ROUND(AVG(CASE WHEN date >= '2021-01-01' THEN new_deaths_per_million END), 3) AS avg_2021_and_after
FROM covid_data
GROUP BY country
ORDER BY avg_2021_and_after DESC;
