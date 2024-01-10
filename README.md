# NCES_Data_Set  
# Comprehensive Analysis of US Tech & Vocational Education Funding (2010-2020)

### Project Status: Advanced Stages of Analysis

## Project Overview

This repository encapsulates an in-depth analysis of a decade's worth of US technical and vocational education funding data, sourced from the National Center for Education Statistics' Local Education Agency (LEA) Finance Survey. It demonstrates a sophisticated data analysis workflow, from crafting a PostgreSQL database to creating nuanced visualizations that render complex data into intelligible insights.

## Repository Contents

- `src/`: Jupyter Notebooks detailing the analytical pipeline with Python scripts for data processing and visualization.
- `PDF Documentation/`: In-depth dataset documentation from NCES and an Entity-Relationship Diagram (ERD) outlining the database architecture.
- `SQL Queries/`: SQL scripts crafted for precise data extraction and rigorous analysis.
- `Local Education Agency Finance Survey – School District Data ERD.pdf`: Detailed ERD visualizing the relational database design.

## Features

- A meticulously designed PostgreSQL database ensuring efficient data handling.
- Comprehensive Python-based data cleansing, ETL processes, and normalization techniques.
- Interactive, Plotly-based visualizations that highlight trends and funding trajectories in an engaging manner.
- Statistical analysis techniques applied to draw out patterns, growth rates, and significant fluctuations in funding streams.

## Interactive Notebooks

Experience the project's data visualizations interactively through Binder-hosted Jupyter Notebooks. Click the corresponding Binder badges to launch a virtual instance where you can run and interact with the notebooks directly from your browser, no local setup required.

National Level Analysis:  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jacobc5266/NCES_Data_Set/main?labpath=src%2FLEA_Finance_Data_National_Level_Analysis.ipynb)

Regional Level Analysis:  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jacobc5266/NCES_Data_Set/main?labpath=src%2FLEA_Finance_Data_Regional_Level_Analysis.ipynb)

**Please Note:** Binder may take a few moments to prepare the environment. I appreciate your patience. Upon loading, execute the notebook by selecting "Restart Kernel and Run All Cells" to see the analysis in action.

## Setup

To delve into this analysis:

1. Clone the repository to your local machine.
2. Install the necessary libraries as specified in `requirements.txt`.
3. Navigate through the Jupyter Notebooks for a step-by-step breakdown of the analyses.
4. Refer to the PDF documentation for a deeper understanding of the dataset nuances.
5. Review the ERD to comprehend the database schema.

## Key Insights

A noteworthy finding is the substantial 114.38% increase in the cost per student between 2014 and 2016, largely attributable to the introduction of new expenditure categories. The analysis also discerns a significant growth in teacher salaries for vocational education, marked by a 7.35% upswing in 2020.

## Acknowledgments

- Data: Sourced from the National Center for Education Statistics (NCES).
- Tools: Utilized Python, Jupyter, Plotly, PostgreSQL, among other open-source software.
