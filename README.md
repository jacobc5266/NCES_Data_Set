# NCES_Data_Set  
# Comprehensive Analysis of US Tech & Vocational Education Funding (2010-2020)

### Project Status: Advanced Stages of Analysis

## Project Overview

This repository documents a deep dive into a decade of US tech and vocational education funding and expenditures, leveraging data from the Local Education Agency (LEA) Finance Survey by the National Center for Education Statistics (NCES). It showcases an end-to-end data analysis workflow from database design to insightful visualizations.

## Repository Contents

- `src/`: Jupyter Notebooks with complete analysis pipeline and Python scripts for data visualizations.
- `PDF Documentation/`: NCES dataset documentation providing crucial context and ERD Diagram showing the structure of the database.
- `SQL Queries/`: SQL scripts used to extract and analyze the data.
- `Local Education Agency Finance Survey – School District Data ERD.pdf`: A comprehensive Entity-Relationship Diagram (ERD) showcasing the database design.

## Features

- Detailed PostgreSQL database design for robust data management.
- Advanced data cleaning, transformation, and normalization in Python.
- Interactive visualizations created with Plotly to identify and communicate funding patterns.
- Statistical analysis to uncover trends and growth rates.

## Interactive Notebook in Binder

For a hands-on experience with the project's data visualizations, you can run the Jupyter Notebook in your web browser via Binder. Click on the Binder badge below or [click here](https://mybinder.org/v2/gh/jacobc5266/NCES_Data_Set/main?labpath=src%2FLEA_Finance_Data_Visualizations_v2.ipynb) to launch a virtual environment where you can interact with the notebook and explore the visualizations without any local setup. This environment is fully configured to mirror the project's requirements, ensuring a seamless user experience.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jacobc5266/NCES_Data_Set/main?labpath=src%2FLEA_Finance_Data_Visualizations_v2.ipynb)


## Setup

To get started with this analysis:

1. Clone this repository.
2. Install dependencies listed in `requirements.txt`.
3. Open the Jupyter Notebooks to walk through the analysis steps.
4. Use the PDF documentation for additional context on the dataset.
5. Examine the ERD for insights into the database structure.

## Key Insights

The analysis revealed a 114.38% increase in cost per student from 2014 to 2016, driven by new expenditure categories. A spike of 7.35% in teacher salaries for vocational education in 2020 suggests substantial growth.

## Future Work

The next phase will introduce machine learning models to forecast funding trends based on historical data, furthering the depth of the analysis.

## Acknowledgments

- Data: Provided by the National Center for Education Statistics (NCES).
- Tools: Python, Jupyter, Plotly, PostgreSQL, and other open-source libraries.
