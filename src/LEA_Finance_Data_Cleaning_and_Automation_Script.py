# Data Source Information:
# "Common Core of Data School District Finance Survey (F-33), FY 2010-2020." National Center for Education Statistics, U.S. Department of Education.
# Accessed from:
# - NCES Website – CCD Data Files: https://nces.ed.gov/ccd/files.asp#Fiscal:1,Page:1

# Local Education Agency Finance Survey – School District Data 2019 – 2020
# Local Education Agency will be abbreviated as LEA

# Import Packages
import pandas as pd
import numpy as np
import os
import json
from sqlalchemy import create_engine


def melt_df(df, schema, table, column_mapping_df, total_columns):
    columns_to_use = []
    new_columns = []
    for _, row in column_mapping_df.iterrows():
        if row['Table'] in [table, 'all']:
            if row['New Name'] not in total_columns:
                columns_to_use.append(row['New Name'])

    new_df = df[columns_to_use].copy()
    id_vars = ['census_id', 'year'] + [col for col in new_df.columns if col.endswith('_flag')]

    if schema == 'expenses':
        new_df = pd.melt(new_df, id_vars=id_vars, var_name='expenditure_title', value_name='amount')
        new_columns = ['expenditure_title', 'amount']
    elif schema == 'revenue':
        new_df = pd.melt(new_df, id_vars=id_vars, var_name='revenue_title', value_name='revenue')
        new_columns = ['revenue_title', 'revenue']

    remaining_columns = [col for col in id_vars if col not in new_columns]
    ordered_columns = remaining_columns[:2] + new_columns + remaining_columns[2:]
    new_df = new_df[ordered_columns]
    return new_df

# Database Initialization with Mapped Data
# use_database = input("Enter 'y' to use database script. Else enter 'n'")
use_database = 'y'

if use_database == 'y':

    # Read in database credentials from JSON file
    db_credentials_path = os.path.join("..", "LEA_Finance_Survey_DB.json")
    with open(db_credentials_path) as infile:
        credentials = json.load(infile)

    # Assign Credentials to Variables
    database_name = credentials['database']
    username = credentials['user']
    password = credentials['password']
    host = credentials['host']
    port = credentials['port']

    # Create a database connection using SQLAlchemy engine
    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database_name}')

# Importing the Dataset
for i in range(10, 21):

    file_name = f'sdf{i}.txt'
    file_path = os.path.join("..", "raw_data_files", file_name)

    df = pd.read_csv(file_path, delimiter= '\t')


    # Import the Column Mapping
    # An excel file with original and new column names, expected datatype, and descriptions is used.
    column_map_path = os.path.join("..", 'LEA Local Finance Survey – School District Data 2010 – 2020 – Column Mapping.xlsx')
    column_mapping_df = pd.read_excel(column_map_path,
                                      sheet_name= f'Column Mapping {i}')

    # Remove White Spaces from Column Names
    column_mapping_df['Original Name'] = column_mapping_df['Original Name'].str.strip()
    column_mapping_df['New Name'] = column_mapping_df['New Name'].str.strip()

    # Create Dictionary to Map New Column Names
    column_map_dict = column_mapping_df.set_index('Original Name')['New Name'].to_dict()

    # Rename Columns
    df.rename(columns=column_map_dict, inplace=True)
    df.columns = df.columns.str.strip()

    # Exclusion of Non-Government Entities from Analysis
    # Only LEAs with 'census_id' not equal to 'N' are considered for analysis.
    df = df[df['census_id'] != 'N']
    df['census_id'].duplicated().any()

    # Column Removal for Database Normalization
    # Columns starting with 'total_' are targeted for removal in the normalization process.
    total_columns = []
    for col in df.columns:
        if col.startswith('total_'):
            total_columns.append(col)


    column_totals = df[total_columns].copy()
    df.drop(columns= total_columns, inplace= True)

    # Casting Data Types
    # ansi_state_code and ansi_county_code are converted to Strings. 'year' is converted to datetime.
    df['year'] = df['year'].astype(str)
    df['year'] = '20' + df['year']
    df['year'] = pd.to_datetime(df['year'].astype(str), format='%Y')
    df['ansi_state_code'] = df['ansi_state_code'].astype(str)
    df['ansi_county_code'] = df['ansi_county_code'].astype(str)
    df['ccd_nonfiscal_match'] = df['ccd_nonfiscal_match'].astype(bool)
    df['census_fiscal_match'] = df['census_fiscal_match'].astype(bool)


    # Data Cleaning Notes
    # Special placeholders in financial data (e.g., -1, -2, -3) are replaced with NaN for accurate analysis.
    df.replace([-9, -3, -2, -1], np.nan, inplace=True)

    # Entity Schema Tables
    # Create entity DataFrame
    entity_columns = []
    for index, row in column_mapping_df.iterrows():
        if row['Table'] in ['entity', 'all'] and row['New Name'] != 'year':
            if row['New Name'] not in total_columns:
                entity_columns.append(row['New Name'])

    entity = df[entity_columns].copy()

    # Create annual_stats DataFrame
    annual_stats_columns = []
    for index, row in column_mapping_df.iterrows():
        if row['Table'] in ['annual_stats', 'all']:
            if row['New Name'] not in total_columns:
                annual_stats_columns.append(row['New Name'])

    annual_stats = df[annual_stats_columns].copy()

    if 'year' in annual_stats.columns and annual_stats.columns[-1] != 'year':
        cols = [col for col in annual_stats.columns if col != 'year']
        cols.append('year')
        annual_stats = annual_stats[cols]

    # Expenses & Revenue Schema Tables
    # melt_df() Function Description:
    # Converts data from wide to long format for normalization in relational databases and for visualizations.


    # Create DataFrames for expenditures, local, state, and federal revenue
    expenditures = melt_df(df, 'expenses', 'expenditures', column_mapping_df, total_columns)
    local = melt_df(df, 'revenue', 'local_revenue', column_mapping_df, total_columns)
    state = melt_df(df, 'revenue', 'state_revenue', column_mapping_df, total_columns)
    federal = melt_df(df, 'revenue', 'federal_revenue', column_mapping_df, total_columns)

    print(f"Data for the 20{i} School Year has been Cleaned and Normalized for the Database")

    census_id_query = 'SELECT census_id FROM entity.entity;'
    existing_census_ids = pd.read_sql(census_id_query, engine)

    # Convert the existing_census_ids DataFrame to a list for easier checking
    existing_census_id_list = existing_census_ids['census_id'].tolist()

    # Iterate through the entity DataFrame and drop rows where the census_id already exists
    entity = entity[~entity['census_id'].isin(existing_census_id_list)]

    # Create Database Mapping
    database_map = {
        'entity': ['entity', entity],
        'annual_stats': ['entity', annual_stats],
        'expenditures': ['expenses', expenditures],
        'federal_revenue': ['revenue', federal],
        'state_revenue': ['revenue', state],
        'local_revenue': ['revenue', local]
    }

    populate_new_tables = 'y'

    if populate_new_tables == 'y':
        print(f"Inserting data for the 20{i} School Year")
        
        # Iterate over the database_map to insert each DataFrame
        for table_name, [schema_name, df_to_export] in database_map.items():
            print(table_name)
            df_to_export.to_sql(table_name, engine, schema=schema_name, if_exists='append', index=False)
        print(f"Successfully inserted data for the 20{i} School Year")

engine.dispose()
