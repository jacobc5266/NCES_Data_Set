/*
This SQL query calculates the z-scores for expenditure amounts across different states, expenditure titles, and years. The z-score represents how many standard deviations an expenditure amount is from the mean of that expenditure category for a given state and year. The key components of the query are:

1. Selection of relevant columns: The query selects the census ID, state, expenditure title, year, and expenditure amount from the 'entity' and 'expenditures' tables.

2. Calculation of z-scores: 
   - The z-score is computed using the formula (amount - mean) / standard deviation.
   - The mean and standard deviation are calculated over a partition of data grouped by state, expenditure title, and year.
   - A CASE statement is used to handle cases where the standard deviation is zero (to avoid division by zero). In such cases, the z-score is set to NULL.

3. Join Operation: An INNER JOIN is used to combine data from the 'entity' and 'expenditures' tables based on the census ID.

4. Data Filtering: The WHERE clause filters out records where the expenditure amount is either NULL or zero to ensure meaningful z-score calculations.

This query is particularly useful for identifying outliers and understanding the distribution of expenditure amounts within specific categories across different states and years. It provides a standardized way to compare expenditures, regardless of the underlying distribution.
*/


CREATE MATERIALIZED VIEW expenses.expenditure_zscores_by_state_year AS
SELECT
    e.census_id,
    e.state,
    exp.expenditure_title,
    DATE_PART('year',exp.year) AS year,
    exp.amount,
    CASE 
        WHEN STDDEV(exp.amount) OVER (PARTITION BY e.state, exp.expenditure_title, exp.year) = 0 THEN NULL
        ELSE (exp.amount - AVG(exp.amount) OVER (PARTITION BY e.state, exp.expenditure_title, exp.year)) / STDDEV(exp.amount) OVER (PARTITION BY e.state, exp.expenditure_title, exp.year)
    END AS amount_z_score
FROM
    entity.entity AS e
INNER JOIN expenses.expenditures AS exp
    ON e.census_id = exp.census_id
WHERE exp.amount IS NOT NULL AND exp.amount != 0;
