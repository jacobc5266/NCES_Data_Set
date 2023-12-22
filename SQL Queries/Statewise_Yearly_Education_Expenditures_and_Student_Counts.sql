/*
This query provides a yearly summary of total educational expenditures and student enrollment counts for each state. It consists of two parts:

1. cte_expenditures: A Common Table Expression that aggregates the total expenditures from the 'expenditure_zscores_by_state_year' materialized view for each state and year.

2. cte_fall_membership: Another CTE that aggregates the total fall membership (student count) from the 'annual_stats' table joined with the 'entity' table on 'census_id', grouped by state and year.

The main query then combines these two CTEs by performing a LEFT JOIN on state and year, ensuring that even if there are no expenditure records for a given state and year, the query still returns the student count with a default expenditure value of 0. The results are ordered by state and year for a chronological overview of the data.
*/


WITH cte_expenditures AS (
    SELECT 
		state, year, 
		SUM(amount) AS total_amount
    FROM expenses.expenditure_zscores_by_state_year
    GROUP BY state, year
),
cte_fall_membership AS (
    SELECT
        e.state,
        DATE_PART('year', stats.year) AS year, 
        SUM(stats.fall_membership) AS student_count
    FROM entity.annual_stats AS stats
    INNER JOIN entity.entity AS e
    ON e.census_id = stats.census_id
    GROUP BY e.state, year
)
SELECT 
    fall_membership.state, 
    fall_membership.year, 
    fall_membership.student_count, 
    COALESCE(expenditures.total_amount, 0) AS total_expenditures
FROM cte_fall_membership AS fall_membership
LEFT JOIN cte_expenditures AS expenditures
    ON fall_membership.state = expenditures.state 
    AND fall_membership.year = expenditures.year
ORDER BY fall_membership.state, fall_membership.year;
