-- This script creates a view named 'funding_view' in the 'revenue' schema.
-- The view combines federal and state funding data, filtering out NULL values and amounts less than or equal to 0.
-- Federal funding data is sourced from 'federal_revenue' table based on specific revenue titles,
-- while state funding data is sourced from 'state_revenue' table using different revenue titles.
-- Rows with NULL or revenue less than or equal to 0 are excluded from both federal and state funding sources.
-- The final output combines these datasets using UNION to form the 'funding_view'.

CREATE OR REPLACE VIEW revenue.funding_view AS
WITH federal_funding AS (
    SELECT 
        fed.census_id,
		e.state,
        DATE_PART('year', fed.year) AS year, 
        fed.revenue_title, 
        fed.revenue AS revenue_amount,
        'federal' AS funding_source
    FROM revenue.federal_revenue AS fed
	INNER JOIN entity.entity AS e
	ON fed.census_id = e.census_id
    WHERE revenue_title IN (
                            'math_science_teacher_quality_thru_state',
                            '21st_century_learning_centers_thru_state',
                            'student_support_academic_enrich_thru_state',
                            'education_stabilization_fund_esf_rem_grant',
                            'title_I_thru_state',
                            'bilingual_education_thru_state',
                            'education_stabilization_fund_esf_rwp_grant',
                            'effective_instruction_support_thru_state',
                            'voc_tech_education_thru_state',
                            'indiv_with_disabilities_thru_state',
                            'esser_fund',
                            'geer_fund'
                           )
	AND revenue > 0
),

state_funding AS (
    SELECT 
        st.census_id,
		e.state,
        DATE_PART('year', st.year) AS year, 
        st.revenue_title, 
        st.revenue AS revenue_amount,
        'state' AS funding_source
    FROM revenue.state_revenue AS st
	INNER JOIN entity.entity AS e
	ON st.census_id = e.census_id
    WHERE revenue_title IN (
                            'bilingual_education_state',
                            'compensatory_basic_skills_programs',
                            'vocational_education_programs',
                            'general_formula_assistance',
                            'special_education_programs'
                           )
	AND revenue > 0
)
SELECT * FROM federal_funding
UNION 
SELECT * FROM state_funding;
