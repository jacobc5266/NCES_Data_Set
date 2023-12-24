# NCES_Data_Set  
# Analysis of US Tech & Vocational Education Funding

### NOTE: This project is still in the beginning stages.

## Overview

This project involves a detailed analysis of funding trends for technology and vocational education across the United States, utilizing the 2019 - 2020 data from the Local Education Agency (LEA) Finance Survey provided by the National Center for Education Statistics (NCES).

Click here to run the visualizations notebook in a virtual environment: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jacobc5266/NCES_Data_Set/main?labpath=src%2FLEA_Finance_Data_Visualizations_v2.ipynb)

## Repository Structure

- `LEA_School_District_Finance_Survey.ipynb`: The Jupyter Notebook will contain the complete analysis pipeline, from data cleaning to exploratory data analysis.
- `2022304_FY20F33_Documentation.pdf`: Documentation from the NCES that provides context and details about the dataset.
- `LEA Local Finance Survey – School District Data 2019 – 2020 – Column Mapping.xlsx`: An XLSX file that outlines the original and new column names, their data types, and descriptions.
- `Local Education Agency Finance Survey – School District Data ERD.pdf`: An Entity-Relationship Diagram (ERD) depicting the database design intended for this dataset.

## Data Analysis Workflow

The Jupyter Notebook is the heart of this analysis. It includes:

1. **Data Cleaning**: Standardizing column names based on the provided column mapping and handling missing or inconsistent data.
2. **Data Transformation**: Pivoting the data from a wide to a long format to enhance readability and facilitate analysis.
3. **Normalization Techniques**: Applying Z-Score Standardization and Min/Max Scaling to the data for consistent comparison across different scales.
4. **Preliminary Visualization**: Initial steps to visualize the cleaned data are outlined for users to follow and apply in their preferred visualization tool.

## Getting Started

To explore this analysis:

1. Clone this repository to your local environment.
2. Install any required dependencies listed at the top of the Jupyter Notebook.
3. Open the `LEA_School_District_Finance_Survey.ipynb` notebook in Jupyter Lab or Jupyter Notebook.
4. Refer to `2022304_FY20F33_Documentation.pdf` for additional context on the dataset and analysis.
5. Review `LEA Local Finance Survey – School District Data 2019 – 2020 – Column Mapping.xlsx` to understand the dataset's schema changes.
6. Examine `Local Education Agency Finance Survey – School District Data ERD.pdf` to understand the intended database structure.

## Goals and Intentions

The purpose of this project is to provide a transparent, analytical look at the distribution and utilization of funds in US tech and vocational education. It sets the stage for potential predictive modeling to forecast future funding trends.

## Contributions

This project is designed for educational and informational purposes and is not currently set up for collaborative contributions. However, feedback, questions, and discussion are welcome. Please feel free to raise an issue or suggest improvements.

## Questions and Contact

Should you have any questions regarding this analysis, please open an issue in this repository, and I'll be happy to engage in a conversation.

## Acknowledgments

- National Center for Education Statistics (NCES) for providing the data.
- Open-source projects that made this analysis possible: Python, Jupyter, and the various libraries used in the analysis.
