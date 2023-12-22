/*
This SQL query is designed to retrieve and summarize data related to educational entities and their expenditures. The query performs the following functions:

1. Selects the state and local education agency (LEA) name from the 'entity' table.
2. Extracts the year from the 'stats.year' field.
3. Retrieves fall membership data along with its associated flag from the 'annual_stats' table.
4. Translates the fall membership flag into a meaningful description:
   - 'R' indicates the data as reported by the state.
   - 'N' signifies that the data is not applicable.
   - 'M' denotes missing data.
   - 'A' means the data has been edited or suppressed by the analyst.
5. Calculates the sum of expenditures for each entity from the 'expenditures' table.
6. Joins the 'annual_stats', 'entity', and 'expenditures' tables based on the census_id.
7. Filters the results to include only those records where the fall membership is less than 50.
8. Groups the results by year, state, LEA name, fall membership, and the fall membership flag.
9. Orders the results by state, LEA name, year, and fall membership.

This query is particularly useful for analyzing small educational entities, as it focuses on those with fall memberships under 50. It provides a comprehensive overview of the entities' demographic information, membership status, and financial expenditures.
*/

SELECT entity.state, entity.lea_name, DATE_PART('year', stats.year) AS year, 
	stats.fall_membership, stats.fall_membership_flag,
	CASE 
		WHEN stats.fall_membership_flag = 'R' THEN 'As reported by state'
		WHEN stats.fall_membership_flag = 'N' THEN 'Not Applicable'
		WHEN stats.fall_membership_flag = 'M' THEN 'Missing'
		WHEN stats.fall_membership_flag = 'A' THEN 'Edited or Suppressed by the Analyst'
	END flag_meaning, SUM(exp.amount) AS sum_expenditures
FROM entity.annual_stats AS stats
LEFT JOIN entity.entity AS entity
	ON stats.census_id = entity.census_id
LEFT JOIN expenses.expenditures AS exp
	ON entity.census_id = exp.census_id
WHERE fall_membership < 50
GROUP BY stats.year, entity.state, 
		 entity.lea_name, stats.fall_membership, 
		 stats.fall_membership_flag
ORDER BY state, lea_name, stats.year, fall_membership;



