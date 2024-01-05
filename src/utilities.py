import numpy as np
import pandas as pd
import os
import json
import psycopg2
from psycopg2 import OperationalError
from typing import Optional
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class Utilities:


    ############################## Connect to Database ##############################
    def create_database_conn(self):
        """
        Connects to the database using credentials from a JSON file.

        Returns:
        psycopg2.connection: A connection to the PostgreSQL database.
        """
        
        try:
            # Import database credentials from json file
            db_credentials_file_name = 'LEA_Finance_Survey_DB.json'
            db_credentials_path = os.path.join("..", db_credentials_file_name)
            with open(db_credentials_path) as infile:
                credentials = json.load(infile)

            # Assign Credentials to Variables
            database_name = credentials['database']
            username = credentials['user']
            password = credentials['password']
            host = credentials['host']
            port = credentials['port']

            # Establish a connection to the database
            conn = psycopg2.connect(
                dbname=database_name,
                user=username,
                password=password,
                host=host,
                port=port
            )

            return conn
        except Exception as e:
            print(f"Failed to connect to database. Error: {e}")


    ############################## Query Database to DataFrame ##############################
    def execute_sql(self, query: str, conn) -> pd.DataFrame:
        """
        Executes an SQL query on the provided database connection.

        Parameters:
        query (str): SQL query to execute.
        conn (psycopg2.connection): Connection to the database.

        Returns:
        pd.DataFrame: Result of the SQL query as a DataFrame.
        """

        # Create a new cursor
        cur = conn.cursor()

        try:
            # Create a new cursor using the connection passed as an argument
            cur = conn.cursor()
            
            # Execute the SQL query
            cur.execute(query)

            # Fetch the results
            rows = cur.fetchall()

            # Get the column names
            colnames = [desc[0] for desc in cur.description]

            # Convert query to dataframe
            df = pd.DataFrame(rows, columns=colnames)

        except OperationalError as e:
            print(f"An error occurred: {e}")
            df = pd.DataFrame()
        finally:
            # Close the cursor after the operation is complete
            if cur is not None:
                cur.close()
        
        return df


        ############################## Aggregate Functions ##############################

    def get_year_total(self, df: pd.DataFrame, year: int, column_name: str):
        """
        Gets the total amount for a specified year and column from a DataFrame.

        Parameters:
        df (pd.DataFrame): DataFrame to search in.
        year (int): Year to filter by.
        column_name (str): Name of the column containing the amount.

        Returns:
        float: Total for the specified year and column.
        """

        total = df[df['year'] == year][column_name].sum()
        return total

    
    def calculate_total_difference(self, amount1, amount2):
        """
        Calculates the total difference between two amounts.

        Parameters:
        amount1: First amount.
        amount2: Second amount.

        Returns:
        float: Difference between the two amounts.
        """

        return amount2 - amount1
    
    def calculate_percentage_difference(self, initial_amount, final_amount):
        """
        Calculates the percentage difference between two amounts.

        Parameters:
        initial_amount: Initial amount.
        final_amount: Final amount.

        Returns:
        float or None: Percentage difference between the two amounts. Returns None if initial_amount is 0.
        """

        if initial_amount == 0:
            return None  # Avoid division by zero
        return ((final_amount - initial_amount) / initial_amount) * 100
    
    def calculate_mean_growth_rate(self, df: pd.DataFrame, expenditure_title: Optional[str] = None, start_year : int = None, end_year : int = None) -> float:
        """
        Calculates the mean growth rate for a given expenditure title and year range.

        Parameters:
        df (pd.DataFrame): DataFrame to search in.
        expenditure_title (str, optional): The title of the expenditure to filter by. Default is None.
        start_year (int): The start of the year range.
        end_year (int): The end of the year range.

        Returns:
        float: Mean growth rate for the specified expenditure title and year range.
        """

        if expenditure_title:
            filtered_data = df[
                (df['expenditure_title'] == expenditure_title) &
                df['year'].between(start_year, end_year)
            ]
        else:
            filtered_data = df[df['year'].between(start_year, end_year)]

        mean_growth_rate = filtered_data['growth_rate'].mean()
        return mean_growth_rate


    ############################## Graph Functions ##############################
    """
    The subsequent lines of code contain various functions for creating different types of charts. 
    These functions are designed to ensure stylistic consistency across all charts and to minimize redundant code in my analyses. 
    They allow for easy customization and quick generation of complex visualizations, streamlining the data presentation process.
    """

    def make_bar_chart_grid(self, df : pd.DataFrame, x : str, y : str, 
                            color : str, facet_col : str, facet_col_wrap : int, title : str) -> go.Figure:
        """
        Creates a grid of bar charts using Plotly Express.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data to plot.
        x (str): The name of the column to use for the x-axis.
        y (str): The name of the column to use for the y-axis.
        color (str): The name of the column to use for color coding.
        facet_col (str): The name of the column to create separate plots for each unique value.
        facet_col_wrap (int): The number of charts per row.
        title (str): The title of the plot.

        Returns:
        go.Figure: A Plotly graph object representing the bar chart grid.
        """

        bar_plot_grid = px.bar(df, 
                    x= x, 
                    y= y,
                    facet_col= facet_col,
                    facet_col_wrap= facet_col_wrap,
                    color= color
                    )

        # Update layout with given title and additional layout arguments
        bar_plot_grid.update_layout(title_text= title,
                                    title={
                                        'y':0.98,  # The position of the title can be adjusted with the y parameter
                                        'x':0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top'
                                        },
                                    height=800,
                                    width=1050, 
                                    legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=-0.5,  # Adjusted position
                                        xanchor="center",
                                        x=0.5
                                        ),
                                    margin=dict(l=40, r=40, t=80, b=200),  # Increase the top margin for padding
                                    hoverlabel=dict(
                                        bgcolor="white",
                                        font_size=16,
                                        font_family="Calibri"
                                        )
                                    )

        bar_plot_grid.update_annotations(font_size=10)  # Reduce font size for subplot titles
        
        return bar_plot_grid
    
    def make_line_plot_grid(self, df : pd.DataFrame, x : str, y : str, 
                        color : str, facet_col : str, facet_col_wrap : int, title : str) -> go.Figure:
        """
        Creates a grid of line charts using Plotly Express.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data to plot.
        x (str): The name of the column to use for the x-axis.
        y (str): The name of the column to use for the y-axis.
        color (str): The name of the column to use for color coding.
        facet_col (str): The name of the column to create separate plots for each unique value.
        facet_col_wrap (int): The number of charts per row.
        title (str): The title of the plot.

        Returns:
        go.Figure: A Plotly graph object representing the line plot grid.
        """

        # Create the grid of line charts
        line_plot_grid = px.line(
            df,
            x= x,
            y= y,  
            color= color,
            facet_col= facet_col,  # Creates a separate plot for each region
            facet_col_wrap= facet_col_wrap,    # Adjust this to control how many charts per row
            title= title
        )

        # Update layout with given title and additional layout arguments
        line_plot_grid.update_layout(title_text=title,
                                title={
                                    'y':0.98,  # The position of the title can be adjusted with the y parameter
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                    },
                                    height=800,
                                    width=1050, 
                                    legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=-0.5,  # Adjusted position
                                        xanchor="center",
                                        x=0.5
                                        ),
                                    margin=dict(l=40, r=40, t=80, b=200),  # Increase the top margin for padding
                                    hoverlabel=dict(
                                        bgcolor="white",
                                        font_size=16,
                                        font_family="Calibri"
                                        )
                                    )

        line_plot_grid.update_annotations(font_size=10)  # Reduce font size for subplot titles
        line_plot_grid.update_xaxes(tickangle=45, tickfont=dict(size=10)) # Update Tick Angles and Axis Font Size

        return line_plot_grid
    
    def create_combined_figure(self, fig1: go.Figure, fig2: go.Figure,
                               title: str, subplot_titles: tuple) -> go.Figure:
        """
        Creates a combined figure with two subplots.

        Parameters:
        fig1 (go.Figure): The first figure to be added to the subplot.
        fig2 (go.Figure): The second figure to be added to the subplot.
        title (str): The main title of the combined figure.
        subplot_titles (tuple): Titles for the subplots (two elements expected).

        Returns:
        go.Figure: A combined figure with two subplots.
        """

        # Create a subplot figure
        combined_fig = make_subplots(rows=1, cols=2, subplot_titles=subplot_titles,
                                    horizontal_spacing=0.1)

        # Add traces from fig1 to the first subplot
        for trace in fig1['data']:
            combined_fig.append_trace(trace, row=1, col=1)

        # Add traces from fig2 to the second subplot
        for trace in fig2['data']:
            combined_fig.append_trace(trace, row=1, col=2)

        # Update layout with given title and additional layout arguments
        combined_fig.update_layout(title_text=title,
                                title={
                                    'y':0.98,  # The position of the title can be adjusted with the y parameter
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                    },
                                    height=600,
                                    width=1050, 
                                    legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=-0.3,  # Adjusted position
                                        xanchor="center",
                                        x=0.5
                                        ),
                                    margin=dict(l=40, r=40, t=80, b=200),  # Increase the top margin for padding
                                    hoverlabel=dict(
                                        bgcolor="white",
                                        font_size=16,
                                        font_family="Calibri"
                                        )
                                    )

        return combined_fig